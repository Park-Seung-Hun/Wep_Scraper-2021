import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python"

def get_last_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text,"html.parser")
    pages = soup.find("div",{"class":"s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)

def extract_job(html):
    title = html.find("h2",{"class":"mb4"}).find("a")["title"] # 직종
    
    company, location = html.find("h3",{"class":"fc-black-700"}).find_all("span",recursive=False) # recursive = False는 전부 가져오는걸 방지(첫단계만)

    print(company.get_text(strip=True), location.get_text(strip=True))
        

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text,"html.parser")
        results = soup.find_all("div",{"class":"-job"}) # 일자리 정보가 들어있음

        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs        

def get_jobs():
    last_pages = get_last_pages()
    jobs = extract_jobs(last_pages)
    return []