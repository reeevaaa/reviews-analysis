# Restaurant Reviews Analysis

A comprehensive tool for scraping, analyzing, and visualizing restaurant reviews from platforms like Swiggy and Zomato.

## Project Structure

- `data/`: Stores raw and processed review data
- `scraping/`: Contains scripts for scraping reviews
- `processing/`: Text preprocessing utilities
- `sentiment_analysis/`: Sentiment analysis models
- `dashboard/`: Interactive visualization dashboard

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Scrape reviews:
   ```bash
   python scraping/scrape_reviews.py
   ```

2. Preprocess data:
   ```bash
   python processing/preprocess.py
   ```

3. Run sentiment analysis:
   ```bash
   python sentiment_analysis/sentiment_model.py
   ```

4. Launch dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```