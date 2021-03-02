from flask import Flask,render_template

app = Flask("HelloScrapper")

@app.route("/") # "/"에 접속하면 home이라는 함수 실행 -> /는 root이다.
def home():
    return render_template("potato.html")

app.run(host="127.0.0.1")