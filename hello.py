from flask import Flask, render_template


#create a flask Instance
app = Flask(__name__)

# Create a route decorator
@app.route('/')

#def index():
 #   return"<h1> hello world</>"

def index():
    return render_template("index.html")

#localhost:5000/user/john
@app.route('/user/<name>')
    
def user(name):
    return"<h1> hello world, i am {}</>".format(name)

#Invalid url
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500
