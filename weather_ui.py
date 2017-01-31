"""
This is a separate module for computing the UI for the weather.
"""

# Global variables - color choices for background based on weather and time of day
LT_BLUE = '#73C5FB'
DK_BLUE = '#2E3261'
LT_BLUE_GREY = '#81AFD6'
DK_BLUE_GREY = '#334A66'
LT_GREY = '#A4A3C7'
DK_GREY = '#41414F'

# Font colors
LT_FONT = '#AEDFFF'
DK_FONT = '#151A2B'

def get_icon(description):
    """Get the icon based on the description of the weather."""
    if 'rain' in description:
        return 'rain'
    if 'thunder' in description:
        return 'thunder'
    if 'snow' in description:
        return 'snow'
    if 'sun' in description:
        return 'sun'
    if 'cloud' in description:
        return 'cloud'
    return 'cloud'  # default value

def get_bg_color(icon, is_day):
    """Get the background color based on the weather and the time of day."""
    if icon in ('rain', 'thunder', 'snow'):
        # Weather's terrible, so show grey.
        if is_day:
            return LT_GREY
        return DK_GREY
    if icon == 'cloud':
        # Weather's aight, so show a bluer grey.
        if is_day:
            return LT_BLUE_GREY
        return DK_BLUE_GREY
    # default values (normal weather, show blue!)
    if is_day:
        return LT_BLUE
    return DK_BLUE

def get_font_color(is_day):
    """Get the font color based on time of day."""
    if is_day:
        return DK_FONT  # darker color
    return LT_FONT  # lighter color

def is_jacket(icon, temp):
    """Determine whether to bring a jacket based on the weather and the temperature."""
    is_bad_weather = icon in ('rain', 'thunder', 'snow')
    is_cold = temp <= 65.0
    return is_bad_weather or is_cold

def get_ui_attributes(description, is_day, temp):
    """Get the UI attributes based on the weather parameters."""
    icon = get_icon(description)
    return {
        'bg_color': get_bg_color(icon, is_day),
        'font_color': get_font_color(is_day),
        'icon': icon,
        'is_jacket': is_jacket(icon, temp),
    }

if __name__ == '__main__':
    # Testing the code above!
    # Note that this won't run when the module is imported,
    # only when we decide to run it using python weather_ui.py

    assert get_icon("It's raining today!") == 'rain'
    assert get_icon("I love the sun!") == 'sun'
    assert get_icon("I have no clue what the weather's like") == 'cloud'

    assert get_bg_color('snow', True) == LT_GREY
    assert get_bg_color('thunder', False) == DK_GREY
    assert get_bg_color('cloud', True) == LT_BLUE_GREY
    assert get_bg_color('cloud', False) == DK_BLUE_GREY
    assert get_bg_color('sun', True) == LT_BLUE
    assert get_bg_color('sun', False) == DK_BLUE

    assert get_font_color(True) == DK_FONT
    assert get_font_color(False) == LT_FONT

    assert is_jacket('rain', 97.0)
    assert is_jacket('sun', 60)
    assert not is_jacket('cloud', 70.0)

    print "All tests passed!"
