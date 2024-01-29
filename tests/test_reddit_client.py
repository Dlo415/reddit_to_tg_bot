import pytest
from requests.exceptions import HTTPError, ConnectionError, Timeout
from app.reddit.reddit_api import RedditClient
from unittest.mock import patch
from requests.models import Response

@pytest.fixture
def reddit_client(mock_response):
    with patch('requests.Session.post', return_value=mock_response):
        return RedditClient('client_id', 'client_secret', 'username', 'password', 'user_agent')

@pytest.fixture
def mock_response(mocker):
    mock_resp = mocker.Mock()
    mock_resp.json.return_value = {'access_token': 'test_token'}
    return mock_resp

def test_get_reddit_token_success(mocker, reddit_client, mock_response):
    mocker.patch('requests.Session.post', return_value=mock_response)
    token = reddit_client.get_reddit_token('client_id', 'client_secret', 'username', 'password')
    assert token == 'test_token'

def test_get_reddit_token_failure(mocker, reddit_client):
    mocker.patch('requests.Session.post', side_effect=ConnectionError)
    with pytest.raises(ConnectionError):
        reddit_client.get_reddit_token('client_id', 'client_secret', 'username', 'password')

def test_get_20_new_posts_success(mocker, reddit_client, mock_response):
    mock_response.json.return_value = {'data': {'children': ['post1', 'post2']}}
    mocker.patch('requests.Session.get', return_value=mock_response)
    posts = reddit_client.get_20_new_posts('subreddit')
    assert posts == ['post1', 'post2']

def test_authentication_failure(mocker, reddit_client):
    mock_response = mocker.Mock(spec=Response)
    mock_response.status_code = 401
    http_error = HTTPError(response=mock_response)
    mocker.patch('requests.Session.post', side_effect=http_error)
    with pytest.raises(HTTPError):
        reddit_client.get_reddit_token('client_id', 'client_secret', 'wrong_username', 'wrong_password')
        reddit_client.get_reddit_token('client_id', 'client_secret', 'wrong_username', 'wrong_password')

def test_timeout_error(mocker, reddit_client):
    mocker.patch('requests.Session.post', side_effect=Timeout)
    with pytest.raises(Timeout):
        reddit_client.get_reddit_token('client_id', 'client_secret', 'username', 'password')

def test_unexpected_error(mocker, reddit_client):
    mocker.patch('requests.Session.post', side_effect=Exception("Unexpected error"))
    with pytest.raises(Exception):
        reddit_client.get_reddit_token('client_id', 'client_secret', 'username', 'password')

def test_find_most_popular_post_with_data():
    posts = [
        {'data': {'score': 10}},
        {'data': {'score': 20}},
        {'data': {'score': 5}}
    ]
    result = RedditClient.find_most_popular_post(posts)
    assert result == {'data': {'score': 20}}

