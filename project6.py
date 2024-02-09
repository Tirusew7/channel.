import io
import sys
from bs4 import BeautifulSoup
import requests
import time
import logging

BOT_TOKEN = '6485261689:AAG-L4aPGR6zEW3eOlGNdCJbWW_cL9PRYiI'
CHANNEL_ID = '@my_projec'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

posted_posts = set()

def send_to_channel(message):
    try:
        api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        params = {
            'chat_id': CHANNEL_ID,
            'text': message,
            'parse_mode': 'HTML'
        }

        response = requests.post(api_url, params=params)
        response.raise_for_status()

        logger.info("Message sent successfully to the channel.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending message to the channel: {e}")

def scrape_and_send_to_channel():
    url = 'https://www.fanabc.com/%e1%88%b5%e1%8d%93%e1%88%ad%e1%89%b5/'

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to retrieve the webpage. Error: {e}")
        return

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
    
        posts = soup.find_all('div', class_='wpb_column bs-vc-column vc_column_container vc_col-sm-12')

        for post in posts:
            post_title = post.find('a', class_='post-url post-title')
            title_text = post_title.text.strip() if post_title else ' '
            title_link = post_title.get('href', '') if post_title else ''

            
            if title_text not in posted_posts:
                message = f"<b>Title:</b> {title_text}\n<b>Link:</b> {title_link}\n"
                logger.info(f"Sending message to the channel for: {title_text}")
                send_to_channel(message)

                
                posted_posts.add(title_text)

            time.sleep(5)

    else:
        logger.warning(f"Failed to retrieve the webpage. Status code: {response.status_code}")


while True:
    scrape_and_send_to_channel()
    time.sleep(600)
