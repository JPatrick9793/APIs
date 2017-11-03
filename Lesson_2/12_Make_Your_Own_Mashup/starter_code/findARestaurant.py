from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "4MKB5U3G31V4SAMFWDPH20G44OQEY31MIWAP4NTW3EIQLZVT"
foursquare_client_secret = "DMQEG0VWTW1D2JYU5QTELRJUMY1HQ0WBH1SWWM3H3GORFRTA"
defaultPic = "https://upload.wikimedia.org/wikipedia/commons/4/41/Terrible_Meme.jpg"

def findARestaurant(mealType,location):
    # 1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    lat = getGeocodeLocation(location)[0]
    lon = getGeocodeLocation(location)[1]
    # 2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    # HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?
    # client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    url = ( ('https://api.foursquare.com/v2/venues/explore?'
        'client_id={0}'
        '&client_secret={1}'
        '&v=20170801'
        '&ll={2},{3}'
        '&query={4}'
        '&limit=1').format( foursquare_client_id,
        foursquare_client_secret, lat, lon, mealType) )

    h = httplib2.Http()
    result = json.loads( h.request(url,'GET')[1] )
    # Grab the first restaurant
    restaurantName = result['response']['groups'][0]['items'][0]['venue']['name']
    # Grab restaurant address
    restaurantAddress = result['response']['groups'][0]['items'][0]['venue']['location']['formattedAddress'][0]
    try:
        restaurantAddress1 = result['response']['groups'][0]['items'][0]['venue']['location']['formattedAddress'][1]
    except Exception, e:
        restaurantAddress1 = ''
    # Grab the first image
    try: 
        firstpic = result['response']['groups'][0]['items'][0]['tips'][0]['photo']
        prefix = firstpic['prefix']
        suffix = firstpic['suffix']
        imageURL = prefix + "300x300" + suffix
    # if no image available, insert default image url
    except KeyError:
        imageURL = defaultPic
    # Return a dictionary containing the restaurant name, address, and image url
    print location + ': ' + mealType
    print ('Restaurant Name     : ' + restaurantName)
    print ('Restaurant Address  : ' + restaurantAddress
        + ', ' + restaurantAddress1)
    print ('Restaurant Image    : ' + imageURL)
    print "---"
    

if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Australia")
