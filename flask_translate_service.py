import json
import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from deep_translator import GoogleTranslator

app = Flask(__name__)


@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data.get('text')
    dest_lang = request.args.get('dest_lang', 'ru')

    # Perform translation using deep-translator
    translator = GoogleTranslator(target=dest_lang)
    translation = translator.translate(text)

    return app.response_class(
        response=json.dumps({'translated_text': translation}, ensure_ascii=False),
        mimetype='application/json'
    )


if __name__ == '__main__':
    load_dotenv()
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(host=host, port=port)
