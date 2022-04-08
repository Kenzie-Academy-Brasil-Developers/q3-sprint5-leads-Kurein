from flask import request, jsonify
from http import HTTPStatus
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import Query
from app.configs.database import db
from app.models.leads_model import Leads

def post_lead():
    return {'msg': 'lead created'}

def get_leads():
    base_query: Query = db.session.query(Leads)

    records = base_query.all()

    return jsonify(records), HTTPStatus.OK

def patch_lead():
    return {'msg': 'lead patched'}

def delete_lead():
    return {'msg': 'lead deleted'}