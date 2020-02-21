import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
import os
from os import listdir
from os.path import isfile, join
import lxml.etree as ET

app = flask.Flask(__name__)
cors = CORS(app)

app.config['DEBUG'] = True
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/plays', methods=['GET'])
@cross_origin()
def get_plays():
    scripts_path = os.path.abspath("shakespeare_scripts")
    all_scripts = [f for f in listdir(scripts_path) if isfile(join(scripts_path, f))]
    return jsonify({
        'plays': all_scripts
    })


@app.route('/play/<playname>', methods=['GET'])
def get_play(playname):
    script_dir = os.path.abspath("shakespeare_scripts")
    xml_filename = os.path.join(script_dir, playname)
    xsl_dir = os.path.dirname(__file__)
    xsl_filename = os.path.join(xsl_dir, "transform_scripts.xsl")

    dom = ET.parse(xml_filename)
    xslt = ET.parse(xsl_filename)
    transform = ET.XSLT(xslt)
    new_dom = transform(dom)
    return jsonify({
        'html': str(new_dom),
        'xml' : str(dom)
    })


app.run()
