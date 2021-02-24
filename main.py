import requests
from bs4 import BeautifulSoup


indeed_result = requests.get("https://www.indeed.com/jobs?as_and=python&limit=50")

indeed_soup = BeautifulSoup(indeed_result.text,"html.parser") # html 분석을 위한 BeautifulSoup

pagination= indeed_soup.find("ul",{"class":"pagination-list"}) # class명이 pagination을 찾기 위한 변수

pages = pagination.find_all('a') # 모든 a 태그를 찾기 위한 변수

spans=[]
for page in pages: # a안에 span을 몯  가져온다.
    spans.append(page.find("span"))
print(spans[0:-1])