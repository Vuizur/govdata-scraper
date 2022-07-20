import os
from random import random
import time
import requests


BASE_URL = "https://www.govdata.de/ckan/catalog/catalog.jsonld"

def get_next_page(url: str) -> str:
    """Gets the next url page"""
    if "?" in url:
        # Increment the number after the = in the URL by 1
        pagenum = int(url.split("=")[1]) + 1
        if pagenum > 610:
            # Stop at page 610
            return None
        url = url.split("=")[0] + "=" + str(pagenum)
        return url
    else:
        return url + "?page=2"


def download_url_and_safe_in_directory(url: str, dir: str):
    #TODO: Doesn't stop yet at the end, has to be stopped manually
    """Downloads the url and saves it in the directory if the file doesn't exist"""
    
    filename = dir + "/" + url.split("/")[-1]
    # Replace ? with _ because ? is not allowed in filenames
    filename = filename.replace("?", "_")
    if not os.path.isfile(filename):
        # Wait between 3 and 5 seconds before downloading the next page
        # to avoid being blocked by the server
        time.sleep(3 + 3 * random())
        with open(filename, "wb") as f:
            f.write(requests.get(url).content)
    
def download_all_pages(url: str, dir: str):
    """Downloads all pages of the url until an exception occurs"""
    try:
        download_url_and_safe_in_directory(url, dir)
        while url is not None:
            url = get_next_page(url)
            download_url_and_safe_in_directory(url, dir)
    except Exception as e:
        print(e)
        return

if __name__ == "__main__":
    DIR = "govdata_files"
    if not os.path.isdir(DIR):
        os.mkdir(DIR)
    download_all_pages(BASE_URL, DIR)
