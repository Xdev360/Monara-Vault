# backend/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import tweepy
from config import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up Tweepy API (v2)
client = tweepy.Client(
    consumer_key=API_KEY, 
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN, 
    access_token_secret=ACCESS_SECRET
)

# Test Twitter connection
try:
    client.get_me()
    print("Twitter authentication OK")
except tweepy.TweepError as e:
    print(f"Error during Twitter authentication: {e}")

# Scheduler instance with job store
jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
scheduler = BackgroundScheduler(jobstores=jobstores)

def post_tweet(tweet_text):
    try:
        print(f"Attempting to post tweet: {tweet_text}")
        response = client.create_tweet(text=tweet_text)
        tweet_id = response.data['id']
        print(f"Tweet posted successfully with ID: {tweet_id}")
        logging.info(f"Tweet posted successfully. ID: {tweet_id}, Text: {tweet_text}")
        return True
    except Exception as e:
        error_msg = f"Error posting tweet: {str(e)}"
        print(error_msg)
        logging.error(error_msg)
        return False

def schedule_tweet(tweet_text, schedule_time):
    try:
        # Test immediate tweet to verify credentials
        print(f"Scheduling tweet for: {schedule_time}")
        print(f"Current time is: {datetime.now()}")
        
        job = scheduler.add_job(
            post_tweet,
            'date',
            run_date=schedule_time,
            args=[tweet_text],
            id=f"tweet_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        msg = f"Tweet successfully scheduled: {tweet_text} at {schedule_time}"
        print(msg)
        logging.info(msg)
        return job
    except Exception as e:
        error_msg = f"Error scheduling tweet: {str(e)}"
        print(error_msg)
        logging.error(error_msg)
        raise

# Start scheduler
scheduler.start()
