from flask import Flask, url_for, redirect, request
import os
from search_engine.search_engine import search as find_similar_docs
import json

app = Flask(__name__, static_folder='/Users/mansurminnikaev/PycharmProjects/crawler/web-interface/static')


@app.route("/")
def redirect_to_index_page():
    return redirect(url_for('static', filename='index.html'), 302)


def create_response(matches):
    res = []
    for doc_id, score in matches:
        name = f'index-{doc_id}.html'
        res.append(
            {
                'name': name,
                'score': score,
                'link': url_for('static', filename='files/' + name)
            }
        )
    return json.dumps(res)


@app.route("/query", methods=["GET"])
def result_for_query():
    query = request.args.get('query')
    return create_response(find_similar_docs(query))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
