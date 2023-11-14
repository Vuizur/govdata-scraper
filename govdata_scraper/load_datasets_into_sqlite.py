import json
import os
import sqlite3


def recreate_database() -> sqlite3.Connection:
    SQLITE_FILE = "interesting_stats.db"
    # Delete file if it already exists
    if os.path.isfile(SQLITE_FILE):
        os.remove(SQLITE_FILE)
    # Create new file
    conn = sqlite3.connect(SQLITE_FILE)
    c = conn.cursor()
    # Create table
    c.execute(  # We use FTS5 because it supports full text search
        """
CREATE VIRTUAL TABLE dataset USING fts5(
              title,
              description,
              data_access_url
)
"""
    )
    conn.commit()
    c.close()
    return conn


def load_insteresting_stats_into_sqlite():
    # Load catalog_full.jsonld
    with open("catalog_full.jsonld", "r", encoding="utf-8") as f:
        # id_title_dict: dict[str, str] = {}
        # Load json LD data
        # stat_list = json.load(f)
        # for stat in stat_list:
        #    if "@id" in stat and "http://purl.org/dc/terms/title" in stat:
        #        id_title_dict[stat["@id"]] = stat["http://purl.org/dc/terms/title"]

        # Load json LD data
        stat_list = json.load(f)
        # unique_ids: set[str] = set()
        # for stat in stat_list:
        #    if "@id" in stat:
        #        unique_ids.add(stat["@id"])
        ## Print length of list
        # print(len(unique_ids))
        # print(len(stat_list))

        # Only keep objects with key "http://www.w3.org/ns/dcat#accessURL"
        statistics_with_data = [
            x for x in stat_list if "http://www.w3.org/ns/dcat#accessURL" in x
        ]
        # print(len(statistics_with_data))
        # quit()

        conn = recreate_database()
        c = conn.cursor()

        for stat in statistics_with_data:
            if "@id" in stat and "http://purl.org/dc/terms/title" in stat:
                # id_title_dict[stat["@id"]] = stat["http://purl.org/dc/terms/title"]
                title = None
                try:
                    title = stat["http://purl.org/dc/terms/title"][0]["@value"]
                except:
                    pass
                description = None
                try:
                    description = stat["http://purl.org/dc/terms/description"][0][
                        "@value"
                    ]
                except:
                    pass
                # XXX This currently only inserts the first data access url
                data_access_url = stat["http://www.w3.org/ns/dcat#accessURL"][0]["@id"]
                # Insert a row of data
                c.execute(
                    "INSERT INTO dataset (title, description, data_access_url) VALUES (?, ?, ?)",
                    (title, description, data_access_url),
                )

        conn.commit()
        c.close()
        conn.close()

        # Print value of key "http://purl.org/dc/terms/title" for the first 100 objects
        # for i in range(500):
        #    print(selected[i]["http://purl.org/dc/terms/title"])
        #    # if "http://purl.org/dc/terms/publisher" in selected[i]:
        #    #    publisher_id = selected[i]["http://purl.org/dc/terms/publisher"]["@id"]
        #    #    # Find the entry in stat_list with the same id as publisher_id
        #    #    for entry in stat_list:
        #    #        if entry["@id"] == publisher_id:
        #    #            print(entry["http://purl.org/dc/terms/title"])
        #    #            break
        #    # search for key "http://dcat-ap.de/def/dcatde/licenseAttributionByText"
        #    if "http://dcat-ap.de/def/dcatde/licenseAttributionByText" in selected[i]:
        #        print(
        #            selected[i]["http://dcat-ap.de/def/dcatde/licenseAttributionByText"]
        #        )


#
## Add full text search on title and description
#

if __name__ == "__main__":
    load_insteresting_stats_into_sqlite()
