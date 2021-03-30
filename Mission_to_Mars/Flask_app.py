from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars_db")


@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.scrape_info.find_one()

    # Return template and data
    return render_template("index.html", mars_mission=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable
    mars_mission = mongo.db.mars_mission
    mars_data = scrape_mars.scrape()
    mars_mission.update({}, mars_data, upsert=True)

    # Update the Mongo database using update and upsert=True
    # @TODO: YOUR CODE HERE!

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
