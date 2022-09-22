# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)



"""
============================= Database Connection and Table ================================
"""

# 

class Employee(db.Model):
    eid = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    pancard = db.Column(db.String(100), nullable = False)
    doj = db.Column(db.String(100), nullable = False)
    education = db.Column(db.String(100), nullable = False)
    year = db.Column(db.Integer, nullable = False)
    technology = db.Column(db.String(80), nullable = False)
    gender = db.Column(db.String(80), nullable = False)
    salary = db.Column(db.Integer, nullable = False)
    address = db.Column(db.String(100), nullable = False)
    mobile_no = db.Column(db.String(12), nullable = False)
    email_id = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(100), nullable = False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __init__(self, name, pancard, doj, education, year, technology, gender, salary, address, mobile_no, email_id, password):
        # self.eid = eid eid,
        self.name = name
        self.pancard = pancard
        self.doj = doj
        self.education = education
        self.year = year
        self.technology = technology
        self.gender = gender
        self.salary = salary
        self.address = address
        self.mobile_no = mobile_no
        self.email_id = email_id
        self.password = password

    def __repr__(self):
        return f'<Employee {self.name}>'


# Product Schema
class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('eid', 'name', 'pancard', 'doj', 'education', 'year', 'technology', 'gender', 'salary', 'address', 'mobile_no', 'email_id')

# Init Schema
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)


"""
===============================================================================================================
"""
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
def hello_world():
    return 'Hello World'

# create a employee record
@app.route('/signup',methods=['POST'])
def esignup():
    # load edata
    # take current datetime, add this field in edata
    # pass data to service layer
    # send response to UI
    # eid = request.json['eid']
    name = request.json['name']
    pancard = request.json['pancard']
    doj = request.json['doj']
    education = request.json['education']
    year = request.json['year']
    technology = request.json['technology']
    gender = request.json['gender']
    salary = request.json['salary']
    address = request.json['address']
    mobile_no = request.json['mobile_no']
    email_id = request.json['email_id']
    password = request.json['password']

    new_employee = Employee(name, pancard, doj, education, year, technology, gender, salary, address, mobile_no, email_id, password)
    db.session.add(new_employee)
    db.session.commit()

    print(employee_schema.jsonify(new_employee))
    return employee_schema.jsonify(new_employee)

# Get all Employees
@app.route('/employee', methods=["GET"])
def get_employees():
    all_employees = Employee.query.all()
    result = employees_schema.dump(all_employees)
    return jsonify(result)

# Get particular Employee data
@app.route("/employee/<id>", methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    return employee_schema.jsonify(employee)

# update a employee details
@app.route('/employee/<id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)

    name = request.json['name']
    pancard = request.json['pancard']
    doj = request.json['doj']
    education = request.json['education']
    year = request.json['year']
    technology = request.json['technology']
    gender = request.json['gender']
    salary = request.json['salary']
    address = request.json['address']
    mobile_no = request.json['mobile_no']
    email_id = request.json['email_id']
    password = request.json['password']

    employee.name = name
    employee.pancard = pancard
    employee.doj = doj
    employee.education = education
    employee.year = year
    employee.technology = technology
    employee.gender = gender
    employee.salary = salary
    employee.address = address
    employee.mobile_no = mobile_no
    employee.email_id = email_id
    employee.password = password

    db.session.commit()

    print(employee_schema.jsonify(employee))
    return employee_schema.jsonify(employee)


# delete a employee details
@app.route('/employee/<id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    db.session.delete(employee)
    db.session.commit()
    return employee_schema.jsonify(employee)



# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug =True)  # host,portno