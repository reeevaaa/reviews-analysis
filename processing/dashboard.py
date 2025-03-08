import streamlit as st  
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load processed data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("./processed_reviews.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Function to generate word cloud
def generate_wordcloud(text, title):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title)
    st.pyplot(fig)

# Streamlit Dashboard Setup
st.set_page_config(page_title="Sentiment & Topic Analysis", layout="wide")
st.title("📊 Sentiment & Topic Analysis Dashboard")

st.write("This dashboard provides insights into customer reviews using sentiment analysis and LDA-based topic classification.")

# Load Data
df = load_data()

if df is None:
    st.error("❌ Failed to load data file")
else:
    # 🔍 Latest Reviews
    st.subheader("🔍 Latest Reviews")
    st.dataframe(df.head(10))

    # 📈 Sentiment Analysis
    if "Sentiment" in df.columns and "Processed_Review" in df.columns:
        st.subheader("📊 Sentiment Distribution")
        sentiment_counts = df["Sentiment"].value_counts().reset_index()
        sentiment_counts.columns = ["Sentiment", "Count"]

        sentiment_fig = px.pie(
            sentiment_counts, 
            names="Sentiment", 
            values="Count", 
            title="Sentiment Distribution",
            color="Sentiment",
            color_discrete_map={"Positive": "#1a936f", "Neutral": "#f4a261", "Negative": "#e63946"}
        )
        st.plotly_chart(sentiment_fig, use_container_width=True)

        # Generate word clouds for positive and negative sentiments
        st.subheader("🌥️ Word Clouds")

        # Extracting reviews for each sentiment
        positive_reviews = " ".join(df[df["Sentiment"] == "Positive"]["Processed_Review"].dropna())
        negative_reviews = " ".join(df[df["Sentiment"] == "Negative"]["Processed_Review"].dropna())

        col1, col2 = st.columns(2)
        with col1:
            if positive_reviews:
                generate_wordcloud(positive_reviews, "Positive Sentiment Word Cloud")
            else:
                st.warning("⚠️ No positive reviews available for word cloud.")

        with col2:
            if negative_reviews:
                generate_wordcloud(negative_reviews, "Negative Sentiment Word Cloud")
            else:
                st.warning("⚠️ No negative reviews available for word cloud.")

    else:
        st.warning("⚠️ Sentiment or Processed Review data not available")

    # ✅ Food vs Beverage Analysis
    if "Category" in df.columns:  # Assuming your data has a 'Category' column
        st.subheader("🍔 Food vs Beverage Analysis")

        # Separate Food and Beverage
        food_df = df[df['Category'].str.contains('food', case=False, na=False)]
        beverage_df = df[df['Category'].str.contains('beverage', case=False, na=False)]

        # 📊 Sentiment Distribution for Food and Beverage
        st.subheader("📊 Sentiment Comparison: Food vs Beverage")
        col1, col2 = st.columns(2)

        # Food Sentiment
        with col1:
            st.write("### Food Sentiment")
            food_sentiment_counts = food_df["Sentiment"].value_counts().reset_index()
            food_sentiment_counts.columns = ["Sentiment", "Count"]

            food_fig = px.pie(
                food_sentiment_counts, 
                names="Sentiment", 
                values="Count", 
                title="Food Sentiment Distribution",
                color="Sentiment",
                color_discrete_map={"Positive": "green", "Neutral": "orange", "Negative": "red"}
            )
            st.plotly_chart(food_fig, use_container_width=True)

        # Beverage Sentiment
        with col2:
            st.write("### Beverage Sentiment")
            beverage_sentiment_counts = beverage_df["Sentiment"].value_counts().reset_index()
            beverage_sentiment_counts.columns = ["Sentiment", "Count"]

            beverage_fig = px.pie(
                beverage_sentiment_counts, 
                names="Sentiment", 
                values="Count", 
                title="Beverage Sentiment Distribution",
                color="Sentiment",
                color_discrete_map={"Positive": "green", "Neutral": "orange", "Negative": "red"}
            )
            st.plotly_chart(beverage_fig, use_container_width=True)

        # 📜 Word Cloud for Food and Beverage
        st.subheader("🌥️ Word Cloud: Food vs Beverage")
        col1, col2 = st.columns(2)

        # Food Word Cloud
        with col1:
            st.write("### Food Word Cloud")
            food_reviews = " ".join(food_df["Processed_Review"].dropna())
            if food_reviews:
                generate_wordcloud(food_reviews, "Food Word Cloud")
            else:
                st.warning("⚠️ No food reviews available.")

        # Beverage Word Cloud
        with col2:
            st.write("### Beverage Word Cloud")
            beverage_reviews = " ".join(beverage_df["Processed_Review"].dropna())
            if beverage_reviews:
                generate_wordcloud(beverage_reviews, "Beverage Word Cloud")
            else:
                st.warning("⚠️ No beverage reviews available.")

    # 📌 Topic Classification
    if "Topic" in df.columns:
        st.subheader("📌 Topic Analysis")
        topic_counts = df["Topic"].value_counts().reset_index()
        topic_counts.columns = ["Topic", "Count"]

        topic_fig = px.bar(
            topic_counts, 
            x="Topic", 
            y="Count", 
            text="Count", 
            title="Topic Distribution",
            color="Topic"
        )
        st.plotly_chart(topic_fig, use_container_width=True)

    # ⭐ Rating Distribution
    if "Rating" in df.columns:
        st.subheader("⭐ Ratings Distribution")
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
        
        rating_fig = px.histogram(
            df, x="Rating", nbins=10, title="Distribution of Ratings",
            color_discrete_sequence=['#FF4B4B']
        )
        rating_fig.update_layout(showlegend=False)
        st.plotly_chart(rating_fig, use_container_width=True)

    # 📑 Raw Data
    st.subheader("📑 Raw Data")
    st.dataframe(df)

# 🔄 Manual Refresh Button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.experimental_rerun()
