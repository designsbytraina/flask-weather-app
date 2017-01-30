# Import Flask
from flask import Flask, render_template, request
# Import requests library to make call to Accuweather API
import requests
# Import os to get API_KEY which was sourced from secrets.sh
import os

# Always keep your API Key secret
# Source secrets.sh file to use API Key
API_KEY = os.environ['ACCUWEATHER_API_KEY']

# "__name__" is a special Python variable for the name of the current module
# Flask wants to know this to know what any imported things are relative to.
app = Flask(__name__)

# Global variables - color choices for background based on weather and time of day
LT_BLUE = '#73C5FB'
DK_BLUE = '#2E3261'
LT_BLUE_GREY = '#81AFD6'
DK_BLUE_GREY = '#334A66'
LT_GREY = '#A4A3C7'
DK_GREY = '#41414F'


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
def get_results():
    """Make request to Accuweather API and display result to user."""

    # Get form variable from request
    location = request.args.get('location')

    # Define payload for query to Accuweather API
    payload = {'apikey':API_KEY, 'q':location, 'language':'en-us'}

    # Make request to Accuweather API and save response object
    # See http://developer.accuweather.com/accuweather-locations-api/apis/get/locations/v1/search
    # for documentation.
    response = requests.get('http://dataservice.accuweather.com/locations/v1/search',
                                 params=payload)

    # Process the JSON object into a list of results
    response_list = response.json()

    if not response_list:
        # TODO: render invalid UI due to empty response
        pass

    # Process JSON returned and index into object's Key attribute
    location_key = response_list[0]['Key']

    # Make call to helper function to get the current weather with location_key
    weather_obj = get_current_weather(location_key)

    if not weather_obj:
        # TODO: render invalid UI due to empty response
        pass

    # Make call to helper function to get the UI parameters to render
    ui_attributes = get_ui_attributes(
        weather_obj['description'].lower(),
        weather_obj['is_day'],
        weather_obj['temp'],
    )

    # Render template with the data we collected on the frontend
    return render_template(
        'results.html',
        color=ui_attributes['bg_color'],
        font=ui_attributes['font_color'],
        icon=ui_attributes['icon'],
        is_jacket=ui_attributes['is_jacket'],
        location=location,
        description=weather_obj['description'],
        temp=weather_obj['temp'],
    )

def get_ui_attributes(description, is_day, temp):
    """Get the UI attributes based on the weather parameters."""

    # Logic to support background color changes, icon choice needed on frontend
    if temp <= 80.0:

        # If the lowered description includes the word rain, choose rain icon
        if 'rain' in description:
            icon = 'rain'

            # Define is_jacket, which will trigger a message on the frontend based on T/F
            is_jacket = True

            # Define background colors based on time of day
            if is_day:
                bg_color = LT_GREY
            else:
                bg_color = DK_GREY

        # If the lowered description includes the word thunder, choose thunder icon
        elif 'thunder' in description:
            icon = 'thunder'

            # Define is_jacket, which will trigger a message on the frontend based on T/F
            is_jacket = True

            # Define background colors based on time of day
            if is_day:
                bg_color = LT_GREY
            else:
                bg_color = DK_GREY

        # If the lowered description includes the word snow, choose snow icon
        elif 'snow' in description:
            icon = 'snow'
            bg_color = LT_GREY

            # Define is_jacket, which will trigger a message on the frontend based on T/F
            is_jacket = True

        # If the lowered description includes the word sun, choose sun icon
        elif 'sun' in description:
            icon = 'sun'

            # Define background colors based on time of day
            if is_day:
                bg_color = LT_BLUE
            else:
                bg_color = DK_BLUE

            # Determine is the weather is sunny and cold and define is_jacket
            if temp <= 65.0:
                is_jacket = True
            else:
                is_jacket = False

        elif 'cloud' in description:
            icon = 'cloud'

            # Define background colors based on time of day
            if is_day:
                bg_color = LT_BLUE_GREY
            else:
                bg_color = DK_BLUE_GREY

            # Determine is the weather is cloudy and cold and define is_jacket
            if temp <= 65.0:
                is_jacket = True
            else:
                is_jacket = False

        else:
            icon = 'cloud'
            is_jacket = False

            # Define background colors based on time of day
            if is_day:
                bg_color = LT_BLUE
            else:
                bg_color = DK_BLUE

    # Else if the temp is above 80F
    else:
        icon = 'cloud'
        is_jacket = False

        # Define background colors based on time of day
        if is_day:
            bg_color = LT_BLUE
        else:
            bg_color = DK_BLUE

    # Define font colors based on time of day to give better contrast
    if is_day:
        font_color = '#151A2B'
    else:
        font_color = '#AEDFFF'

    return {
        'bg_color': bg_color,
        'font_color': font_color,
        'icon': icon,
        'is_jacket': is_jacket,
    }

# Process weather data using the location key passed as a parameter from show_results()
def get_current_weather(location):
    """Get current weather data."""

    # Define payload for query to Accuweather API
    payload = {'apikey': API_KEY}

    # Make request to Current Conditions API and save response object
    # See http://developer.accuweather.com/accuweather-current-conditions-api/apis/get/currentconditions/v1/%7BlocationKey%7D
    # for documentation.
    response = requests.get('http://dataservice.accuweather.com/currentconditions/v1/%s' % location,
                                 params=payload)

    # Process the JSON object into a list of results
    response_list = response.json()

    # If there is no weather data, we return an empty dictionary
    if not response_list:
        return {}

    # Define variables using attributes returned in response
    description = response_list[0]['WeatherText']
    is_daytime = response_list[0]['IsDayTime']
    curr_temp = response_list[0]['Temperature']['Imperial']['Value']

    # Return these to the caller
    return {
        'is_day': is_daytime,
        'description': description,
        'temp': curr_temp,
    }


##################################
# Necessary to get application running.
if __name__ == '__main__':
    # debug=True gives us error messages in the browser and also "reloads" our
    # web app if we change the code.
    app.run(debug=True, host='0.0.0.0', port=5000)
