# webscraper-2021
 
### 📖 webscraper-2021
> 파이썬을 이용하여 구직 사이트의 정보를 추출하는 프로그램을 구현해보았다. <br>


### ✅ 사용 Skills
  1. HTML
  2. Python
  3. Flask


### 📕 주요 기능
1. 스크래핑
<img src="https://github.com/Park-Seung-Hun/webScraper-2021/blob/main/resultImage/%EC%9B%B9%EC%8A%A4%ED%81%AC%EB%9E%98%ED%95%91.gif" width="80%">
2. 추출 
<img src="https://github.com/Park-Seung-Hun/webScraper-2021/blob/main/resultImage/%EC%B6%94%EC%B6%9C.gif" width="80%">
<img src="https://github.com/Park-Seung-Hun/webScraper-2021/blob/main/resultImage/2021-03-17.png" width="80%">

[csv 파일 보러가기](https://github.com/Park-Seung-Hun/webScraper-2021/blob/main/resultImage/flask%20(1).csv)
#### `main.py`
> 웹 스크래퍼의 모든 기능을 통제하기 위해 만든 파일로 3가지 주요 함수를 담당한다. [main 코드 보러가기](https://github.com/Park-Seung-Hun/webScraper-2021/blob/main/main.py)<br>

 1. app.route("/") : 기본 화면(main.html을 웹 상에 띄운다.)
```python
@app.route("/") # root에 접속하면 home이라는 함수 실행
def home():
    return render_template("main.html") # main.html을 렌더링
```
 2. app.route("/report") : 검색어를 입력하여 웹 스크래핑.
 ```python
 @app.route("/report")
 def report():
    word = request.args.get("word") # 해당 페이지의 word 값을 받아온다.
    
    if word: 
        word = word.lower() # 입력되는 검색어를 모두 소문자로 바꾼다.
        existingJobs = db.get(word) # 임시 database를 설정
        if existingJobs: # 이미 검색했던 검색어 일때
            jobs = existingJobs
        else: # 검색한 적이 없을 때
            jobs = get_jobs(word) # scrapper의 get_jobs 함수 실행
            db[word] = jobs
    else: # root로 돌아간다.
        return redirect("/")
        
    return render_template("report.html", 
        searchingBy=word,
        resultNum=len(jobs),
        jobs=jobs) # report.html 을 렌더링 하는데, 받은 변수들을 같이 보낸다.
 ```

 3. app.route("/export") : 스크래핑한 정보를 excel로 추출.
```python
@app.route("/export")
def export():
    try:
        word = request.args.get('word')
        
        if not word:
            raise Exception()

        word = word.lower()
        existingJobs = db.get(word)

        if not existingJobs:
            raise Exception()

        save_to_file(existingJobs,word)
        file_name=f"{word}.csv"
        return send_file(file_name,
            mimetype='text/csv',
            as_attachment=True,
            attachment_filename = file_name)
    except:
        return redirect("/")
```
#### `scrapper.py` [scrapper 코드 보러가기](https://github.com/Park-Seung-Hun/webScraper-2021/blob/main/scrapper.py)
```python
# 1. 페이지의 최대 수를 받아온다.
def get_last_pages(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text,"html.parser")
    pages = soup.find("div",{"class":"s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)

# 3. 전부 불러온 일자리 정보들을 각각의 세분화된 정보로 나눈다.(제목,회사,지역,지원 링크)
def extract_job(html):
    title = html.find("h2",{"class":"mb4"}).find("a")["title"] # 직종
    company, location = html.find("h3",{"class":"fc-black-700"}).find_all("span",recursive=False) # recursive = False는 전부 가져오는걸 방지(첫단계만)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id= html["data-jobid"]

    return {'title': title,'company': company,'location': location, 'apply_link': f"https://stackoverflow.com/jobs/{job_id}"}

# 2. 페이지마다 일자리 정보들을 전부 불러온다. 
def extract_jobs(last_page,url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: page: {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text,"html.parser")
        results = soup.find_all("div",{"class":"-job"}) # 일자리 정보가 들어있음

        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs        

# main에서 입력한 검색어를 통해 페이지 정보 스크래핑 후 정보를 세분화해 다시 main으로 return.
def get_jobs(word):
    URL = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_pages(URL)
    jobs = extract_jobs(last_page,URL)
    return jobs
```
#### `exporter.py` [exporter 코드 보러가기](https://github.com/Park-Seung-Hun/webScraper-2021/blob/main/exporter.py)
```python
# main에서 스크래핑하고 세분화한 직업 정보와 파일명을 받아와 .csv파일로 저장한다.
def save_to_file(jobs,word):
    file = open(f"{word}.csv", encoding='UTF-8',mode="w", newline='') # mode w 쓰기, r 읽기
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "link"])
    
    for job in jobs:
        writer.writerow(list(job.values()))
    return 
```

#### `report.html`
```html
<!--정보를 받아와 html 파일에 나타낸다.-->
 <body>
    <h1>Search Result</h1>
    <h3>Found {{resultNum}} results for: {{searchingBy}}</h3>
    <a href="/export?word={{searchingBy}}">Export to CSV</a>
    <section>
      <h4>Title</h4>
      <h4>Company</h4>
      <h4>Location</h4>
      <h4>Link</h4>

      {% for job in jobs %}
      <span>{{job.title}}</span>
      <span>{{job.company}}</span>
      <span>{{job.location}}</span>
      <a href="{{job.apply_link}}" target="blank">Apply</a>
      {% endfor %}
    </section>
  </body>
```

### 📘 추가할 기능


### 📙 출처
[노마드 코더](https://nomadcoders.co/)<br>



