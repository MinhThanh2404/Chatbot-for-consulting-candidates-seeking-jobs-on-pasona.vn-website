from flask import Blueprint, request
from controllers.dashboard_controller import getData

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/getData', methods=['POST']) #collect data from database
def getData_route():
    return getData()