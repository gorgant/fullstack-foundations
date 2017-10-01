from flask import (Flask,  #loads the flask app functionality, #constructs urls, #renders html temlates
                  url_for, #constructs urls
                  render_template, #renders html temlates
                  request, #handles get/post requests
                  redirect, #handles redirect requests
                  flash, #allows for flash messages
                  jsonify) #enables us to configure an api endpoint for our application

#Instantiate the Flask app
app = Flask(__name__)

# #Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]



## import CRUD Operations##
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with stinky cheese', 'price':'$5.99','course' :'Entree', 'id':'1', 'restaurant_id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2','restaurant_id':'1'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3','restaurant_id':'1'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4','restaurant_id':'1'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5','restaurant_id':'1'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree','id':'1'}

##Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db') #I should try running postgres and see if that works
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def refreshDatabase():
  session.query(Restaurant).delete()
  session.commit()
  session.query(MenuItem).delete()
  session.commit()
  print "Database Wiped!"
  import lotsofmenus #loads up the demo menus from the lotsofmenus.py file

#used for counting menu items in the restaurants.html file
def getMenuItemCount(restaurant_id):
  menuItemCount = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).count()
  return menuItemCount
app.jinja_env.globals.update(getMenuItemCount=getMenuItemCount) #adds the function above to jinja2's (the template rendere's) global variables so that it can be called in the HTML doc

@app.route('/restaurant/JSON/')
def restaurantJSON():
  restaurants = session.query(Restaurant).all()
  return jsonify(Restaurants=[i.serialize for i in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  menuItems = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
  return jsonify(MenuItems=[i.serialize for i in menuItems])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
  menuItem = session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).one()
  return jsonify(MenuItem=menuItem.serialize)

@app.route('/') #These "decorators" run the code below them IF the conditions are matched, in this case, if we are routed to the directories in the parenthesis
@app.route('/restaurant/')
def showRestaurants():
  restaurantsList = session.query(Restaurant).all()
  return render_template('restaurants.html', restaurant_list=restaurantsList)

@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
  if request.method == 'POST':
    if request.form['name']:
      newRestaurantName = request.form['name']
      newRestaurant = Restaurant(name = newRestaurantName)
      session.add(newRestaurant)
      session.commit()
      flash("You just created a new restaurant called %s" %(newRestaurantName))
    return redirect(url_for('showRestaurants'))
  else:
    return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
  oldRestaurantName = restaurant.name
  newRestaurantName = oldRestaurantName
  if request.method == 'POST':
    if request.form['name']:
      newRestaurantName = request.form['name']
      restaurant.name = newRestaurantName
      session.add(restaurant)
      session.commit()
      flash("You just changed the restaurant name from %s to %s" %(oldRestaurantName,newRestaurantName))
    return redirect(url_for('showRestaurants'))
  else:
    return render_template('editrestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
  restaurantName = restaurant.name
  if request.method == 'POST':
    session.delete(restaurant)
    session.commit()
    flash("You just deleted the restaurant: %s" %(restaurantName))
    return redirect(url_for('showRestaurants'))
  else:
    return render_template('deleterestaurant.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
  menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
  return render_template('menu.html', restaurant_id = restaurant_id, menu_items=menuItems)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
  if request.method == 'POST':
    newMenuItemName = request.form['name']
    newMenuItemDescription = request.form['description']
    newMenuItemPrice = request.form['price']
    newMenuItemCourse = request.form['course']
    print newMenuItemCourse
    newMenuItem = MenuItem(name = newMenuItemName, description = newMenuItemDescription,
                            price = newMenuItemPrice, course = newMenuItemCourse,
                            restaurant_id = restaurant_id)
    session.add(newMenuItem)
    session.commit()
    flash("You just added a new menu item %s" %(newMenuItemName))
    return redirect(url_for('showMenu', restaurant_id=restaurant_id))
  else:
    return render_template('newmenuitem.html', restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
  menuItem = session.query(MenuItem).filter_by(id = menu_id, restaurant_id = restaurant_id).one()
  oldMenuItemCourse = menuItem.course
  if request.method == 'POST':
    if request.form['name']:
      oldMenuItemName = menuItem.name
      menuItem.name = request.form['name']
      flash("You just changed the menu item name %s to %s" %(oldMenuItemName, menuItem.name))
    if request.form['description']:
      menuItem.description = request.form['description']
      flash("You just changed the description for menu item %s" %(menuItem.name))
    if request.form['price']:
      menuItem.price = request.form['price']
      flash("You just changed the price for menu item %s" %(menuItem.name))
    if (request.form['course'] != oldMenuItemCourse):
      menuItem.course = request.form['course']
      flash("You just changed the course for menu item %s" %(menuItem.name))
    session.add(menuItem)
    session.commit()
    return redirect(url_for('showMenu', restaurant_id=restaurant_id))
  else:
    return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_item=menuItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
  menuItem = session.query(MenuItem).filter_by(id = menu_id, restaurant_id = restaurant_id).one()
  menuItemName = menuItem.name
  if request.method == 'POST':
    session.delete(menuItem)
    session.commit()
    flash("You just deleted the menu item: %s" %(menuItemName))
    return redirect(url_for('showMenu',restaurant_id=restaurant_id))
  else:
    return render_template('deletemenuitem.html', restaurant_id=menuItem.restaurant_id, menu_item=menuItem) #CAN REMOVE RESATUARANT ID WHEN USING ACTUAL MENUITEM OBJECT

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True #Flask operation that automatically restarts server when change detected
  refreshDatabase() #Wipes database and imports fresh dummy data
  app.run(host = '0.0.0.0', port = 7997) #By default, server is only accessible from host machine, but b/c we are using vagrant, this sets the server to public



