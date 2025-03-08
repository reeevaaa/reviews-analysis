import pandas as pd
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import os

# Download all required NLTK data
def setup_nltk():
    print("Setting up NLTK resources...")
    try:
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')
        print("✅ NLTK resources downloaded successfully")
    except Exception as e:
        print(f"⚠️ Error downloading NLTK resources: {e}")
        raise

# Load spaCy NLP model
def load_spacy_model():
    print("Loading spaCy model...")
    try:
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy model loaded successfully")
        return nlp
    except OSError:
        print("⚠️ spaCy model 'en_core_web_sm' not found. Please install it using the following command:")
        print("   python -m spacy download en_core_web_sm")
        raise

# Fix file paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(SCRIPT_DIR, "..", "raw_reviews.csv")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "processed_reviews.csv")

# Helper function for debug messages
def print_debug(message):
    print(f"DEBUG: {message}")

# Preprocessing function
def preprocess_text(text):
    try:
        text = str(text).lower()
        words = word_tokenize(text)
        stop_words = set(stopwords.words("english"))
        words = [word for word in words if word.isalpha() and word not in stop_words]
        return " ".join(words)
    except Exception as e:
        print(f"Error in preprocessing text: {e}")
        return ""

# Clean the rating
def clean_rating(rating):
    try:
        if isinstance(rating, (int, float)):
            return float(rating)
        rating_str = str(rating).strip()
        if '/' in rating_str:
            return float(rating_str.split('/')[0])
        return float(rating_str)
    except Exception as e:
        print_debug(f"Error cleaning rating '{rating}': {e}")
        return None

# Sentiment Analysis
def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    return "Neutral"

# Extract Food/Beverage entities using spaCy NER
def extract_food_beverage(text):
    doc = nlp(text)
    food_items = []
    
    # Loop through entities and capture any food or beverage items
    for ent in doc.ents:
        if ent.label_ in ["FOOD", "PRODUCT"]:
            food_items.append(ent.text)
    
    # Return unique food items (if any)
    return ", ".join(list(set(food_items))) if food_items else "N/A"

# Perform Sentiment Analysis ONLY on Food/Beverage entities
def get_food_beverage_sentiment(text):
    food_entities = extract_food_beverage(text)
    
    # If no food/beverage mentioned, return N/A
    if food_entities == "N/A":
        return "N/A"
    
    # Perform sentiment analysis only on extracted food entities
    sentiment = TextBlob(food_entities).sentiment.polarity
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

# Keyword-based Issue Classification
service_keywords = ["service", "rude", "waiter", "staff", "polite", "friendly"]
food_keywords = ["food", "yummy", "delicious", "tasty", "flavor", "coffee"]
timing_keywords = ["long", "waiting", "slow", "delay", "quick", "fast"]
location_keywords = ["location", "place", "view", "ambience", "cozy"]

def classify_issue(text):
    text_lower = text.lower()
    issue_categories = []

    if any(word in text_lower for word in service_keywords):
        issue_categories.append("Service")
    if any(word in text_lower for word in food_keywords):
        issue_categories.append("Food Quality")
    if any(word in text_lower for word in timing_keywords):
        issue_categories.append("Timing")
    if any(word in text_lower for word in location_keywords):
        issue_categories.append("Location")
    
    return ", ".join(issue_categories) if issue_categories else "General"

# Load processed reviews
def load_processed_reviews(output_path):
    processed_ids = set()
    try:
        if os.path.exists(output_path):
            existing_df = pd.read_csv(output_path)
            processed_ids = {f"{row['Name']}_{row['Review']}" for _, row in existing_df.iterrows()}
            print_debug(f"Loaded {len(processed_ids)} existing processed reviews")
    except Exception as e:
        print_debug(f"Error loading processed reviews: {e}")
    return processed_ids

# Incremental processing of reviews
def preprocess_review_data(input_path, output_path=None):
    print_debug(f"Starting incremental preprocessing for file: {input_path}")
    
    try:
        processed_ids = load_processed_reviews(output_path) if output_path else set()
        df = pd.read_csv(input_path)
        print_debug(f"Loaded {len(df)} raw reviews")
        
        df['unique_id'] = df.apply(lambda row: f"{row['Name']}_{row['Review Text']}", axis=1)
        new_reviews = df[~df['unique_id'].isin(processed_ids)].copy()
        print_debug(f"Found {len(new_reviews)} new reviews to process")
        
        if len(new_reviews) == 0:
            print_debug("No new reviews to process")
            return pd.DataFrame()
        
        # Preprocessing pipeline
        new_reviews["Processed_Review"] = new_reviews["Review Text"].astype(str).apply(preprocess_text)
        new_reviews["Rating"] = new_reviews["Rating"].apply(clean_rating)
        new_reviews["Sentiment"] = new_reviews["Processed_Review"].apply(get_sentiment)
        new_reviews["Issue_Category"] = new_reviews["Processed_Review"].apply(classify_issue)
        new_reviews["Food_Beverage"] = new_reviews["Processed_Review"].apply(extract_food_beverage)
        new_reviews["Food_Beverage_Sentiment"] = new_reviews["Processed_Review"].apply(get_food_beverage_sentiment)
        
        # Append new data
        if output_path:
            if os.path.exists(output_path):
                new_reviews.to_csv(output_path, mode='a', header=False, index=False)
            else:
                new_reviews.to_csv(output_path, index=False)
            print_debug(f"Appended {len(new_reviews)} processed reviews to: {output_path}")
        
        return new_reviews
    
    except Exception as e:
        print_debug(f"Error in preprocessing pipeline: {e}")
        raise

# Main execution
if __name__ == "__main__":
    setup_nltk()
    nlp = load_spacy_model()
    processed_df = preprocess_review_data(INPUT_PATH, OUTPUT_PATH)
    print(f"✅ Preprocessing Complete. Final columns: {processed_df.columns.tolist()}")

# Export the main function
__all__ = ['preprocess_review_data']
