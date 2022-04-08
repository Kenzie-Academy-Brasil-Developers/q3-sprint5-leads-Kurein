import json
from flask import request, jsonify
from http import HTTPStatus
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Query
from app.configs.database import db
from app.models.leads_model import Leads
from datetime import datetime

def post_lead():
    data = request.get_json()

    data["creation_date"] = datetime.now()
    data["last_visit"] = datetime.now()

    leads_info = Leads(**data)

    session: Session = db.session()

    session.add(leads_info)
    session.commit()

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

    try:
        setattr(record, "visits", record.visits + 1)
        setattr(record, "last_visit", datetime.now())
    except AttributeError:
        return {'error': 'email not found'}, HTTPStatus.NOT_FOUND

    session.commit()

    return jsonify(record)

def delete_lead():
    return {'msg': 'lead deleted'}