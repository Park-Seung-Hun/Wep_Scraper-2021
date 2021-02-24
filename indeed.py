import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=25&l=%EC%84%9C%EC%9A%B8&fromage=any&limit={LIMIT}&sort=&psf=advsrch&from=advancedsearch"

# 페이지 정보 추출
def get_last_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text,"html.parser") # html 분석을 위한 BeautifulSoup
    pagination = soup.find("ul",{"class":"pagination-list"}) # class명이 pagination을 찾기 위한 변수

    links = pagination.find_all('a') # 모든 a 태그를 찾기 위한 변수
    pages=[]

    for link in links[:-1]: # next를 제와한 페이지 숫자를 가져온다.
        pages.append(int(link.string)) # text를 추출하여 숫자로 바꾸어 저장한다.

    max_page = pages[-1]
    return max_page

# 정보 추출
def extract_job(html):
        title = html.find("h2",{"class":"title"}).find("a")["title"] # 직종
       
        location = html.find("div",{"class": "recJobLoc"})["data-rc-loc"] # 지역
       
        job_id = html["data-jk"] # 지원 링크
       
        company = html.find("span", {"class": "company"}) # 지원 회사
       
        if company:
            company_anchor = company.find("a")
            if(company_anchor is not None):
                company = str(company.find("a").string)
            else:
                company = str(company.string)
            company = company.strip("\n")
        else:
            company = None

        return {'title': title, 'company': company, 'location': location, 'link': f"{URL}&vjk={job_id}"}

def extract_jobs(last_pages):
    jobs = []
    for page in range(last_pages):
        print(f"Scrapping page {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}") #status_code = 200은 request가 잘 동작한 것.
        soup = BeautifulSoup(result.text,"html.parser")
        results = soup.find_all("div",{"class":"jobsearch-SerpJobCard"}) # 일자리 정보가 들어있음
        
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_pages = get_last_pages()
    jobs = extract_jobs(last_pages)
    return jobs