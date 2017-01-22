# TODO
from flask import Flask, render_template, request, jsonify
# TODO
import requests
# TODO
import os

# Always keep your API Key secret
# Source secrets.sh file to use API Key
API_KEY = os.environ['ACCUWEATHER_API_KEY']

# "__name__" is a special Python variable for the name of the current module
# Flask wants to know this to know what any imported things are relative to.
app = Flask(__name__)


##################################
# ROUTING
##################################

# Establish routing for home page.
@app.route('/')
def index():
    """Home page."""

    # Render index page
    return render_template('index.html')


@app.route('/get-weather', methods=['GET'])
def show_results():
    """Make request to Accuweather API and display result to user."""

    # Get form variable from request
    location = request.args.get('location')

    # Define payload for query to Accuweather API
    payload = {'apikey':API_KEY, 'q':location, 'language':'en-us'}

    # Make request to Accuweather API and save response object
    response = requests.get('http://dataservice.accuweather.com/locations/v1/search', params=payload)

    # Process JSON returned and index into object's Key attribute
    location_key = response.json()[0]['Key']

    # Make call to helper function get_current_weather() with location_key
    weather_obj = get_current_weather(location_key)

    # Render template passing weather object attributes to be accessible on the frontend
    return render_template('result.html',
                            location=location,
                            sentiment=weather_obj['sentiment'],
                            temp=weather_obj['temp'],
                            is_day=weather_obj['is_day'])


# Process weather data using the location key passed as a parameter from show_results()
def get_current_weather(location):
    """Get current weather data."""

    # Define payload for query to Accuweather API
    payload = {'apikey':API_KEY}

    # Make request to Accuwether API and save response object
    response = requests.get('http://dataservice.accuweather.com/currentconditions/v1/%s' % location, params=payload)

    # Define variables using attributes returned in JSON
    sentiment = response.json()[0]['WeatherText']
    is_daytime = response.json()[0]['IsDayTime']
    curr_temp = response.json()[0]['Temperature']['Imperial']['Value']

    # Create a weather_object to pass back to show_results() for chosen attributes
    weather_obj = {'temp':curr_temp, 'is_day':is_daytime, 'sentiment':sentiment}
    
    # Return a weather_object to show_results() which has invoked get_current_weather()
    return weather_obj


##################################
# Necessary to get application to run.
if __name__ == '__main__':
    # debug=True gives us error messages in the browser and also "reloads" our
    # web app if we change the code.
    app.run(debug=True, host='0.0.0.0', port=5000)
