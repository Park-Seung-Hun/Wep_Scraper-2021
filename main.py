from flask import Flask,render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file

app = Flask("HelloScrapper")
db = {} # fake database


@app.route("/") # "/"에 접속하면 home이라는 함수 실행 -> /는 root이다.
def home():
    return render_template("main.html")

@app.route("/report") # 화면에 출력
def report():
    word = request.args.get("word")# 해당 페이지의 word 값을 받아온다.
    
    if word:
        word = word.lower() 
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
        
    return render_template("report.html", 
        searchingBy=word,
        resultNum=len(jobs),
        jobs=jobs)

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

app.run(host="127.0.0.1")
