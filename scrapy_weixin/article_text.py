import requests
from bs4 import BeautifulSoup
url = 'https://mp.weixin.qq.com/s?timestamp=1517535962&src=3&ver=1&signature=TIBY8-bpJg9S9ACkU-DjKIkUkKPkPIXcfIkqMEWq85mzNBoIY4OVV*BuvuUjLZ97VDlVs0UpueWuhWu9fr8R3P3WASQ0NNwgRwyEShkZN260PNFgKUHSCEQEhuWfyN-7abfHf-I3ZnawucO8p8wtCuFHYtYeZrwCbyGWS3BoeCU='
page = requests.get(url)
page.encoding = 'utf-8'
soup = BeautifulSoup(str(page.text), 'html.parser')
article = soup.select('.rich_media_content')[0].text
print(article)