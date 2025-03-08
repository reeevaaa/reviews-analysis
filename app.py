from scraping.scrape_reviews import scrape_reviews
from processing.preprocess import preprocess_review_data
import schedule
import time
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

def run_pipeline():
    try:
        logging.info("Starting scraping process...")
        scrape_reviews()
        
        logging.info("Starting preprocessing...")
        preprocess_review_data(
            input_path="scraping/raw_reviews.csv",
            output_path="processing/processed_reviews.csv"
        )
        
        logging.info(f"Pipeline completed successfully at {datetime.now()}")
    except Exception as e:
        logging.error(f"Error in pipeline: {e}")

def main():
    logging.info("Starting application...")
    
    # Run once immediately
    run_pipeline()
    
    # Schedule hourly runs
    schedule.every().hour.do(run_pipeline)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute for scheduled tasks

if __name__ == "__main__":
    main()

