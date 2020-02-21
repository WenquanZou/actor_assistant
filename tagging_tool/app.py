import spacy
import os
from flask import Flask, render_template, request, jsonify
import lxml.etree as ET

TEMPLATE_DIR = os.path.abspath('static')
app = Flask(__name__, template_folder=TEMPLATE_DIR)
nlp = None
MODEL = 'en_core_web_sm'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tokenise', methods=['POST'])
def tokenise():
    if not request.json or 'text' not in request.json:
        return jsonify({'success': False, 'error': 'Text not found.'}), 400

    text = request.json['text']
    ext = request.json['extension'] if 'extension' in request.json else ''
    meta = {}

    if ext == 'xml':
        text = extract_xml(text)

    # Extract tokens from spaCy
    # tokens = nlp.extract_tokens(text)
    return jsonify({'success': True, 'data': text})


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


def extract_xml(text):
    script_dir = os.path.abspath("shakespeare_scripts")
    xml_filename = os.path.join(script_dir, "ps_alls_well_that_ends_well.xml")
    xsl_dir = os.path.dirname(__file__)
    xsl_filename = os.path.join(xsl_dir, "transform_scripts.xsl")
    
    dom = ET.parse(xml_filename)
    xslt = ET.parse(xsl_filename)
    transform = ET.XSLT(xslt)
    new_dom = transform(dom)
    result = str(new_dom)
    
    return result


def concat_elements(root, tag):
    return ' '.join(map(lambda i: i.text, root.findall(tag)))


class NLP:
    def __init__(self):
        self.nlp = spacy.load(MODEL)
        print("spaCy loaded.")

    def extract_tokens(self, text):
        doc = self.nlp(text)
        return list(map(lambda token: token.text, doc))


if __name__ == '__main__':
    nlp = NLP()
    app.run(debug=True)
