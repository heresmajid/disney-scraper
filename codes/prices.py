import requests
import time
import json
import logging
import os
from datetime import date, datetime
from typing import List, Dict, Any, Optional
import pandas as pd
import asyncio
import aiohttp
from dataclasses import dataclass

# Configuration
CONFIG = {
    'market': 'nl-nl',
    'currency': 'EUR',
    # year, month, day
    'end_date': date(2026, 3, 31),
    'output_files': {
        'json': 'output/prices.json',
        'csv': 'output/prices.csv'
    },
    'request_delay': 1.0,  # seconds between requests
    'max_retries': 3
}

# Product configurations
PRODUCT_OPTIONS = [
    {
        'park_type': '1-day-1-park',
        'deal_category': 'special deal',
        'adult_code': 'TKITK6061A',
        'child_code': 'TKITK6061C'
    },
    {
        'park_type': '1-day-2-parks', 
        'deal_category': 'special deal',
        'adult_code': 'TKITHL081A',
        'child_code': 'TKITHL081C'
    },
    {
        'park_type': '1-day-1-park',
        'deal_category': 'regular deal', 
        'adult_code': 'TKITK6001A',
        'child_code': 'TKITK6001C'
    },
    {
        'park_type': '1-day-2-parks',
        'deal_category': 'regular deal',
        'adult_code': 'TKITHL001A', 
        'child_code': 'TKITHL001C'
    }
]

