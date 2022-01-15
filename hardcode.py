from flask import Flask,jsonify, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sqlite3 as sql

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///School.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)
ma=Marshmallow(app)

class Registration(db.Model):
    __tablename__="registration"
    user_id = db.Column(db.String(50),primary_key=True)
    user_username=db.Column(db.String(50))
    user_email=db.Column(db.String(50))
    user_password=db.Column(db.String(50))

    def __init__(self,user_id,user_username,user_email,user_password):
        self.user_id=user_id
        self.user_username=user_username
        self.user_email=user_email
        self.user_password=user_password

class RegistrationSchema(ma.Schema):
    class Meta:
        fields =("user_id","user_username","user_email","user_password")
registration_schema = RegistrationSchema()
registrations_schema=RegistrationSchema(many=True)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Inventory.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)
ma=Marshmallow(app)

class Inventory(db.Model):
    __tablename__="inventory"
    rice_id = db.Column(db.String(50),primary_key=True)
    rice_name=db.Column(db.String(50))
    rice_stock=db.Column(db.String(50))
    rice_price=db.Column(db.String(50))

    def __init__(self,rice_id,rice_name,rice_stock,rice_price):
        self.rice_id=rice_id
        self.rice_name=rice_name
        self.rice_stock=rice_stock
        self.rice_price=rice_price

class InventorySchema(ma.Schema):
    class Meta:
        fields =("rice_id","rice_name","rice_stock","rice_price")
inventory_schema = InventorySchema()
inventorys_schema= InventorySchema(many=True)

@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('login'))

        #return redirect(url_for('login'))

    # show the form, it wasn't submitted
    return render_template("login.html")

@app.route('/home',methods=['POST','GET'])
def home():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        user_username = request.form['user_username']
        user_password = request.form['user_password']
        con =sql.connect("School.sqlite")
        con.row_factory =sql.Row
        cur=con.cursor()
        cur.execute(f"SELECT user_username from registration WHERE user_username='{user_username}' AND user_password = '{user_password}';")
        if not cur.fetchone():  # An empty result evaluates to False.
            print("Login failed")
            return redirect(url_for('login'))
        else:
            print("Welcome")
            con =sql.connect("Inventory.sqlite")
            con.row_factory =sql.Row
            cur=con.cursor()
            cur.execute("select * from inventory")
            rows=cur.fetchall()
            print(rows)
            return render_template("home.html",rows=rows)
    con =sql.connect("Inventory.sqlite")
    con.row_factory =sql.Row
    cur=con.cursor()
    cur.execute("select * from inventory")
    rows=cur.fetchall()
    print(rows)
    return render_template("home.html",rows=rows)
    
@app.route('/registration',methods=['POST','GET'])
def registration():
    if request.method == 'POST':
        return render_template("reg.html")
    return render_template("reg.html")

@app.route('/user',methods=['POST','GET'])
def create_user():
    if request.method == 'POST':
        try:
            user_id = request.form['user_id']
            user_username = request.form['user_username']
            user_email = request.form['user_email']
            user_password = request.form['user_password']
            with sql.connect("School.sqlite") as con:
        
                cur = con.cursor()
                cur.execute("INSERT INTO registration(user_id,user_username,user_email,user_password) VALUES (?,?,?,?)",(user_id,user_username,user_email,user_password))
                con.commit()
                
            print('try')
        except:
            con.rollback()
            
            print('except')
        finally:
            print('finally')
            con.close()
            return redirect(url_for('login'))
    return redirect(url_for('login'))

@app.route('/list', methods=["GET","POST"])
def list():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('home'))
    con =sql.connect("Inventory.sqlite")
    con.row_factory =sql.Row
    cur=con.cursor()
    cur.execute("select * from inventory")
    rows=cur.fetchall()
    print(rows)
    return render_template("inventory.html",rows=rows)

