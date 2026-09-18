import os

import numpy as np
import pandas as pd
import streamlit as st
import snowflake.connector
import torch

from dotenv import load_dotenv
from groq import Groq
from transformers import AutoModel, AutoTokenizer


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

BGE_M3_PATH = (
    r"C:\Users\chara\.cache\huggingface\hub\models--BAAI--bge-m3"
    r"\snapshots\5617a9f61b028005a4858fdac845db406aefb181"
)

CHAT_MODEL = "openai/gpt-oss-120b"

NEW_REVIEWS = 500

TOK_K = 5

CACHE_FILE = "review_embeddings.parquet"


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ============================================================
# BGE-M3 MODEL
# ============================================================

tokenizer = AutoTokenizer.from_pretrained(
    BGE_M3_PATH,
    local_files_only=True,
    use_fast=False
)

embedding_model = AutoModel.from_pretrained(
    BGE_M3_PATH,
    local_files_only=True,
    use_safetensors=False
)

embedding_model.eval()


# ============================================================
# READ REVIEWS FROM SNOWFLAKE
# ============================================================

def read_reviews_from_snowflake():

    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )

    query = f"""
        SELECT
            REVIEW_ID,
            CITY,
            RATING,
            COMMENT
        FROM ZOMATO.STAGING.STG_REVIEWS
        SAMPLE ({NEW_REVIEWS} ROWS)
    """

    df = (
        conn
        .cursor()
        .execute(query)
        .fetch_pandas_all()
    )

    conn.close()

    df.columns = [
        col.lower()
        for col in df.columns
    ]

    return df


# ============================================================
# CREATE BGE-M3 EMBEDDINGS
# ============================================================

def embed(texts):

    inputs = tokenizer(
        texts,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = embedding_model(
            **inputs
        )

    # Use the CLS token representation
    embeddings = outputs.last_hidden_state[:, 0]

    # Normalize embeddings for cosine similarity
    embeddings = torch.nn.functional.normalize(
        embeddings,
        p=2,
        dim=1
    )

    return embeddings.cpu().tolist()


# ============================================================
# LOAD REVIEWS + EMBEDDINGS
# ============================================================

@st.cache_data()
def load_reviews():

    if os.path.exists(CACHE_FILE):

        return pd.read_parquet(
            CACHE_FILE
        )

    df = read_reviews_from_snowflake()

    df["embedding"] = embed(
        df["comment"].fillna("").tolist()
    )

    df.to_parquet(
        CACHE_FILE
    )

    return df


# ============================================================
# STREAMLIT UI
# ============================================================

st.title(
    "Chat with your Zomato Reviews"
)

st.caption(
    f"Searching {NEW_REVIEWS} reviews, "
    f"answering with {CHAT_MODEL} model"
)


# ============================================================
# COSINE SIMILARITY
# ============================================================

def cosine_similarity(
    vec_a,
    vec_b
):

    return np.dot(
        vec_a,
        vec_b
    ) / (
        np.linalg.norm(vec_a)
        *
        np.linalg.norm(vec_b)
    )


# ============================================================
# FIND SIMILAR REVIEWS
# ============================================================

def find_similar_reviews(
    question,
    df
):

    question_vector = embed(
        [question]
    )[0]

    scores = []

    for review_vector in df["embedding"]:

        scores.append(
            cosine_similarity(
                question_vector,
                review_vector
            )
        )

    df = df.copy()

    df["score"] = scores

    return df.nlargest(
        TOK_K,
        "score"
    )


# ============================================================
# ASK GROQ LLM
# ============================================================

def ask_llm(
    question,
    top_reviews
):

    context = ""

    for _, row in top_reviews.iterrows():

        context += (
            f"({row['city']}, "
            f"{row['rating']} stars) "
            f"{row['comment']}\n"
        )

    system_prompt = (
        "Answer ONLY using the customer reviews provided. "
        "Be concise. "
        "If the reviews don't cover it, say so."
    )

    user_prompt = (
        f"Question: {question}\n\n"
        f"Reviews:\n{context}"
    )

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return response.choices[0].message.content


# ============================================================
# LOAD REVIEW DATA
# ============================================================

review_df = load_reviews()


# ============================================================
# USER QUESTION
# ============================================================

question = st.text_input(
    "Ask a question about your reviews:",
    placeholder=(
        "e.g. What are the most common complaints "
        "about delivery?"
    )
)


# ============================================================
# RAG PIPELINE
# ============================================================

if question:

    top_reviews = find_similar_reviews(
        question,
        review_df
    )

    answer = ask_llm(
        question,
        top_reviews
    )

    st.markdown(
        "**Answer:**"
    )

    st.write(
        answer
    )

    with st.expander(
        "Reviews used to build this answer"
    ):

        st.dataframe(
            top_reviews[
                [
                    "city",
                    "rating",
                    "comment"
                ]
            ],
            hide_index=True
        )