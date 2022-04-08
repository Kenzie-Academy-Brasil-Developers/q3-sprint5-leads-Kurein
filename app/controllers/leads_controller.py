import json
from flask import request, jsonify
from http import HTTPStatus
from sqlalchemy.exc import ProgrammingError, IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Query
from app.configs.database import db
from app.models.leads_model import Leads
from datetime import datetime

def post_lead():
    data = request.get_json()
    items = data.items()
    filtered_data = dict()

    fieldnames = ["email", "phone", "name"]

    for key, value in items:
        if len(items) != 3:
            return {'error': 'key(s) missing or extra key(s) detected', 'keys needed': fieldnames}, HTTPStatus.BAD_REQUEST
        if key in fieldnames:
            filtered_data[f'{key}'] = value
        if key not in fieldnames:
           return {'error': f'key {key} unauthorized', 'keys needed': fieldnames}, HTTPStatus.BAD_REQUEST 
        if type(value) != str:
            return {'error': f'key {key} must be a string'}, HTTPStatus.BAD_REQUEST

    filtered_data["creation_date"] = datetime.now()
    filtered_data["last_visit"] = filtered_data["creation_date"]

    leads_info = Leads(**filtered_data)

    session: Session = db.session()

    session.add(leads_info)
    try:
        session.commit()
    except IntegrityError:
        return {'error': 'email or phone taken'}, HTTPStatus.CONFLICT

    return jsonify(leads_info), HTTPStatus.CREATED

def get_leads():
    base_query: Query = db.session.query(Leads)

    records = base_query.all()

    return jsonify(records), HTTPStatus.OK

def patch_lead():

    data = request.get_json()

    session: Session = db.session

    try:
        if list(data.keys())[1]:
            return {'error': 'extra key detected, only email is required'}, HTTPStatus.BAD_REQUEST
    except IndexError:
        pass
    
    try:
        record = session.query(Leads).filter(Leads.email  == data["email"]).first()
    except KeyError:
        return {'error': 'email key missing or spelled wrong'}, HTTPStatus.BAD_REQUEST
    except ProgrammingError:
        return {'error': 'email not a string'}, HTTPStatus.BAD_REQUEST

    try:
        setattr(record, "visits", record.visits + 1)
        setattr(record, "last_visit", datetime.now())
    except AttributeError:
        return {'error': 'email not found'}, HTTPStatus.NOT_FOUND

    session.commit()

    return jsonify(record), HTTPStatus.OK

def delete_lead():

    data = request.get_json()

    session: Session = db.session

    try:
        if list(data.keys())[1]:
            return {'error': 'extra key detected, only email is required'}, HTTPStatus.BAD_REQUEST
    except IndexError:
        pass
    
    try:
        record = session.query(Leads).filter(Leads.email  == data["email"]).first()
    except KeyError:
        return {'error': 'email key missing or spelled wrong'}, HTTPStatus.BAD_REQUEST
    except ProgrammingError:
        return {'error': 'email not a string'}, HTTPStatus.BAD_REQUEST

    try:
        session.delete(record)
    except UnmappedInstanceError:
        return {'error': 'email not found'}, HTTPStatus.NOT_FOUND

    session.commit()

    return "", HTTPStatus.NO_CONTENT