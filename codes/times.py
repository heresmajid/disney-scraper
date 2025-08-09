import requests
from datetime import datetime, timedelta, date
import random
import time
from pprint import pprint
import json
import pandas as pd
import concurrent.futures
from threading import Lock
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://www.disneylandparis.com',
    'Referer': 'https://www.disneylandparis.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'accept': '*/*',
    'content-type': 'application/json',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    "Authorization": "Token 6d55eau1jdzifi0nmc83kgn93liycqf97xjamz6n"
}

def generate_dates():
    """Generate list of dates to scrape"""
    today = date.today()
    # year, month, day
    end_date = date(2025, 10, 31)
    
    dates = []
    current_day = today
    while current_day <= end_date:
        dates.append(current_day.isoformat())
        current_day += timedelta(days=1)
    
    return dates

def create_request_payload(date_str):
    """Create GraphQL request payload"""
    return {
        'operationName': 'activitySchedules',
        'variables': {
            'market': 'nl-nl',
            'types': [
                {
                    'type': 'ThemePark',
                    'status': ['OPERATING', 'EXTRA_MAGIC_HOURS'],
                },
                {
                    'type': 'Attraction',
                    'status': ['REFURBISHMENT', 'OPERATING', 'CLOSED_OPS'],
                },
                {
                    'type': 'Entertainment',
                    'status': 'PERFORMANCE_TIME',
                },
            ],
            'date': date_str,
        },
        'query': 'query activitySchedules($market: String!, $types: [ActivityScheduleStatusInput]!, $date: String!) {\n  activitySchedules(market: $market, date: $date, types: $types) {\n    id\n    name\n    url\n    urlFriendlyId\n    hideFunctionality\n    shortDescription\n    iconFont\n    subType\n    thumbMedia {\n      url\n      alt\n      __typename\n    }\n    subLocation {\n      ...location\n      __typename\n    }\n    location {\n      ...location\n      __typename\n    }\n    type\n    schedules(date: $date, types: $types) {\n      startTime\n      endTime\n      date\n      status\n      closed\n      language\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment location on Location {\n  id\n  value\n  urlFriendlyId\n  iconFont\n  url\n  __typename\n}\n',
    }

def fetch_data_for_date(date_str, session):
    """Fetch data for a single date"""
    try:
        json_data = create_request_payload(date_str)
        
        proxy = "http://proxy_username:proxy_password@domain_name:proxy_port"
        proxies = {"http": proxy, "https": proxy}
        
        response = session.post(
            'https://api.disneylandparis.com/query', 
            headers=headers, 
            json=json_data, 
            proxies=proxies,
            timeout=30
        )
        
        # Reduced sleep time
        time.sleep(random.uniform(0.5, 1.5))
        
        logger.info(f"Date: {date_str}, Status: {response.status_code}")
        
        if response.status_code == 200:
            return date_str, response.json()['data']['activitySchedules']
        else:
            logger.warning(f"Failed for date {date_str}: {response.status_code}")
            return date_str, None
            
    except Exception as e:
        logger.error(f"Error fetching data for {date_str}: {e}")
        return date_str, None

def process_activities(date_str, activities):
    """Process activities data for a date"""
    if not activities:
        return []
    
    results = []
    target_locations = {"Walt Disney Studios Park", "Disneyland Park"}
    
    for activity in activities:
        location = activity['name']
        if location in target_locations:
            schedules = activity.get('schedules', [])
            for schedule in schedules:
                result = {
                    'date': date_str,
                    'location': location,
                    'status': schedule.get('status'),
                    'starting_time': schedule.get('startTime'),
                    'ending_time': schedule.get('endTime')
                }
                results.append(result)
    
    return results

def main():
    """Main function with concurrent processing"""
    scraping_dates = generate_dates()
    logger.info(f"Scraping {len(scraping_dates)} dates")
    
    all_data = []
    data_lock = Lock()
    
    # Use session for connection pooling
    session = requests.Session()
    
    # Use ThreadPoolExecutor for concurrent requests
    max_workers = 5  # Adjust based on rate limits
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_date = {
            executor.submit(fetch_data_for_date, date_str, session): date_str 
            for date_str in scraping_dates
        }
        
        # Process completed tasks
        for future in concurrent.futures.as_completed(future_to_date):
            date_str, activities = future.result()
            
            if activities:
                processed_data = process_activities(date_str, activities)
                
                with data_lock:
                    all_data.extend(processed_data)
                    logger.info(f"Processed {len(processed_data)} records for {date_str}")
    
    # Remove duplicates using pandas (much faster than list comparison)
    df = pd.DataFrame(all_data)
    if not df.empty:
        df = df.drop_duplicates()
        
        # Sort by date and then by location for consistent ordering
        df['date_sort'] = pd.to_datetime(df['date'])
        df = df.sort_values(['date_sort', 'location', 'starting_time'])
        df = df.drop('date_sort', axis=1)  # Remove the temporary sort column
        
        logger.info(f"Total unique records: {len(df)}")
        
        # Create output directory if it doesn't exist
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")
        
        # Save data
        df.to_json('output/times.json', orient='records', indent=4)
        df.to_csv('output/times.csv', index=False)
        
        logger.info("Data saved successfully to output folder!")
    else:
        logger.warning("No data collected!")

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    logger.info(f"Total execution time: {end_time - start_time:.2f} seconds")