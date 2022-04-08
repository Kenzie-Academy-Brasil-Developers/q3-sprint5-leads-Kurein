from flask import Blueprint
from app.controllers import leads_controller

bp = Blueprint("leads", __name__, url_prefix="/leads")

bp.post("")(leads_controller.post_lead)
bp.get("")(leads_controller.get_leads)
bp.patch("")(leads_controller.patch_lead)
bp.delete("")(leads_controller.delete_lead)