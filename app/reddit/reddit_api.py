import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import os
import logging
# Basic configuration of the logging system
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from a .env file
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
user_agent = os.getenv('USER_AGENT')
bot_token = os.getenv('BOT_TOKEN')
access_token_url = 'https://www.reddit.com/api/v1/access_token'

class RedditClient:
    """
    A client for interacting with the Reddit API.
    Handles authentication and data retrieval from Reddit.
    """

    def __init__(self, client_id: str, client_secret: str, username: str, password: str, user_agent: str):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': user_agent}
        self.token = self.get_reddit_token(client_id, client_secret, username, password)

    def get_reddit_token(self, client_id, client_secret, username, password) -> str:
        """
        Initialize the RedditClient with Reddit API credentials.
        Creates a session with the user agent and retrieves the access token.
        """
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                auth = HTTPBasicAuth(client_id, client_secret)
                data = {'grant_type': 'password', 'username': username, 'password': password}
                response = self.session.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data)
                logger.info('Reddit token retrieved successfully')
                return response.json()['access_token']

            except (requests.ConnectionError, requests.Timeout) as e:
                logger.warning(f'Network error occurred, attempt {attempt + 1} of {max_attempts}: {e}')
                if attempt + 1 == max_attempts:
                    logger.error('Max attempts reached, unable to retrieve token')
                    raise

            except requests.HTTPError as e:
                if e.response.status_code == 401:
                    logger.error('Authentication failed, check credentials')
                else:
                    logger.error(f'HTTP error: {e}')
                raise

            except Exception as e:
                logger.error(f"Unexpected error retrieving Reddit token: {e}")
                raise

    def get_20_new_posts(self, subreddit: str) -> List[Dict[str, Any]]:
        """
        Fetches the latest 20 new posts from a specified subreddit.
        Uses the access token for authorization in the header.
        """
        if not isinstance(subreddit, str) or not subreddit.strip():
            logger.error(f'Invalid parameter: {subreddit}. It should be a non-empty string.')
            return []

        try:
            headers = {'Authorization': f'bearer {self.token}'}
            params = {'limit': 20}
            response = self.session.get(f'https://oauth.reddit.com/r/{subreddit}/new', headers=headers, params=params)
            return response.json()['data']['children']

        except Exception as e:
            logger.error(f'Unexpected error while fetching posts: {e}')
            return []

    @staticmethod
    def find_most_popular_post(posts: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Identifies and returns the most popular post based on the
        highest score (upvotes) from a list of posts.
        """
        if not isinstance(posts, list) or not posts:
            logger.error(f'Invalid input type: Expected a list, got {type(posts)} or list is empty')
            return None

        try:
            return max(posts, key=lambda post: post.get('data', {}).get('score', 0))
        except Exception as e:
            logger.error(f'Error processing posts: {e}')
            return None
