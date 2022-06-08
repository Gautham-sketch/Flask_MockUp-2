from flask import Flask,jsonify,request
import csv

from storage import all_articles,liked_articles,notliked_articles
from content_filtering import get_recommendations
from demographic_filtering import output

app = Flask(__name__)
@app.route('/getArticles')
def getArticles():
    return jsonify({
        'data' : all_articles[0],
        'status' : 'success',
    })

@app.route("/likedArticles",methods=["POST"])
def likedMovies():
    article = all_articles[0]
    liked_articles.append(article)
    all_articles = all_articles[1:]
    return jsonify({
        'status' : 'success'
    }),200

@app.route("/notlikedArticles",methods=["POST"])
def notlikedMovies():
    article = all_articles[0]
    notliked_articles.append(article)
    all_articles = all_articles[1:]
    return jsonify({
        'status' : 'success'
    }),200

@app.route("/popularArticles")
def popular_articles():
    article_data = []
    for article in output:
        _d = {
            "title": article[0],
            "poster_link": article[1],
            "release_date": article[2] or "N/A",
            "duration": article[3],
            "rating": article[4],
            "overview": article[5]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

@app.route("/recommendedArticles")
def recommended_articles():
    all_recommended = []
    for liked in liked_articles:
        output = get_recommendations(liked[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "poster_link": recommended[1],
            "release_date": recommended[2] or "N/A",
            "duration": recommended[3],
            "rating": recommended[4],
            "overview": recommended[5]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200


if(__name__ == '__main__'):
    app.run()