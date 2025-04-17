from transformers import pipeline
import streamlit as st

@st.cache_resource
def load_hf_pipelines():
    summarizer = pipeline("summarization", model="google/pegasus-xsum")
    generator = pipeline("text2text-generation", model="google/flan-t5-base")
    sentiment = pipeline("sentiment-analysis")
    ner = pipeline("ner", grouped_entities=True)
    return summarizer, generator, sentiment, ner

summarizer_hf, generator_hf, sentiment_hf, ner_hf = load_hf_pipelines()