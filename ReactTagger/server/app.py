import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
cors = CORS(app)

app.config['DEBUG'] = True
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/plays', methods=['GET'])
@cross_origin()
def get_plays():
    return jsonify({
        'plays': [f'Play{i + 1}' for i in range(20)]
    })


@app.route('/play/<playid>', methods=['GET'])
def get_play(playid):
    return jsonify({
        'html': ''.join([f'<p>{quote}</p>' for quote in ('hello world', 'good night', f'play {playid}')])
    })

app.run()