from flask import Flask

# create a Flask App instance
app = Flask(__name__)

# create a Flask route
# root
@app.route('/')

# create a function
def hello_world():
    return 'Hello world'
    
