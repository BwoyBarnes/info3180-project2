import requests
from bs4 import BeautifulSoup
import urlparse

def get_images(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    # soup = BeautifulSoup(open("/media/odane/UN/INFO3180/AngularTest/AmazonTestPage.html"),"html.parser")
    images = []
    
    for img in soup.findAll("img", src=True):
        images.append(img["src"])
    return images