import os
from random import random
import time
from typing import Any
import requests


BASE_URL = "https://www.govdata.de/ckan/catalog/catalog.jsonld"

def get_next_page(url: str, max_pages: int) -> str | None:
    """Gets the next url page"""
    if "?" in url:
        # Increment the number after the = in the URL by 1
        pagenum = int(url.split("=")[1]) + 1
        if pagenum > max_pages:
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
        # Wait a bit to avoid overloading the server
        time.sleep(0.2 + random())
        with open(filename, "wb") as f:
            f.write(requests.get(url).content)

def get_last_page() -> int:
    """Gets the last page number"""
    url = BASE_URL + "?page=10000000"
    r = requests.get(url)
    l: list[dict[Any, Any]] = r.json()
    # Find object with key-value pair
    #  "@type": [
    #  "http://www.w3.org/ns/hydra/core#PagedCollection"
    #],

    for obj in l:
        try:
            if "@type" in obj and "http://www.w3.org/ns/hydra/core#PagedCollection" in obj["@type"]:
                return int(obj["http://www.w3.org/ns/hydra/core#lastPage"][0]["@value"].split("?page=")[-1])
        except:
            pass
    raise Exception("Couldn't find last page")
    
def download_all_pages(base_url: str, dir: str):
    """Downloads all pages of the url until an exception occurs"""
    url: str | None = base_url
    max_page = get_last_page()
    try:
        download_url_and_safe_in_directory(url, dir)
        while url is not None:
            url = get_next_page(url, max_page) 
            if url is not None:
                download_url_and_safe_in_directory(url, dir)
    except Exception as e:
        print(e)
        return
    
if __name__ == "__main__":
    DIR = "govdata_files"
    if not os.path.isdir(DIR):
        os.mkdir(DIR)
    download_all_pages(BASE_URL, DIR)
