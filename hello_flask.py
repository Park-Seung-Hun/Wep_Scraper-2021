from flask import Flask

app = Flask("HelloScrapper")

@app.route("/") # "/"에 접속하면 home이라는 함수 실행 -> /는 root이다.
def home():
    return "Hello! welcome to hi"

@app.route("/contact") # "/contact" 에 접속하면 contact 함수 실행
def contact():
    return "Contact me!"
    
app.run(host="127.0.0.1")