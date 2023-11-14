import json


def list_insteresting_stats():
    # Load catalog_full.jsonld
    with open("catalog_full.jsonld", "r", encoding="utf-8") as f:
        # Load json LD data
        stat_list = json.load(f)
        # Only keep objects with key "http://www.w3.org/ns/dcat#accessURL"
        selected = [x for x in stat_list if "http://www.w3.org/ns/dcat#accessURL" in x]

        # Print value of key "http://purl.org/dc/terms/title" for the first 100 objects
        for i in range(500):
            print(selected[i]["http://purl.org/dc/terms/title"])
            if "http://purl.org/dc/terms/publisher" in selected[i]:
                publisher_id = selected[i]["http://purl.org/dc/terms/publisher"]["@id"]
                # Find the entry in stat_list with the same id as publisher_id
                for entry in stat_list:
                    if entry["@id"] == publisher_id:
                        print(entry["http://purl.org/dc/terms/title"])
                        break
            # search for key "http://dcat-ap.de/def/dcatde/licenseAttributionByText"
            if "http://dcat-ap.de/def/dcatde/licenseAttributionByText" in selected[i]:
                print(selected[i]["http://dcat-ap.de/def/dcatde/licenseAttributionByText"])
        
        

if __name__ == "__main__":
    list_insteresting_stats()