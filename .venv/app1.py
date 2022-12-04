from collections import UserString
from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import column, Integer, String, Float
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqllite:///' + os.path.join(basedir,'plantes.db')

db = SQLAlchemy(app)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database Created!')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')
    

@app.cli.command('db_seed')
def db_seed():
    Health = Insurance(insurance_name = 'Health_Insurance',
                       insurance_group = 'Health')

    Vechicle = Insurance(insurance_name = 'Vechicle',
                         insurance_group = 'Motor')

    Civil = Insurance(insurance_name = 'Civil',
                      insurance_group = 'Other')

    db.session.add(Health)
    db.session.add(Vechicle)
    db.session.add(Civil)

    test_user = User(first_name = 'avi',
                     last_name = 'patil',
                     email = 'ok@a.com',
                     password = '12345678')
    
    db.session.add(test_user)
    db.session.commit()
    print('Database Seeded!')

    db.drop_all()
    print('Database dropped!')
   

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the Planatery App') , 200

@app.route('/not_found')
def not_found():
    return jsonify(message='The Request Not Found') , 404


@app.route('/parameter')
def Parameter():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message="Sorry " + name + ", You are not Eligible for Registration") , 401
    else:
        return jsonify(message="Welcome " + name + ",To the Registration")

@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message="Sorry " + name + ", You are not Eligible for Registration") , 401
    else:
        return jsonify(message="Welcome " + name + ",To the Registration")


@app.route('/insure',methods=['GET'])
def insure():
    insure_list = insure.query.all()
    return jsonify(data=insure_list)


# database modules
class User(db.Model):
    _tablename_ = 'users'
    id = column(Integer,Primary_key=True)
    first_name = column(String)
    last_name = column(String)
    email = column(String, unique=True)
    password = column(String)


class Insurance(db.Model):
      _tablename_ = 'Insurance_type'
      insurance_id = column(Integer, Primary_key=True)
      insurance_name = column(String)
      insurance_group = column(String)


if __name__ == '__main__':
    app.run()
