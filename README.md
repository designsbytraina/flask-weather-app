## Flask Weather App
This is an application built as an example for Hackbright students during the part time program.

It uses Python, Flask, HTML, and CSS to illustrate core computer science concepts like APIs and requests.

### Getting Started

First, begin by cloning this repo to your local machine:

```sh
$ git clone https://github.com/.../flask-weather-app.git <YOUR_DIR_NAME>
```

Before getting started, you will need to obtain an Accuweather API Key by [signing up here](http://developer.accuweather.com/). 

Create a file called `secrets.sh` which will live in the project root alongside `server.py` and `requirements.txt`

Within `secrets.sh` export your newly created API Key using the same format as below and save the file:

```sh
export ACCUWEATHER_API_KEY="IfThisWereTheKeyItWouldBeHere"
```

Next, create and source a virtual environment so that you can install the requirements for this project. We recommend using Python's [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) tool.

```sh
$ virtualenv env
$ source env/bin/activate
```

After sourcing your virtual environment, you can use pip to install the requirements. Please check out the [pip documentation](https://pip.pypa.io/en/stable/) for instructions on usage.

```sh
(env) $ pip install -r requirements.txt
```

You should also source your `secrets.sh` file to have access to the API Key.

```sh
(env) $ source secrets.sh
```

Once all required packages have finished installing and you have sourced your key, you will be ready to run the application locally using:

```sh
(env) $ python server.py
```

Visit [localhost:5000](http://localhost:5000/) in the browser of your choice to make weather queries to your heart's content.

#### Acknowledgements
Thank you to Hackbright Academy and its incredible students + staff 🦄

Animated Weather Icons c/o [Josh Bader](http://codepen.io/joshbader/) 💯

This application is for learning purposes only. All code is reproducible and shareable.
