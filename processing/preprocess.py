import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def clean_text(text):
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text.lower().strip()

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text)
    return ' '.join([word for word in word_tokens if word not in stop_words])

def preprocess_reviews(input_path, output_path):
    df = pd.read_csv(input_path)
    df['cleaned_text'] = df['review_text'].apply(clean_text)
    df['processed_text'] = df['cleaned_text'].apply(remove_stopwords)
    df.to_csv(output_path, index=False)
