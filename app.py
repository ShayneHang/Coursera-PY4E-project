from flask import Flask, render_template, request, redirect, url_for, session
from helpers.scraper import scrape_review
from foodbased_NER import recommended_food
app = Flask(__name__)


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
		review_df = scrape_review(restaurant_name)
		# session["results"] = results
		# session["query"] = query
	# 	return redirect(url_for("searchr"))
	return render_template("index.html", results=session["results"], query=session["query"])
	

@app.route("/return_result", methods=["POST", "GET"])
def return_result():
    foodlist = recommended_food(results)
    return render_template("index.html", food_list = foodlist)
    
    
if __name__ == "__main__":
    app.run(debug=True)