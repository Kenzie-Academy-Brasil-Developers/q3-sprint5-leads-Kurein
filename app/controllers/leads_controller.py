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
    return {'msg': 'lead patched'}

def delete_lead():
    return {'msg': 'lead deleted'}