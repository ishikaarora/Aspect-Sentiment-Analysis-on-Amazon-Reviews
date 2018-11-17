from flask import Flask, render_template, request, json

app = Flask(__name__)

@app.route('/')
def review():
    return render_template('Review.html')

if __name__=="__main__":
    app.run()
