# webscraper-2021
 
### 📖 webscraper-2021
> 파이썬을 이용하여 구직 사이트의 정보를 추출하는 프로그램을 구현해보았다. <br>


### ✅ 사용 Skills
  1. HTML
  2. Python
  3. Flask


### 📕 주요 기능
<img src="https://github.com/Park-Seung-Hun/webScraper-2021/blob/main/resultImage/result.gif" width="800">

#### `main.py`
> 웹 스크래퍼의 모든 기능을 통제하기 위해 만든 파일로 3가지 주요 함수를 담당한다. [main 코드 보러가기](https://github.com/Park-Seung-Hun/webScraper-2021/blob/main/main.py)<br>

 1. app.route("/")
```python
@app.route("/") # root에 접속하면 home이라는 함수 실행
def home():
    return render_template("main.html") # main.html을 렌더링
```
 2. app.route("/report")
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

 3. app.route("/export")
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
#### `scrapper.py`
#### `exporter.py`
#### `template`

### 📘 추가할 기능


### 📙 출처
[노마드 코더](https://nomadcoders.co/)<br>



