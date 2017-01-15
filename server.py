# from random import choice
from flask import Flask, render_template, request


# "__name__" is a special Python variable for the name of the current module
# Flask wants to know this to know what any imported things are relative to.
app = Flask(__name__)


@app.route('/')
def index():
    """Home page."""

    return render_template('index.html')


@app.route('/wear-this')
def show_result():
    """Tell user what to wear."""

    # Get form variable from request
    location = request.args.get('location')

    return render_template('result.html',
                            location=location)

    return 'Location object appears here!'


if __name__ == '__main__':
    # debug=True gives us error messages in the browser and also "reloads" our
    # web app if we change the code.
    app.run(debug=True, host='0.0.0.0', port=5000)
