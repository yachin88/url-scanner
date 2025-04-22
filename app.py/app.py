from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'wordlists'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    target_url = request.form.get('url')
    wordlist_file = request.files.get('wordlist')
    
    wordlist_path = os.path.join(UPLOAD_FOLDER, wordlist_file.filename)
    wordlist_file.save(wordlist_path)
    
    results = []

    with open(wordlist_path, 'r') as f:
        for line in f:
            path = line.strip()
            full_url = target_url.rstrip('/') + '/' + path
            try:
                response = requests.get(full_url, timeout=3)
                status = response.status_code
            except requests.RequestException:
                status = 'Error'
            results.append({'url': full_url, 'status': status})
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
