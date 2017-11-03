from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request, redirect, url_for
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = '4MKB5U3G31V4SAMFWDPH20G44OQEY31MIWAP4NTW3EIQLZVT'
foursquare_client_secret = 'DMQEG0VWTW1D2JYU5QTELRJUMY1HQ0WBH1SWWM3H3GORFRTA'
google_api_key = 'AIzaSyAZVjzOXK-uCS4g1Bg7tgxEMCK76rGA9Tg'

engine = create_engine('sqlite:///restaruants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  #YOUR CODE HERE
  if request.method == 'POST':
  	#
  	location = request.args.get('location')
  	mealType = request.args.get('mealType')
  	RestaurantJSON = findARestaurant(mealType, location)
  	newRestaurant = Restaurant(
  		restaurant_name=RestaurantJSON['name'],
  		restaurant_address = RestaurantJSON['address'],
  		restaurant_image = RestaurantJSON['image'] 
  		)
  	session.add(newRestaurant)
  	session.commit()
  	return jsonify(Restaurant = newRestaurant.serialize)

  if request.method == 'GET':
    #RETURN ALL RESTAURANTS
    allRestaurants = session.query(Restaurant).all()
    return jsonify( Restaurant = [i.serialize for i in allRestaurants])


    
@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  #YOUR CODE HERE
  restaurant = session.query(Restaurant).filter_by(id = id).one()

  if request.method == 'GET':
  	# RETURN RESTAURANT WITH SPECIFIED ID
  	return jsonify(restaurant.serialize)

  if request.method == 'PUT':
  	#check to see if name param was entered
  	if request.args.get('name'):
  		newName = request.args.get('name')
  		restaurant.restaurant_name = newName
  	# check to see if location param was entered
  	if request.args.get('location'):
  		newLocation = request.args.get('location')
  		restaurant.restaurant_address = newLocation
  	# check to see if image param was enterd
  	if request.args.get('image'):
  		newImage = request.args.get('image')
  		restaurant.restaurant_image = newImage
  	session.add(restaurant)
  	session.commit()
  	return jsonify(restaurant.serialize)

  if request.method == 'DELETE':
  	session.delete(restaurant)
  	session.commit()
  	return redirect(url_for('all_restaurants_handler'))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