@app.route('/create',methods=['GET','POST'])
def create_inventory():
    if request.method == 'POST':
        try:
            rice_id = request.form['rice_id']
            rice_name = request.form['rice_name']
            rice_stock = request.form['rice_stock']
            rice_price = request.form['rice_price']
            with sql.connect("Inventory.sqlite") as con:
        
                cur = con.cursor()
                cur.execute("INSERT INTO inventory(rice_id,rice_name,rice_stock,rice_price) VALUES (?,?,?,?)",(rice_id,rice_name,rice_stock,rice_price))
                con.commit()
                
            print('try')
        except:
            con.rollback()
            
            print('except')
        finally:
            print('finally')
            con.close()
            #return render_template("result.html")
            return redirect(url_for('home'))
    return render_template("result.html")

@app.route('/listdelete', methods=["GET","POST"])
def listdelete():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        delete = request.form['delete']
        con = sql.connect("Inventory.sqlite")
        cur=con.cursor()
        cur.execute("delete from inventory where rice_id='{}'".format(delete))
        con.commit()
        return redirect(url_for('home'))
    con =sql.connect("Inventory.sqlite")
    con.row_factory =sql.Row
    cur=con.cursor()
    cur.execute("select * from inventory")
    rows=cur.fetchall()
    print(rows)
    return render_template("delete.html",rows=rows)

@app.route('/delete',methods=['POST'])
def delete():
    delete = request.form['delete']
    con = sql.connect("Inventory.sqlite")
    cur=con.cursor()
    cur.execute("delete from inventory where rice_id='{}'".format(delete))
    con.commit()
    return redirect(url_for('home'))

@app.route('/listsearch', methods=["GET","POST"])
def listsearch():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        #return redirect(url_for('search'))
        search = request.form['rice_id']
        con = sql.connect("Inventory.sqlite")
        cur=con.cursor()
        cur.execute("Select * from inventory where rice_id='{}'".format(search))
        con.commit()
        con.row_factory =sql.Row
        rows=cur.fetchall()
        print(rows)
        return render_template("result.html",rows=rows)
    con = sql.connect("Inventory.sqlite")
    con.row_factory =sql.Row
    cur=con.cursor()
    cur.execute("select * from inventory")
    rows=cur.fetchall()
    print(rows)
    return render_template("search.html",rows=rows)

@app.route('/search',methods=['POST','GET'])
def search():
    if request.method == 'POST':
        search = request.form['rice_id']
        con = sql.connect("Inventory.sqlite")
        cur=con.cursor()
        cur.execute("Select * from inventory where rice_id='{}'".format(search))
        con.commit()
        con.row_factory =sql.Row
        rows=cur.fetchall()
        print(rows)
        return render_template("result.html",rows=rows)

@app.route('/listsales', methods=["GET","POST"])
def listsales():
    if request.method == 'POST':
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        rice_name = request.form['rice_id']
        rice_stock = int(request.form['rice_stock'])
        
        con = sql.connect("Inventory.sqlite")
        cur=con.cursor()
        cur.execute("Select rice_stock from inventory where rice_id='{}'".format(rice_name))
        con.commit()
        con.row_factory =sql.Row
        rows=cur.fetchall()
        all_stock = int(rows[0][0])
        minus=str(all_stock - rice_stock)
        cur.execute("UPDATE inventory SET rice_stock='{}' where rice_id='{}'".format(minus,rice_name))
        con.commit()
        con = sql.connect("Inventory.sqlite")
        cur=con.cursor()
        cur.execute("Select * from inventory where rice_id='{}'".format(rice_name))
        con.commit()
        con.row_factory =sql.Row
        rows=cur.fetchall()
        print(rice_stock)
        print(rice_name)
        return render_template("sales.html",rows=rows)
    con =sql.connect("Inventory.sqlite")
    con.row_factory =sql.Row
    cur=con.cursor()
    cur.execute("select * from inventory")
    rows=cur.fetchall()
    print(rows)
    return render_template("salesoutput.html",rows=rows)

@app.route('/sales',methods=['GET','POST'])
def sales():
    if request.method == 'POST':
        rice_name = request.form['rice_id']
        rice_stock = request.form['rice_stock']
        con = sql.connect("Inventory.sqlite")
        cur=con.cursor()
        cur.execute("UPDATE inventory SET rice_stock='{}' where rice_id='{}'".format(rice_stock,rice_name))
        con.commit()
        con.row_factory =sql.Row
        rows=cur.fetchall()
        print(rice_stock)
        print(rice_name)
        return render_template("sales.html",rows=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)