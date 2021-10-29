from flask import Flask

# keknya artinya 'importing Flask class from flask module'
# double underscore means the name of the module, special shit di python
app = Flask(__name__)
# type of app :  <class 'flask.app.Flask'>

@app.route("/")
@app.route("/home")
def home():
    return "<h1>Hello, World!</h1>"

@app.route("/about")
def about():
    return "<h1>About</h1>"



if __name__ == '__main__':
    app.run(debug = True)