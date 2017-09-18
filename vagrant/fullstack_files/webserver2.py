from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## import CRUD Operations##
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


import re #For regex functionality

##Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db') #I should try running postgres and see if that works
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def importData():
  import lotsofmenus #loads up the demo menus from the lotsofmenus.py file

def getListOfRestaurants():

  restaurantHTMLString = ""
  restaurants = session.query(Restaurant).all()
  for restaurant in restaurants:
    restaurantName = restaurant.name
    restaurantId = restaurant.id
    editLink = '''<a href="/restaurants/%s/edit">Edit</a>''' %restaurantId
    deleteLink = '''<a href="/restaurants/%s/delete">Delete</a>''' %restaurantId
    restaurantHTMLString += '''<p>%s<br>%s<br>%s</p>''' %(restaurantName, editLink,deleteLink)
    print "Restaurant Name: %s Restaurant ID: %s" %(restaurantName, restaurantId)
  return restaurantHTMLString

def insertNewRestaurant(rName):
  newRestaurant = Restaurant(name = rName)
  session.add(newRestaurant)
  session.commit()

def getRestaurantName(rId):
  restaurantObject = session.query(Restaurant).filter_by(id = rId).one()
  restaurantName = restaurantObject.name
  return restaurantName

def updateRestaurantName(rId, rNewName):
  restaurantObject = session.query(Restaurant).filter_by(id = rId).one()
  restaurantObject.name = rNewName
  session.add(restaurantObject)
  session.commit()

def deleteRestaurant(rId):
  restaurantObject = session.query(Restaurant).filter_by(id = rId).one()
  session.delete(restaurantObject)
  session.commit

def clearDatabase():
  session.query(Restaurant).delete()
  session.commit()
  session.query(MenuItem).delete()
  session.commit()

def loadHomeScreenOutput():
  output = ""
  output += "<html><body>"
  output += "%s" % getListOfRestaurants()
  output += '''<form method='GET' enctype='multipart/form-data' action='/restaurants/new'>
                <input name="addNewRestaurant" type="submit" value="Add New Restaurant">
               </form>'''
  output += "</body></html>"
  return output




class webserverHandler(BaseHTTPRequestHandler):
  def do_GET(self):

    try:
      if self.path.endswith("/restaurants"):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = loadHomeScreenOutput()
        self.wfile.write(output)
        print output
        return

      newPath = re.compile(r"/restaurants/new") #creates a match candidate for comparison against the path
      if newPath.search(self.path):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = ""
        output += "<html><body>"
        output += "<h1>Add a New Restaurant</h1>"
        output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants'>
                      <input name="newName" type="text" >
                      <input type="submit" value="Submit">
                     </form>'''
        output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants'>
                      <input name="cancelNew" type="submit" value="Cancel">
                     </form>'''
        output += "</body></html>"
        self.wfile.write(output)
        print output
        return

      editPath = re.compile(r"/restaurants/\d+/edit") #creates a match candidate for comparison against the path
      if editPath.search(self.path):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        restaurantId = re.findall(r'\d+',self.path)[0] #extracts the first number from the path
        restaurantName = getRestaurantName(restaurantId)
        output = ""
        output += "<html><body>"
        output += "<h1>Edit Restaurant Name</h1>"
        output += "<h2>Current Name: %s</h2>" %restaurantName
        output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants'>
                      <input name="editedName" type="text" >
                      <input name="theRestaurantId" type="hidden" value=%s>
                      <input type="submit" value="Submit">
                     </form>''' %restaurantId
        output += "</body></html>"
        self.wfile.write(output)
        print output
        return

      deletePath = re.compile(r"/restaurants/\d+/delete") #creates a match candidate for comparison against the path
      if deletePath.search(self.path):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        restaurantId = re.findall(r'\d+',self.path)[0] #extracts the first number from the path
        restaurantName = getRestaurantName(restaurantId)
        output = ""
        output += "<html><body>"
        output += "<h1>Delete Restaurant</h1>"
        output += "<h2>Are You Sure You Want to Delete: %s</h2>" %restaurantName
        output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants'>
                      <input name="theRestaurantId" type="hidden" value=%s>
                      <input name="executeDelete" type="submit" value="Yes">
                     </form>''' %restaurantId
        output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants'>
                      <input name="theRestaurantId" type="hidden" value=%s>
                      <input name="cancelDelete" type="submit" value="Cancel">
                     </form>''' %restaurantId
        output += "</body></html>"
        self.wfile.write(output)
        print output
        return

    except IOError:
      self.send_error(404, 'File Not Found: %s' % self.path)

  def do_POST(self):
    try:
      self.send_response(301)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      ctype, pdict = cgi.parse_header(
          self.headers.getheader('content-type'))
      if ctype == 'multipart/form-data': #confirms this is a form-data submission
        fields = cgi.parse_multipart(self.rfile, pdict) #collects all fields in a form
      if ('newName' in fields): #uses form name field from POST command in GET method above to identify form type
        formContent = fields.get('newName')
        print formContent
        insertNewRestaurant(formContent[0])
        output = loadHomeScreenOutput()
        self.wfile.write(output)
        print output
      elif ('editedName' in fields): #uses form name field from POST command in GET method above to identify form type
        formNameContent = fields.get('editedName')
        formIdContent = fields.get('theRestaurantId')
        restaurantId = formIdContent[0]
        newRestaurantName = formNameContent[0]
        print newRestaurantName + " with ID: " + restaurantId
        updateRestaurantName(restaurantId, newRestaurantName)
        output = loadHomeScreenOutput()
        self.wfile.write(output)
        print output
      elif ('executeDelete' in fields): #uses form name field from POST command in GET method above to identify form type
        formIdContent = fields.get('theRestaurantId')
        restaurantId = formIdContent[0]
        print "WARNING: " + restaurantId + " is being deleted"
        deleteRestaurant(restaurantId)
        output = loadHomeScreenOutput()
        self.wfile.write(output)
        print output
      elif ('cancelDelete' in fields): #uses form name field from POST command in GET method above to identify form type
        formIdContent = fields.get('theRestaurantId')
        restaurantId = formIdContent[0]
        print "Phew, you prevented " + restaurantId + " from being deleted"
        output = loadHomeScreenOutput()
        self.wfile.write(output)
        print output
      elif ('cancelNew' in fields): #uses form name field from POST command in GET method above to identify form type
        print "Guess you didn't want to make a new one after all"
        output = loadHomeScreenOutput()
        self.wfile.write(output)
        print output

    except:
        pass

def main():

  try:
    port = 7997
    server = HTTPServer(('',port), webserverHandler)
    print "Web server running on port %s" % port
    importData()
    server.serve_forever()


  except KeyboardInterrupt: ## hold ctrl+c to activate
    print "^C entered, stopping web server..."
    clearDatabase()
    server.socket.close()

if __name__ == '__main__':
  main()