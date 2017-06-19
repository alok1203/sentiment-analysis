from flask import Flask, redirect, render_template, request, url_for

import helpers
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "").lstrip("@")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name,50)

    # TODO
    if tweets==None:
        return redirect(url_for("index"))
    obj=Analyzer()
    positive, negative, neutral =0,0,0
    for tweet in tweets:
        tokeni=nltk.tokenize.TweetTokenizer()
        tokens=tokeni.tokenize(tweet)
        score=0
        for word in tokens:
            score=obj.analyze(word)+score
        if score>0:
            positive=positive+1
        elif score < 0:
            negative=negative+1
        else:
            neutral=neutral+1
    
    

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
app.run()
