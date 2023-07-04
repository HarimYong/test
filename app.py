from flask import Flask, render_template
# from car_ocr import recognition

app = Flask(__name__)

@app.route("/")
def index():
    # result=recognition('test.png')
    return render_template('./index.html')


