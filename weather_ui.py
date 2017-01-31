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
        return '#151A2B'  # darker color
    return '#AEDFFF'  # lighter color

def is_jacket(icon, temp):
    """Determine whether to bring a jacket based on the weather and the temperature."""
    is_bad_weather = icon in ('rain', 'thunder', 'snow')
    is_cold = temp <= 80.0 or (icon in ('sun', 'cloud') and temp <= 65.0)
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
