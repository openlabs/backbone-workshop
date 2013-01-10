# -*- coding: utf-8 -*-
"""
    app

    Application code

    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from datetime import datetime

from flask import Flask, render_template, jsonify, request, abort



def get_next(ctx={'id': 0}): 
    ctx['id'] += 1
    return ctx['id']


NEWS_FEED = [
    {
        'id': get_next(),
        'time': datetime.utcnow().isoformat(),
        'message': 'Hello World'
    }
]

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def hello_world():
    return render_template('index.jinja')

@app.route('/news-feed/', methods=['GET', 'POST'])
@app.route('/news-feed/<int:feed_id>', methods=['GET', 'PUT', 'DELETE'])
def news_feed(feed_id=None):
    print request.method
    if request.method == 'POST':
        NEWS_FEED.append({
            'id': get_next(),
            'time': datetime.utcnow().isoformat(),
            'message': request.json and \
                    request.json['message'] or request.form['message']
        })
        print NEWS_FEED

    if feed_id:
        for feed_item in NEWS_FEED:
            if feed_item['id'] == feed_id:
                break
        else:
            abort(404)

        if request.method == 'PUT':
            feed_item['message'] = request.json['message']

        if request.method == 'DELETE':
            NEWS_FEED.remove(feed_item)
            return jsonify({})

        if request.is_xhr:
            return jsonify(feed_item)
        return render_template('feeditem.jinja', feed_item=feed_item)

    if request.is_xhr:
        return jsonify(result=NEWS_FEED)
    return render_template('newsfeed.jinja', feed_items=NEWS_FEED)


if __name__ == '__main__':
    app.debug = True
    app.run()
