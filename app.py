from flask import Flask, render_template, request, redirect, url_for, session
from helpers.scraper import scrape_review
from foodbased_NER import recommended_food
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv("flask_secret_key")

app = Flask(__name__)
app.secret_key = secret_key


@app.route("/")
def index():
	return render_template("index.html")

# GET is when you want to get information
# POST is when you want to submit information
# PUT is when you want to update
# DELETE is use to delete information

@app.route("/search", methods=["POST", "GET"])
def search():
	if request.method == "POST":
		restaurant_name = request.form["restaurant_name"]
		# review_df = scrape_review(restaurant_name)
		foodlist = recommended_food(restaurant_name)
		session["foodlist"] = foodlist
		session["query"] = restaurant_name
		return redirect(url_for("search"))

	return render_template("index.html", foodlist=session["results"], restaurant_name=session["query"])
	# return render_template("index.html", food_list = foodlist, query=session["query"])
	

@app.route("/return_result", methods=["POST", "GET"])
def return_result():
    foodlist = session.get("results")

    return render_template("index.html", foodlist = foodlist)
    
    
if __name__ == "__main__":
    app.run(debug=True)