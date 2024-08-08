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
# Clone the Repository

```
git clone https://github.com/zedaes/Wallpaper-Scraper.git
cd Wallpaper-Scraper
```

# Optional (Virtual Environment)

This is **recommended** if you don't want any problems with packages.

```
python3 -m venv venv
source venv/bin/activate
```

Now install the packages in the virtual environment.

# Configure the Script

Open the script file `scraper.py` and set the `searchQuery` variable to your desired search term.
Adjust the numberOfPages variable if you want to scrape more or fewer pages.
The downloadPath variable is set to `~/pictures/wallpapers` by default. Change it to your preferred directory if needed.

# Run the Script

```
python scrape_images.py
```
This will start scraping images based on the search query and save them to the specified directory.

# Code Overview

Configuration: Set your search query, number of pages, and download path.
Fetching Pages: Loops through the specified number of pages and fetches HTML content.
Parsing HTML: Uses BeautifulSoup to find image tags with the data-src attribute.
Downloading Images: Extracts image URLs and downloads them to the specified directory.

# Example

To scrape images of "neon city" from the first 4 pages of search results and save them to `~/pictures/wallpapers`, you can use the following script:

```
import requests
from bs4 import BeautifulSoup
import os
import re

# Configuration
searchQuery = 'neon%20city'  # Your search query
numberOfPages = 4  # Number of pages to scrape
downloadPath = os.path.expanduser('~/pictures/wallpapers')  # Path to save images

# Create the download folder if it doesn't exist
if not os.path.exists(downloadPath):
    os.makedirs(downloadPath)

# Regex to extract image URLs
imageUrlPattern = re.compile(r'(https?:\/\/[^\s]+)')

# Fetch images from multiple pages
for page in range(numberOfPages):
    url = f'https://wallhaven.cc/search?q={searchQuery}&page={page+1}' 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find image URLs
    imageTags = soup.find_all('img', {'data-src': True})  # Wallhaven uses 'data-src' for lazy-loaded images

    for image in imageTags:
        imageUrl = image.get('data-src')
        if imageUrl:
            # Find the image URL from 'data-src'
            imageUrlMatch = imageUrlPattern.search(imageUrl)
            if imageUrlMatch:
                imageUrl = imageUrlMatch.group(0)
                if imageUrl.startswith('http'):
                    imageName = os.path.join(downloadPath, imageUrl.split('/')[-1])
                    imageResponse = requests.get(imageUrl, stream=True)
                    
                    # Save image
                    with open(imageName, 'wb') as file:
                        for chunk in imageResponse.iter_content(chunk_size=8192):
                            file.write(chunk)

                    print(f'Downloaded: {imageName}')

print('Finished downloading images.')
```

Contributing
Feel free to fork the repository and submit pull requests. Any contributions are welcome!

Contact
For any questions or feedback, please open an issue on GitHub.