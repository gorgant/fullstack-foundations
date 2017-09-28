from flask import (Flask,  #loads the flask app functionality, #constructs urls, #renders html temlates
                  url_for, #constructs urls
                  render_template, #renders html temlates
                  request, #handles get/post requests
                  redirect, #handles redirect requests
                  flash, #allows for flash messages
                  jsonify) #enables us to configure an api endpoint for our application

#loads up the demo menus from the lotsofmenus.py file
import lotsofmenus

## import CRUD Operations##
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Instantiate the Flask app
app = Flask(__name__)

##Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db') #I should try running postgres and see if that works
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

#Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  menuItems = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
  return jsonify(MenuItems=[i.serialize for i in menuItems])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
  print restaurant_id
  print menu_id
  menuItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
  print menuItem.name
  return jsonify(MenuItem=menuItem.serialize)


@app.route('/') #These "decorators" run the code below them IF the conditions are matched, in this case, if we are routed to the directories in the parenthesis
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  menuItems = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
  return render_template('menu.html',restaurant = restaurant,items = menuItems)

#Processes new menu item entries
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
      newItem = MenuItem(name = request.form['name'],restaurant_id=restaurant_id)
      session.add(newItem)
      session.commit()
      flash("You just created a new menu item: %s" %request.form['name'])
      return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
      return render_template('newmenuitem.html',restaurant_id=restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
    oldMenuItemName = menuItem.name
    if request.method == 'POST':
      if request.form['name']:
        menuItem.name = request.form['name']
      session.add(menuItem)
      session.commit()
      flash("You just changed the menu item name %s to %s" %(oldMenuItemName, menuItem.name))
      return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
      return render_template('editmenuitem.html', menuItem = menuItem)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
  menuItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
  oldMenuItemName = menuItem.name
  if request.method == 'POST':
    session.delete(menuItem)
    session.commit()
    flash("You just deleted the menu item %s" %(oldMenuItemName))
    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
  else:
    return render_template('deletemenuitem.html', menuItem = menuItem)

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True #Flask operation that automatically restarts server when change detected
  app.run(host = '0.0.0.0', port = 7997) #By default, server is only accessible from host machine, but b/c we are using vagrant, this sets the server to public