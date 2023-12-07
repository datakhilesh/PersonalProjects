from transformers import pipeline
import streamlit as st
MODEL = "jy46604790/Fake-News-Bert-Detect"
clf = pipeline("text-classification", model=MODEL, tokenizer=MODEL)


result = clf(text)
text = "JFK shot"


print(result[0]['label'])

if result[0]['label'] == "LABEL_0":
  st.write('Hello, *REAL NEWS* :sunglasses:')
