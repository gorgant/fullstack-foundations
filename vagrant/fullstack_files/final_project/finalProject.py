from flask import (Flask,  #loads the flask app functionality, #constructs urls, #renders html temlates
                  url_for, #constructs urls
                  render_template, #renders html temlates
                  request, #handles get/post requests
                  redirect, #handles redirect requests
                  flash, #allows for flash messages
                  jsonify) #enables us to configure an api endpoint for our application

#Instantiate the Flask app
app = Flask(__name__)

@app.route('/') #These "decorators" run the code below them IF the conditions are matched, in this case, if we are routed to the directories in the parenthesis
@app.route('/restaurants/')
def showRestaurants():
  return "This page will show all my restaurants"

@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
  return "This page will be for making a new restaurant"

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
  return "This page will be for editing restaurant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
  return "This page will be for deleting restaurant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
  return "This page is the menu for restuarant %s" % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
  return "This page is for making a new menu item for restaurant %s"  % restaurant_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
  return "This page is for editing menu item %s" % menu_id

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
  return "This page is for deleting menu item %s" % menu_id

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True #Flask operation that automatically restarts server when change detected
  app.run(host = '0.0.0.0', port = 7997) #By default, server is only accessible from host machine, but b/c we are using vagrant, this sets the server to public

