from flask import Flask, render_template, request
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
            results.append({
                "filename": hit["_source"]["filename"],
                "url": hit["_source"]["url"]
            })
    return render_template('index.html', results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)
