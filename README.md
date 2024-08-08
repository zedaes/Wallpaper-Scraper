# Wallhaven Image Scraper

This script scrapes images from multiple pages of Wallhaven search results. It downloads images based on a search query and saves them to a specified directory.

## Features

- Scrapes multiple pages of search results from Wallhaven.
- Extracts image URLs and downloads images.
- Saves images to a specified directory.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

Install the required libraries using pip:

```
pip install requests beautifulsoup4
```

## Usage
### Clone the Repository

```
git clone https://github.com/zedaes/Wallpaper-Scraper.git
cd Wallpaper-Scraper
```

### Optional (Virtual Environment)

This is **recommended** if you don't want any problems with packages.

```
python3 -m venv venv
source venv/bin/activate
```
Then install the packages, whether or no you are using a virtual environment:
```
pip install requests beautifulsoup4
```

## Configure the Script

Open the script file `scraper.py` and set the `searchQuery` variable to your desired search term.
Adjust the `numberOfImagesToDownload` variable if you want to scrape more or fewer pages.
The `downloadPath` variable is set to `~/pictures/wallpapers` by default. Change it to your preferred directory if needed.

## Run the Script

```
python scraper.py
```
This will start scraping images based on the search query and save them to the specified directory.

## Code Overview

Configuration: Set your search query, number of pages, and download path.
Fetching Pages: Loops through the specified number of pages and fetches HTML content.
Parsing HTML: Uses BeautifulSoup to find image tags with the data-src attribute.
Downloading Images: Extracts image URLs and downloads them to the specified directory.

## Example

To scrape the first 20 images of "neon city" and save them to `~/pictures/wallpapers`, you can use the following script:

```
import requests
from bs4 import BeautifulSoup
import os
import re

searchQuery = 'neon city'
searchQuery = searchQuery.replace(' ', '%20')
numberOfImagesToDownload = 20
downloadPath = os.path.expanduser('~/pictures/wallpapers')
numberOfImagesDownloaded = 0

if not os.path.exists(downloadPath):
    os.makedirs(downloadPath)

imageUrlPattern = re.compile(r'(https?:\/\/[^\s]+)')

print(f'You are searching for "{searchQuery}".')

page = 1
while numberOfImagesDownloaded < numberOfImagesToDownload:
    url = f'https://wallhaven.cc/search?q={searchQuery}&page={page}' 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    imageTags = soup.find_all('img', {'data-src': True})
    
    if not imageTags:
        print('No more images found. Exiting.')
        break

    for image in imageTags:
        if numberOfImagesDownloaded >= numberOfImagesToDownload:
            break

        imageUrl = image.get('data-src')
        if imageUrl:
            imageUrlMatch = imageUrlPattern.search(imageUrl)
            if imageUrlMatch:
                imageUrl = imageUrlMatch.group(0)
                if imageUrl.startswith('http'):
                    imageName = os.path.join(downloadPath, imageUrl.split('/')[-1])
                    imageResponse = requests.get(imageUrl, stream=True)
                    
                    with open(imageName, 'wb') as file:
                        for chunk in imageResponse.iter_content(chunk_size=8192):
                            file.write(chunk)

                    print(f'Downloaded: {imageName} from {url}')
                    numberOfImagesDownloaded += 1

    page += 1

print(f'Finished downloading {numberOfImagesDownloaded} images.')

```

## Contributing
Feel free to fork the repository and submit pull requests. Any contributions are welcome!

## Contact
For any questions or feedback, please open an issue on GitHub.
