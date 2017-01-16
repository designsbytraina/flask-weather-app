from flask import Flask, render_template, request, jsonify
import requests
import os

# Always keep your API Key secret
API_KEY = os.environ['ACCUWEATHER_API_KEY']

# "__name__" is a special Python variable for the name of the current module
# Flask wants to know this to know what any imported things are relative to.
app = Flask(__name__)


@app.route('/')
def index():
    """Home page."""

    return render_template('index.html')


@app.route('/wear-this')

@app.route('/get-weather', methods=['GET'])
def show_results():
    """Make request to Accuweather API and display result to user."""

    # Get form variable from request
    location = request.args.get('location')

    payload = {'apikey':API_KEY, 'q':location, 'language':'en-us'}

    response = requests.get('http://dataservice.accuweather.com/locations/v1/search', params=payload)

    location_key = response.json()[0]['Key']

    weather_data = get_data(location_key)

    return render_template('result.html',
                            location=location,
                            sentiment=weather_data['sentiment'],
                            temp=weather_data['temp'],
                            is_day=weather_data['is_day'])


def get_data(location):
    """Get location data and return to user."""

    payload = {'apikey':API_KEY}

    response = requests.get('http://dataservice.accuweather.com/currentconditions/v1/%s' % location, params=payload)

    sentiment = response.json()[0]['WeatherText']

    is_daytime = response.json()[0]['IsDayTime']

    curr_temp = response.json()[0]['Temperature']['Imperial']['Value']

    weather_obj = {'temp':curr_temp, 'is_day':is_daytime, 'sentiment':sentiment}
    
    return weather_obj

    # is_jacket_needed()

# def is_jacket_needed():


##################################
if __name__ == '__main__':
    # debug=True gives us error messages in the browser and also "reloads" our
    # web app if we change the code.
    app.run(debug=True, host='0.0.0.0', port=5000)
