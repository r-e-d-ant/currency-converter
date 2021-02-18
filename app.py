

from flask import Flask, render_template, request, redirect, url_for
import json
from urllib.request import urlopen

app = Flask(__name__)

# ** ---------------------------------------------------- ** #

# First of All subscribe here :
# https://free.currencyconverterapi.com/free-api-key

# To get an API key then assign it to API_KEY variable below
# e.g: API_KEY = "8fhry......fhu34fsf"

# ** ---------------------------------------------------- ** #

# ***************************** #
                                #
                                #
API_KEY = "Your-API-key-Here"   #
                                #
                                #
# ***************************** #


# assign url
countries_url = "https://free.currconv.com/api/v7/countries?apiKey="+API_KEY

# open countries url and read it content
with urlopen(countries_url) as response:
    source = response.read()

# load data as string form source variable
countries_data = json.loads(source)


infos = dict() # set an empty dictionary

'''
loop in countries_data dictionary

get a key which is equal to currency Id
get a value wich is equal to currency Name

add all of them in infos empty dictionary below
currency Id as key, currency Name as value

'''

for key, value in countries_data['results'].items():
    curr_id = value['currencyId']
    curr_name = value['currencyName']
    infos[curr_id] = curr_name
    

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    result = 0
    rate = 0
    if request.method == 'POST':
        amount = request.form['amount']
        # If input is not None
        if amount:
            _from = request.form['currencyID_from']
            to = request.form['currencyID_to']
            
            convert_url = "https://free.currconv.com/api/v7/convert?q="+_from+"_"+to+"&compact=ultra&apiKey="+API_KEY
            with urlopen(convert_url) as response:
                source = response.read()
                
            convert_data = json.loads(source)
            rate = convert_data[_from+"_"+to]
            result = float(amount) * float(rate)
            
            return render_template('home.html', infos=sorted(infos.items()), rate=rate, result=result, title="Home")
        
    return render_template('home.html', infos=sorted(infos.items()), rate=rate, result=result, title="Home")



if __name__ == '__main__':
    app.run(debug=True) # debug = False, in production
