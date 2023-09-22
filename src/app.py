# Description: Flask app for 3GPP Document Search.

from flask import Flask, render_template, request, send_from_directory
from elasticsearch import Elasticsearch
import argparse
import os

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")

@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    Renders the index page and handles search queries.
    '''
    results = []
    query = ""
    if request.method == 'POST':
        query = request.form['query']
        response = es.search(index=app.config['IDX_NAME'], body={"query": {"match": {"content": query}}})
        for hit in response["hits"]["hits"]:
            filename = hit["_source"]["filename"]
            download_url = f"/files/download/{filename}"
            view_url = f"/files/view/{filename}"
            results.append({
                "filename": filename,
                "download_url": download_url,
                "view_url": view_url
            })
    return render_template('index.html', results=results, query=query)

@app.route('/files/<action>/<path:filename>', methods=['GET'])
def serve_file(action, filename):
    '''
    Serves the specified file for download or viewing.
    Inputs:
        action: Either "download" or "view".
        filename: Name of the file to serve.
    '''
    if action == "download":
        return send_from_directory(app.config['DOC_DIR'], filename, as_attachment=True)
    elif action == "view":
        return send_from_directory(app.config['DOC_DIR'], filename, as_attachment=False)
    else:
        return "Invalid action", 400

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Flask app for 3GPP Document Search.')
    parser.add_argument('--doc_dir', type=str, default='data/raw_docs', help="Directory containing the .txt documents.")
    parser.add_argument('--idx_name', type=str, default='3gpp_docs', help="Name of the Elasticsearch index.")
    
    args = parser.parse_args()
    
    # Store the parsed arguments in Flask's app.config
    app.config['DOC_DIR'] = os.path.abspath(args.doc_dir)
    app.config['IDX_NAME'] = args.idx_name

    app.run(debug=True)
