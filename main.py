import requests
from bs4 import BeautifulSoup


indeed_result = requests.get("https://www.indeed.com/jobs?as_and=python&limit=50")

indeed_soup = BeautifulSoup(indeed_result.text,"html.parser") # html 분석을 위한 BeautifulSoup

pagination= indeed_soup.find("ul",{"class":"pagination-list"}) # class명이 pagination을 찾기 위한 변수

links = pagination.find_all('a') # 모든 a 태그를 찾기 위한 변수

pages=[]
for link in links[:-1]: # next를 제와한 페이지 숫자를 가져온다.
    pages.append(int(link.string)) # text를 추출하여 숫자로 바꾸어 저장한다.

max_page = pages[-1]
