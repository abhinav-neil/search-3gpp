import os
from tqdm import tqdm
import string

import os

def doc2txt(src_dir='../data/downloaded_docs', dest_dir='../data/raw_docs'):
    """
    Extracts text from all .doc files in the source directory using antiword,
    and saves the extracted text in the destination directory.
    
    Args:
    - src_dir (str): Path to the source directory containing .doc files.
    - dest_dir (str): Path to the destination directory to save extracted .txt files.
    """
    
    # Ensure destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Loop through all files in the source directory
    for filename in os.listdir(src_dir):
        if filename.endswith(".doc"):
            doc_path = os.path.join(src_dir, filename)
            # Convert .doc to .txt using antiword
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(dest_dir, txt_filename)
            os.system(f"antiword {doc_path} > {txt_path}")

def preprocess_text(text):
    """
    Preprocess the extracted text.
    
    Args:
    - text (str): Extracted text from the PDF.
    
    Returns:
    - list: List of preprocessed tokens.
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize
    tokens = text.split()
    
    # Remove stop words (a simple list for demonstration; can be expanded)
    stop_words = set(["and", "the", "is", "of", "to", "in", "it", "that", "on", "for"])
    tokens = [token for token in tokens if token not in stop_words]
    
    return tokens


