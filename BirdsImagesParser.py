import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import cv2
from urllib.request import urlopen
import numpy as np

def generateWorkingUrls(path=os.path.join(os.getcwd(), "urllist")):
    with open(path) as sourcefile:
        for line in sourcefile:
            yield line

def cachePage(url):
    # TODO someday.
    # Avoid downloading
    # Same pages multiple times
    ...

def getPage(url):
    rawPage = requests.get(url)
    wrappedPage = BeautifulSoup(rawPage.content, 'html.parser')
    # For now - hardcoded version
    targetDivs = wrappedPage.find_all("div", {"class": "photos_only"})
    for pageFrame in targetDivs:
        # HARDCODED
        aTag = pageFrame.contents[0]
        imgTag = aTag.contents[0]
        smallImageUrl = imgTag.get('data-src')
        smallImageUrl = smallImageUrl.replace("mp.jpg","fronpic1.jpg")
        aName = pageFrame.contents[2]
        birdUrlShort = aTag.get('href')
        # birdUrl = urljoin(url, birdUrlShort)
        birdUrl = urljoin(url,smallImageUrl)
        # print(f"{aName},{birdUrl}")
        yield aName, birdUrl

def takeBirdImage(birdImageUrl):
    resp = urlopen(birdImageUrl)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def saveBird(birdName, birdImage):
    imageItself = takeBirdImage(birdImage)
    cv2.imwrite(os.path.join(os.getcwd(),"scrapped",birdName+".jpg"), imageItself)

for url in generateWorkingUrls():
    for birdName, birdImgUrl in getPage(url):
        saveBird(birdName, birdImgUrl)
