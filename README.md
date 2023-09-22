# 3GPP Document Search

This repository provides tools to download, process, and search through 3GPP documents via an inverted index, using Elasticsearch and Flask.

## Features

- **dl_docs.py**: Download documents (in .zip format) from a 3GPP website.
- **process_docs.py**: Scan '.doc' files, extract raw text, and save them as '.txt' files.
- **inverse_index.py**: Tokenize the '.txt' files and index them using Elasticsearch. Also contains a function to search for documents directly.
- **app.py**: A Flask application to search for a given 3GPP specification and display matching filenames along with links to view/download the files.
- **index.html**: A web page to render the search form and display the results.

## Setup

### Environment Setup

```bash
conda create -n search-3gpp python==3.11.4
conda activate search-3gpp
pip install -r requirements.txt
```

### OS Libraries

Install the following libraries on your OS:

```bash
# For antiword
sudo apt-get install antiword

# For Elasticsearch (assuming Debian/Ubuntu)
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
sudo apt-get update && sudo apt-get install elasticsearch
```

### Directory Structure

```
.
├── requirements.txt
└── src
    ├── app.py
    ├── dl_docs.py
    ├── inverse_index.py
    ├── main.ipynb
    ├── process_docs.py
    └── templates
        └── index.html
```

## Usage

1. **Download Documents**

   ```bash
   python src/dl_docs.py --base_url [BASE_URL] --save_dir [SAVE_DIR] --max_files [MAX_FILES]
   ```

2. **Process Documents**

   ```bash
   python src/process_docs.py --src_dir [SRC_DIR] --dest_dir [DEST_DIR]
   ```

3. **Start Elasticsearch Instance**

   ```bash
   sudo service elasticsearch start
   ```

4. **Index Documents to Elasticsearch**

   ```bash
   python src/inverse_index.py --idx_name [IDX_NAME] --docs_dir [DOCS_DIR] --reset_idx [RESET_IDX]
   ```

5. **Run Flask Application**

   ```bash
   python src/app.py
   ```

Visit `http://127.0.0.1:5000/` in your browser to use the application.

---