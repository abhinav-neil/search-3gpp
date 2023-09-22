from flask import Flask, render_template, request, send_from_directory
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    query = ""
    if request.method == 'POST':
        query = request.form['query']
        response = es.search(index='3gpp_docs', body={"query": {"match": {"content": query}}})
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
    if action == "download":
        return send_from_directory('/home/neil/docscan-philips/data/raw_docs/', filename, as_attachment=True)
    elif action == "view":
        return send_from_directory('/home/neil/docscan-philips/data/raw_docs/', filename, as_attachment=False)
    else:
        return "Invalid action", 400


if __name__ == '__main__':
    app.run(debug=True)
