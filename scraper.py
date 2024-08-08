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
