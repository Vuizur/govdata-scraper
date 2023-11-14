# Govdata scraper

Many German institutions send their data to https://www.govdata.de/. Unfortunately, the website does not offer a straightforward way to download the index of all data sets directly. This scraper aims to fix that and downloads the entire index into one json-ld file.

Unfortunately only a part of the datasets link to a CSV or XLSX file that is machine interpretable. And there is no standard to the data format either, so each data file will follow its own standards. (For totally automated processing you probably will need an AI something.)