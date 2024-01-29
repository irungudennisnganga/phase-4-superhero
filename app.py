#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate
from flask_restful import Api,Resource
from models import db, Hero,HeroPower,Power

app = Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

class HeroData(Resource):
    def get(self):
         
        response_dict=[data.to_dict() for data in Hero.query.all()]
        
        response=make_response(
            (response_dict),
            200
        )
        return response
   
    
api.add_resource(HeroData, '/heroes')

class HeroById(Resource):
    def get(self,id):
        data = Hero.query.filter_by(id=id).first()
        response_dict=data.to_dict()
        
        response=make_response(
            jsonify(response_dict),
            200
        )
        return response
api.add_resource(HeroById, '/heroes/<int:id>')

class PowerData(Resource):
    def get(self):
        data=[one.to_dict() for one in Power.query.all()]
        
        response=make_response(
            data,
            200
        )
        return response
    
  
    
api.add_resource(PowerData, '/powers')

class PowerById(Resource):
    def get(self,id):
        data = Power.query.filter_by(id=id).first().to_dict()

        response_data=data
        
        response=make_response(
            jsonify(data),
            200
        )
        return response
    
    def patch(self,id):
        data=Power.query.filter_by(id=id).first()
        
        for attr in request.form:
            setattr(data,attr,request.form[attr])
        db.session.add(data)    
        db.session.commit()

        response_dict=data.to_dict()
        response=make_response(
            response_dict,
            200
        )
        return response
    
api.add_resource(PowerById, '/powers/<int:id>')  
class NewHeroPower(Resource):
    def post(self):
        new_record=HeroPower(
            strength=request.form['strength'],
            hero_id=request.form['hero_id'],
            power_id=request.form['power_id'],
            
        )
        db.session.add(new_record)
        db.session.commit()

        response_dict=new_record.to_dict()

        response=make_response(
            response_dict,
            201
        )
        return response
    
api.add_resource(NewHeroPower, '/hero_powers')   

 
if __name__ == '__main__':
    app.run(port=5555,debug=True)
