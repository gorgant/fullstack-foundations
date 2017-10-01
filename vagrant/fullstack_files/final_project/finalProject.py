from flask import (Flask,  #loads the flask app functionality, #constructs urls, #renders html temlates
                  url_for, #constructs urls
                  render_template, #renders html temlates
                  request, #handles get/post requests
                  redirect, #handles redirect requests
                  flash, #allows for flash messages
                  jsonify) #enables us to configure an api endpoint for our application

#Instantiate the Flask app
app = Flask(__name__)

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with stinky cheese', 'price':'$5.99','course' :'Entree', 'id':'1', 'restaurant_id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2','restaurant_id':'1'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3','restaurant_id':'1'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4','restaurant_id':'1'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5','restaurant_id':'1'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree','id':'1'}

@app.route('/') #These "decorators" run the code below them IF the conditions are matched, in this case, if we are routed to the directories in the parenthesis
@app.route('/restaurant/')
def showRestaurants():
  restaurantsList = restaurants #WILL NEED TO BE UPDATED TO A DATABASE QUERY
  #add a loop to pull out each restaurant, count the nubmer of menu items, and push that value into the restaurant page
  return render_template('restaurants.html', restaurant_list=restaurantsList)

@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():
  if request.method == 'POST':
    if request.form['name']:
      newRestaurantName = request.form['name']
      flash("You just created a new restaurant called %s" %(newRestaurantName))
    return redirect(url_for('showRestaurants'))
  else:
    return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
  oldRestaurantName = restaurant_id
  newRestaurantName = oldRestaurantName
  if request.method == 'POST':
    if request.form['name']:
      newRestaurantName = request.form['name']
      flash("You just changed the restaurant name from %s to %s" %(oldRestaurantName,newRestaurantName))
    return redirect(url_for('showRestaurants'))
  else:
    return render_template('editrestaurant.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
  restaurantName = restaurant_id
  if request.method == 'POST':
    flash("You just deleted the restaurant: %s" %(restaurantName))
    return redirect(url_for('showRestaurants'))
  else:
    return render_template('deleterestaurant.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
  menuItems = items #WILL NEED TO BE UPDATED TO A DATABASE QUERY
  return render_template('menu.html', restaurant_id = restaurant_id, menu_item_list=menuItems)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
  if request.method == 'POST':
    newMenuItemName = request.form['name']
    newMenuItemDescription = request.form['description']
    newMenuItemPrice = request.form['price']
    newMenuItemCourse = request.form['course']
    #ADD CODE HERE TO APPLY TO DATABASE
    flash("You just added a new menu item %s" %(newMenuItemName))
    return redirect(url_for('showMenu', restaurant_id=restaurant_id))
  else:
    return render_template('newmenuitem.html', restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
  menuItem = item #will need to pull the actual menu item from the DB using the menu_id
  oldMenuItemName = menuItem['name']
  oldMenuItemCourse = menuItem['course'].lower()
  if request.method == 'POST':
    if request.form['name']:
      newMenuItemName = request.form['name']
      flash("You just changed the restaurant name from %s to %s" %(oldMenuItemName, newMenuItemName))
    if request.form['description']:
      newMenuItemDescription = request.form['description']
      flash("You just changed the description for menu item %s" %(oldMenuItemName))
    if request.form['price']:
      newMenuItemPrice = request.form['price']
      flash("You just changed the price for menu item %s" %(oldMenuItemName))
    if (request.form['course'] != oldMenuItemCourse):
      newMenuItemCourse = request.form['course']
      flash("You just changed the course for menu item %s" %(oldMenuItemName))
    return redirect(url_for('showMenu', restaurant_id=restaurant_id))
  else:
    return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_item=menuItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
  menuItem = item #WILL NEED TO PULL from the DB using the menu_id
  menuItemName = menuItem['name']
  if request.method == 'POST':
    flash("You just deleted the menu item: %s" %(menuItemName))
    return redirect(url_for('showMenu',restaurant_id=restaurant_id))
  else:
    return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_item=menuItem) #CAN REMOVE RESATUARANT ID WHEN USING ACTUAL MENUITEM OBJECT

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True #Flask operation that automatically restarts server when change detected
  app.run(host = '0.0.0.0', port = 7997) #By default, server is only accessible from host machine, but b/c we are using vagrant, this sets the server to public

