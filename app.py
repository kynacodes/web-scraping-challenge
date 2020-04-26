from flask import Flask, render_template
import pymongo
import scrape_mars

app = Flask(__name__)

# Setup Mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Connect to MongoDB and collection
db = client.mars_scrapes
scrapes = db.scrapes

@app.route("/scrape")
def scrape():
    mars_dict = scrape_mars.scrape()
    print(mars_dict)
    scrapes.insert_one(mars_dict)
    return "Data successfully scraped."
    
if __name__ == "__main__":
    app.run(debug=True)