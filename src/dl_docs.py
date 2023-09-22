# Description: Downloads zip files from the 3GPP website.

# Imports
import os
import requests
import argparse
from bs4 import BeautifulSoup
from tqdm import tqdm

def extract_zip_urls(base_url, max_files=None):
    '''
    Extracts zip file links from the 3GPP website.
    Inputs:
        base_url: Base URL of the 3GPP website to scrape.
        max_files: Maximum number of files to download.
    Returns:
        file_urls: List of zip file links.
    '''
    # Fetch the content of the base webpage
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract links to the Rel-<X> folders
    rel_urls = [a['href'] for a in soup.find_all('a', href=True) if 'Rel-' in a['href']]

    file_urls = []

    # For each Rel-<X> link, extract <XX>_series links
    for rel_url in tqdm(rel_urls):
        response = requests.get(rel_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        series_urls = [a['href'] for a in soup.find_all('a', href=True) if '_series' in a['href']]
        
        # For each <XX>_series link, extract zip file links
        for series_url in series_urls:
            response = requests.get(series_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            zip_urls = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.zip')]
            file_urls.extend(zip_urls)
            
            # Check if the number of file_urls exceeds max_files
            if max_files is not None and len(file_urls) >= max_files:
                file_urls = file_urls[:max_files]
                print(f'Max file limit reached. Returning {max_files} files.')
                return file_urls

    return file_urls

def download_docs_from_3gpp(url, save_dir='../downloaded_files', max_files=None):
    '''
    Downloads zip files from the 3GPP website.
    Inputs:
        url: Base URL of the 3GPP website to scrape.
        save_dir: Directory to save the downloaded zip files.
        max_files: Maximum number of files to download.
    '''
    # Extract all zip file links
    zip_urls = extract_zip_urls(url, max_files)

    # Create the directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)

    # Download and save each zip file
    print(f"Downloading {len(zip_urls)} files...")
    for url in tqdm(zip_urls):
        # Get the zip file content
        zip_response = requests.get(url, stream=True)
       
        # Determine the filename
        filename = os.path.join(save_dir, url.split('/')[-1])
       
        # Save the zip file
        with open(filename, 'wb') as file:
            for chunk in zip_response.iter_content(chunk_size=8192):
                file.write(chunk)
        
    print("done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download zip files from 3GPP website.")
    parser.add_argument("--url", default="https://www.3gpp.org/ftp/Specs/2023-06", help="Base URL of the 3GPP website to scrape.")
    parser.add_argument("--save_dir", default="../downloaded_files", help="Directory to save the downloaded zip files.")
    parser.add_argument("--max_files", default=None, type=int, help="Maximum number of files to download.")
    
    args = parser.parse_args()

    download_docs_from_3gpp(args.url, args.save_dir, args.max_files)
    print(f"files downloaded to {args.save_dir}/")
