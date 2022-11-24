from email.policy import default
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime




#create a flask Instance
app = Flask(__name__)
#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secret key
app.config['SECRET_KEY'] = "You aren't supposed to know this key"

# Initialize database
db =SQLAlchemy(app)

# Create model for database
class Users(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200), nullable=False)
    email= db.Column(db.String(120), nullable=False, unique= True)
    date_added= db.Column(db.DateTime, default= datetime.utcnow)

    # Create a string
    def __repr__(self):
        return '<Name %r>' % self.name 

class Userform(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


#Create a form
class Namerform(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")



# Create a route decorator
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user/add', methods=['POST','GET'])
def add_user():
    name= None
    form=Userform()
    if form.validate_on_submit():
        user= Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user =Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name= form.name.data
        form.name.data=''
        form.email.data=''
        flash('User Added Successfully!')
    our_users = Users.query.order_by(Users.date_added)

    return render_template("add_user.html",
    form =form,
    name=name,
    our_users=our_users)

#def index():
 #   return"<h1> hello world</>"



#localhost:5000/user/john
@app.route('/user/<name>')
    
def user(name):
    return render_template("user.html",user_name=name)

#Invalid url
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500


#route for name page
@app.route('/name', methods =['GET','POST'])
def name():
    name = None
    form = Namerform()
    #Validate form
    if form.validate_on_submit():
        name= form.name.data
        form.name.data =''
        flash("Form Submitted Sucessfully")

    return render_template('name.html',
    name=name,
    form=form)