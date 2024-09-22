import json

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
    app.run(host='0.0.0.0', port=5000)
