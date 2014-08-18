__author__ = 'seven'
import urllib
import httplib2
import time
import xml.etree.ElementTree as ElementTree

BASE_URL = "http://localhost:8111/"
http = httplib2.Http()

# Get a list of all registered items
def showItems():
    print "\nFunction: GET, URL: %s" % (BASE_URL + "items")
    resp, content = http.request(BASE_URL + "items", "GET")
    contentXML = ElementTree.fromstring(content)
    for item in contentXML.findall("item"):
        print "Name: %s, Description: %s" \
            % (item.find("name").text, item.find("description").text)



# Create a new item: item1
item = {"name": "item1", "description": "this is the first item"}
resp, content = http.request(
                BASE_URL + "items", "POST", urllib.urlencode(item))

print "\nFunction: POST, URL: %s" % (BASE_URL + "items")
# Check whether this item is already existed according the response
if resp['status'] != '201' or not content:
    contentXML = ElementTree.fromstring(content)
    # Print the error message
    print "Error code: %s, Message: %s" \
        % (contentXML.find("code").text, contentXML.find("message").text)
    exit(0)
else:
    print content
    # Print the response of POST method, just for check
    print "URL of the newly created item: %s" % resp['content-location']

    
# Print the representation of the newly created item.
itemURL = resp['content-location']
print "\nFunction: GET, URL: %s" % itemURL
if itemURL:
    resp, content = http.request(itemURL, "GET")  
    contentXML = ElementTree.fromstring(content)
    assert isinstance(contentXML, object)
    print "Name: %s, Description: %s" \
        % (contentXML.find("name").text, contentXML.find("description").text)

# Print the list of all registered items.
showItems()

# Update the newly created item
print "\nFunction: POST, URL: %s" % itemURL
item = {"name": "item2", "description": "this is the second item"}
itemURL = BASE_URL + "items/" + item["name"]
# item["description"] = "this is an other description"
resp, content = http.request(itemURL, "PUT", urllib.urlencode(item))
if not content and resp["status"] == "204":
    #print "Response code: %s" % resp["status"]
    print "Update success!"
elif not content and resp["status"] == "201":
    print "%s doesn't exist yet, %s created." % (item["name"], item["name"])
    # Print the response of POST method, just for check
    print "URL of the newly created item: %s" % itemURL

# Print the list of all registered items.
time.sleep(1)
showItems()

# Delete the item
print "\nFunction: DELETE, URL: %s" % itemURL
resp, content = http.request(itemURL, "DELETE", urllib.urlencode(item))
if not content and resp["status"] == "204":
    #print "Response code: %s" % resp["status"]
    print "Delete success!"

time.sleep(1)
# Print the list of all registered items.
showItems()