HEADERS = {
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.7',
    'Access-Control-Allow-Credentials': 'true',
    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
    'Access-Control-Allow-Origin': 'disneylandparis.com',
    'Connection': 'keep-alive',
    'Content-type': 'application/json; charset=UTF-8',
    'Origin': 'https://tickets.disneylandparis.com',
    'Referer': 'https://tickets.disneylandparis.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

API_URL = 'https://api.disneylandparis.com/prices-calendar/api/v2/prices/ticket-price-calendar'

@dataclass
class PriceData:
    date: str
    deal_category: str
    park_category: str
    available: str
    adult_price: str
    child_price: str
    range: str

class DisneyPriceScraper:
    def __init__(self):
        self.setup_logging()
        self.data: List[Dict[str, Any]] = []
        
    def setup_logging(self):
        """Configure logging for the scraper."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_date_range(self) -> tuple[str, str]:
        """Get formatted start and end dates."""
        today = datetime.today().date().isoformat()
        end_date = CONFIG['end_date'].isoformat()
        
        self.logger.info(f"Date range: {today} to {end_date}")
        return today, end_date

    def build_request_payload(self, product_option: Dict[str, str], start_date: str, end_date: str) -> Dict[str, Any]:
        """Build the JSON payload for API request."""
        return {
            'market': CONFIG['market'],
            'currency': CONFIG['currency'],
            'startDate': start_date,
            'endDate': end_date,
            'products': [{
                'productType': product_option['park_type'],
                'adultProductCode': product_option['adult_code'],
                'childProductCode': product_option['child_code'],
            }],
            'eligibilityInformation': {
                'salesChannel': 'DIRECT',
                'membershipType': '',
                'masterCategoryCodes': [
                    'EVENT',
                    'TICKET', 
                    'TKTEXPERI',
                ],
            },
        }

    def fetch_prices_for_product(self, product_option: Dict[str, str], start_date: str, end_date: str) -> Optional[List[Dict[str, Any]]]:
        """Fetch price data for a specific product configuration."""
        park_type = product_option['park_type']
        deal_category = product_option['deal_category']
        
        self.logger.info(f"Fetching prices for {deal_category} - {park_type}")
        
        json_data = self.build_request_payload(product_option, start_date, end_date)
        
        # Proxy configuration
        proxy = "http://jvaqddnv-rotate:291zhr06ylwg@p.webshare.io:80"
        proxies = {"http": proxy, "https": proxy}
        
        for attempt in range(CONFIG['max_retries']):
            try:
                response = requests.post(API_URL, headers=HEADERS, json=json_data, proxies=proxies, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                if 'calendar' not in data:
                    self.logger.error(f"Invalid response structure for {park_type}")
                    return None
                
                return self.process_calendar_data(data['calendar'], park_type, deal_category)
                
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for {park_type}: {e}")
                if attempt < CONFIG['max_retries'] - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    self.logger.error(f"All attempts failed for {park_type}")
                    return None
            except (KeyError, ValueError) as e:
                self.logger.error(f"Data processing error for {park_type}: {e}")
                return None
        
        return None

    def process_calendar_data(self, calendar: List[Dict[str, Any]], park_type: str, deal_category: str) -> List[Dict[str, Any]]:
        """Process calendar data and extract price information."""
        processed_data = []
        
        for day_data in calendar:
            try:
                date_str = day_data['date']
                products = day_data['products']
                
                if park_type not in products:
                    self.logger.warning(f"Park type {park_type} not found in products for date {date_str}")
                    continue
                
                park_data = products[park_type]
                available = park_data.get('available', False)
                
                if available:
                    price_data = PriceData(
                        date=date_str,
                        deal_category=deal_category,
                        park_category=park_type,
                        available="Yes",
                        adult_price=park_data.get('priceAdult', ''),
                        child_price=park_data.get('priceChild', ''),
                        range=park_data.get('range', '')
                    )
                else:
                    price_data = PriceData(
                        date=date_str,
                        deal_category=deal_category,
                        park_category=park_type,
                        available="No",
                        adult_price='',
                        child_price='',
                        range=''
                    )
                
                processed_data.append(price_data.__dict__)
                self.logger.debug(f"Processed data for {date_str}: {price_data}")
                
            except KeyError as e:
                self.logger.error(f"Missing key in calendar data: {e}")
                continue
        
        return processed_data

    def scrape_all_prices(self) -> List[Dict[str, Any]]:
        """Scrape prices for all product configurations."""
        start_date, end_date = self.get_date_range()
        all_data = []
        
        for product_option in PRODUCT_OPTIONS:
            product_data = self.fetch_prices_for_product(product_option, start_date, end_date)
            
            if product_data:
                all_data.extend(product_data)
                self.logger.info(f"Successfully fetched {len(product_data)} records for {product_option['park_type']} - {product_option['deal_category']}")
            else:
                self.logger.error(f"Failed to fetch data for {product_option['park_type']} - {product_option['deal_category']}")
            
            # Rate limiting
            time.sleep(CONFIG['request_delay'])
        
        return all_data

    def save_data(self, data: List[Dict[str, Any]]) -> None:
        """Save data to JSON and CSV files."""
        if not data:
            self.logger.warning("No data to save")
            return
        
        try:
            # Create output directory if it doesn't exist
            output_dir = 'output'
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                self.logger.info(f"Created output directory: {output_dir}")
            
            # Save as JSON
            with open(CONFIG['output_files']['json'], 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            self.logger.info(f"Data saved to {CONFIG['output_files']['json']}")
            
            # Save as CSV
            df = pd.DataFrame(data)
            df.to_csv(CONFIG['output_files']['csv'], index=False, encoding='utf-8')
            self.logger.info(f"Data saved to {CONFIG['output_files']['csv']}")
            
        except Exception as e:
            self.logger.error(f"Error saving data: {e}")

    def run(self) -> None:
        """Main execution method."""
        self.logger.info("Starting Disney price scraping...")
        
        try:
            data = self.scrape_all_prices()
            
            if data:
                self.save_data(data)
                self.logger.info(f"Scraping completed successfully. Total records: {len(data)}")
            else:
                self.logger.error("No data was scraped")
                
        except Exception as e:
            self.logger.error(f"Unexpected error during scraping: {e}")

def main():
    """Entry point for the script."""
    scraper = DisneyPriceScraper()
    scraper.run()

if __name__ == "__main__":
    main()