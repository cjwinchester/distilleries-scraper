"""
import json (from the standard library) to encode json output: https://docs.python.org/2/library/json.html

json would be useful if, say, you want to use the data in a web page or something
"""
import json

"""
import requests to fetch pages: http://docs.python-requests.org/en/master/
"""
import requests

"""
and beautiful soup to parse the html: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
"""
from bs4 import BeautifulSoup



"""
assign the URL we want to scrape to the variable 'BASE_URL'
"""
BASE_URL = "https://www.ttb.gov/foia/xls/frl-spirits-producers-and-bottlers.htm"



"""
Use requests to get 'BASE_URL' and fetch the page contents, assigning the request data to the variable 'r'
'verify=False' means we're going to ignore the SSL certificate error that pops up on this page b/c good work federal government
"""
r = requests.get(BASE_URL, verify=False)



"""
The request data has the property "text" -- the same code you'd see if you viewed source in the browser -- which you can access using dot notation

to see what other properties are available, you can use the dir() method: print(dir(r))

then parse the text with BeautifulSoup(); assign the parsed HTML to the variable 'soup'
"""
soup = BeautifulSoup(r.text, "html.parser")



"""
if you view the source code on the target page, there are two tables on the page. we want the second one with all the data.

the beautifulsoup method find_all() returns a list of matching elements. lists in python are zero-indexed, and you can access list items by numeric index with brackets -- which means that [1] returns the second item in the list

so: within 'soup' (the parsed HTML tree), find all the tables, then grab the second one and assign it to the variable 'target_table'
"""
target_table = soup.find_all('table')[1]



"""
within the target table, get a list of all the rows using the same method
"""
trs = target_table.find_all('tr')



"""
our goal is a list of dictionaries, so first we'll make an empty list to append records to
"""
distilleries = []



"""
ok so now loop through the table rows, from the second ([1]) row down to the second-to-last row ([-1]), skipping the header row and the mostly empty row at the end

(more on list slicing: http://www.dotnetperls.com/slice-python)

everything inside the loop is indented -- this is important!

"""
for row in trs[1:-1]:
    """
    within each row, get a list of the table cells (td)
    """
    col = row.find_all('td')
    
    
    
    """
    ... which you can access by numeric index and assign to variables
    
    .text gets the text from the HTML node
    
    .strip() removes whitespace
    
    (we're skipping the zip-four and the county b/c they're hot garb)
    
    """
    license_no = col[0].text.strip()
    owner = col[1].text.strip()
    operating_name = col[2].text.strip()
    address = col[3].text.strip()
    city = col[4].text.strip()
    state = col[5].text.strip()
    zip_code = col[6].text.strip()
    
    
    
    """
    create an empty dictionary for this record and assign to the variable 'liquor_dict'
    """
    liquor_dict = {}
    
    
    
    """
    populate the dictionary with data from this row -- yes, we're still in a loop iteration here! -- assigning key/value pairs using brackets
    """
    liquor_dict['license'] = license_no
    liquor_dict['owner'] = owner
    liquor_dict['address'] = address
    liquor_dict['city'] = city
    liquor_dict['state'] = state
    
    
    
    """
    use some conditional logic to see whether there's any text in the "operating name" cell -- we only want to add it to the dictionary if there's something there
    
    see: http://www.tutorialspoint.com/python/python_if_else.htm
    """
    if operating_name != "":
        liquor_dict['operating_name'] = operating_name



    """
    append the dictionary to the master list
    """
    distilleries.append(liquor_dict)
    
    
    
"""
k now we're out of the loop

last thing: open a blank json file, encode the list as json, write to file
"""

with open("distilleries.json", "wb") as liquor_list:
    liquor_json = json.dumps(distilleries) 
    liquor_list.write(liquor_json)
