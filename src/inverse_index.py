# Description: This script creates an inverse index from .txt files in a directory and indexes the files to Elasticsearch.

import os
from elasticsearch import Elasticsearch, helpers
from process_docs import preprocess_text
from pathlib import Path
import argparse

def index_files_to_es(es, idx_name='3gpp_docs', docs_dir='../data/raw_docs', reset_idx=True):
    """
    Indexes .txt files from the given directory to Elasticsearch.
    
    Args:
    - es (Elasticsearch): Elasticsearch client instance.
    - idx_name (str): Name of the Elasticsearch index.
    - docs_dir (str): Path to the directory containing .txt files.
    - reset_idx (bool): Whether to delete the index if it already exists.
    """
    if reset_idx:
        # if index exists, delete it
        if es.indices.exists(idx_name):
            es.indices.delete(idx_name)
    
    # Define a generator to yield individual documents
    def generate_bulk_data():
        for filename in os.listdir(docs_dir):
            if filename.endswith(".txt"):
                filepath = Path(docs_dir) / filename
                file_url = filepath.resolve().as_uri()
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Preprocess the content
                    processed_content = preprocess_text(content)
                    doc = {
                        "_index": idx_name,
                        "_source": {
                            "filename": filename,
                            "content": processed_content, 
                            "url": file_url
                        }
                    }
                    yield doc
    
    # Use the bulk helper function to index the data
    helpers.bulk(es, generate_bulk_data())
    
def search_docs(es, term, idx_name='3gpp_docs'):
    """
    Search for documents in the given Elasticsearch index that match the specified term.
    
    Parameters:
    - es_instance: Elasticsearch instance.
    - idx_name: Name of the Elasticsearch index.
    - term: Search term (3gpp specification).
    
    Returns:
    - List of dictionaries containing matching document filenames and their URLs.
    """
    # Perform the search
    response = es.search(index=idx_name, body={"query": {"match": {"content": term}}})
    
    # Extract matching documents and their URLs
    matching_docs = []
    for hit in response["hits"]["hits"]:
        doc_info = {
            "filename": hit["_source"]["filename"],
            "url": hit["_source"].get("url", "URL not available")  
        }
        matching_docs.append(doc_info)
    
    return matching_docs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Index .txt files to Elasticsearch.')
    parser.add_argument('--docs_dir', type=str, default='../data/raw_docs',
                        help='Path to the directory containing .txt files.')
    parser.add_argument('--idx_name', type=str, default='3gpp_docs',
                        help='Name of the Elasticsearch index.')
    parser.add_argument('--reset_idx', type=bool, default=True,
                        help='Whether to delete the index if it already exists.')
    args = parser.parse_args()
    
    # Create an Elasticsearch client instance
    es = Elasticsearch("http://localhost:9200")
    
    # Index the files to Elasticsearch
    index_files_to_es(es, args.idx_name, args.docs_dir, args.reset_idx)