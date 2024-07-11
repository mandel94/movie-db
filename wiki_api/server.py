from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from wiki_clients.clients import MovieWikiClient, WikiClient

app = Flask(__name__)

cors = CORS(app, resources={r"/v1/*": {"origins": "*"}})

LIMITS = {
    "personal_requests": 5000, # requests per hour
}


# Home page
@app.route('/v1/home', methods=['GET'])
def home():
    return 'Welcome to the wiki API!'

@app.route('/v1/search/pages', methods=['GET', 'POST'])
def search_page():
    # page_title = request.args.get('title')
    # pages = wiki_client.search_page(page_title, nb_results=10)
    # response = jsonify(pages)
    # return response
    return "request.args.get('title')"

@app.route('/v1/search/movies', methods=['GET', 'POST'])
def search_movie():
    movie_title = request.args.get('title')
    movies = movie_wiki_client.search_movie(movie_title, nb_results=10)
    response = jsonify(movies)
    return response



if __name__ == '__main__':
    movie_wiki_client = MovieWikiClient(rate_limit = LIMITS["personal_requests"]) # More on rate limits policy from wikimedia can be found here: https://api.wikimedia.org/wiki/Rate_limits)
    wiki_client = WikiClient(rate_limit = LIMITS["personal_requests"])
    app.run(debug=True, host='0.0.0.0', port=5000)
    
