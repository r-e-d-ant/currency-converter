

from flask import Flask, render_template, request, redirect, url_for
import json
from urllib.request import urlopen
import sys

app = Flask(__name__)

# ** ---------------------------------------------------- ** #

# First of All subscribe here, To get an API key :
# https://free.currencyconverterapi.com/free-api-key

# Then assign it to the API_KEY variable below
# e.g: API_KEY = "8fhry......fhu34fsf"

# ** ---------------------------------------------------- ** #

# ******************************* ####### <<<<----<-----| ############## >>>> Please <<<<<
                                  #
                                  #
API_KEY = "Add-Your-API-key-Here" ####### <<<<----<-----| ############# >>>> Don't  <<<<<
                                  #
                                  #
# ******************************* ####### <<<<----<-----| ############# >>>> Forget <<<<<<

RED = '\033[91m' # red font color in terminal
GREEN = '\033[92m' # green font color in terminal
reset = '\033[0m' # white font color in terminal

if API_KEY == "":
    print(RED, "\nSorry, This can't work without the API key", GREEN ,"\nGo get one here : https://free.currencyconverterapi.com/free-api-key \n", reset)
    sys.exit(0)


# assign url
countries_url = "https://free.currconv.com/api/v7/countries?apiKey="+API_KEY

try:
    # open countries url and read it content
    with urlopen(countries_url) as response:
        source = response.read()
except:
    print(RED, "\nSorry, something went wrong, Maybe the API key is invalid or there is no internet connection.\n", reset)
    sys.exit(0)


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
    date = datetime.utcnow()
    if request.method == 'POST':
        amount = request.form['amount']
        if amount:
            _from = request.form['currencyID_from']
            to = request.form['currencyID_to']
            convert_url = "https://free.currconv.com/api/v7/convert?q="+_from+"_"+to+"&compact=ultra&apiKey="+API_KEY
            with urlopen(convert_url) as response:
                source = response.read()
                
            convert_data = json.loads(source)
            rate = convert_data[_from+"_"+to]
            formatted_rate = "{:,}".format((round(float(rate), 2)))

            result = round(float(amount) * float(rate), 2)
            formatted_result = "{:,}".format(result)
            
            print("Amount:", str(amount), "From:", str(_from), "To:", str(to))
            print(result)
            
            return render_template('home.html', infos=sorted(infos.items()), rate=formatted_rate, result=formatted_result, date=date, title="Home")
        
    return render_template('home.html', infos=sorted(infos.items()), rate=rate, result=result, date=date, title="Home")



if __name__ == '__main__':
    app.run(debug=True) # debug = False, in production
