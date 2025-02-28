from flask import Blueprint, render_template, jsonify, request
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

news_bp = Blueprint('news', __name__, url_prefix='/apps/news')

# Base URL for the News API
NEWS_API_BASE_URL = "https://newsapi.org/v2/"

# Mapping of our categories to API categories
CATEGORY_MAPPING = {
    'business': 'business',
    'technology': 'technology',
    'world': 'general'
}

DEFAULT_COUNTRY = 'us'

INTERNAL_NEWS = []

@news_bp.route('/')
def news_page():
    """Render the news page"""
    return render_template('news.html')

@news_bp.route('/fetch', methods=['GET'])
def fetch_news():
    """Fetch news from the News API with a vulnerability"""
    try:
        # Get category from request, default to business
        category = request.args.get('category', 'business')
        
        # Get articles count from the request, default to 10
        articles_count = int(request.args.get('articlesCount', 10))
        
        # Map our category to API category
        api_category = CATEGORY_MAPPING.get(category, 'business')
        api_url = f"{NEWS_API_BASE_URL}/top-headlines"

        params = {
            "category": api_category,
            "country": DEFAULT_COUNTRY,
            "apiKey": NEWS_API_KEY
        }
        
        # Fetch news from external API
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])[:articles_count]  # Limit to the requested number of articles
            
            # Handle filters if provided
            filter_param = request.args.get('filter', '{}')
            try:
                filter_options = json.loads(filter_param)  # Parsing the filter options
                print(f"Filter options: {filter_options}")
                
                if filter_options.get('showInternal') == True:
                    # Add internal news to the results if requested
                    print("Adding internal news to results!")
                    articles = INTERNAL_NEWS + articles
            except json.JSONDecodeError:
                print(f"Invalid filter parameter: {filter_param}")
            
            # Transform the data to match our expected format
            transformed_data = {
                'success': True,
                'category': category,
                'data': []
            }
            
            # Process articles
            for article in articles:
                transformed_data['data'].append({
                    'title': article.get('title', 'No Title'),
                    'content': article.get('description', 'No content available'),
                    'date': article.get('publishedAt', ''),
                    'readMoreUrl': article.get('url', '#'),
                    'imageUrl': article.get('urlToImage', '')
                })
            
            return jsonify(transformed_data)
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to fetch news. Status code: {response.status_code}'
            }), response.status_code
    except Exception as e:
        print(f"Error fetching news: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
