from flask import Flask, render_template, jsonify, redirect, request
import pymongo
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb:/localhost:27017/mars_data"
mongo = PyMongo(app)

@app.route("/")
def index():
    try:
        mars_data = mongo.db.mars_data.find_one()
        return render_template('index.html', mars_data=mars_data)
    except:
        return redirect('http://localhost:5000/scrape', code=302)    

@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    # Run the scrape funtion
    mars_data_scrape = scrape_mars.scrape()
    mars_data.update(
        {},
        mars_data_scrape,
        upsert=True
    )
    return redirect('http://localhost:5000/', code=302)

@app.route('/shutdown')
def shutdown_server():
    func = request.environ.get('server.shutdown')    
    if func is None:
        raise RuntimeError('Not running with the Server')
    func()
    return 'Shutting down Flask server...'    

if __name__ == "_main_":
    app.run(debug=True)
