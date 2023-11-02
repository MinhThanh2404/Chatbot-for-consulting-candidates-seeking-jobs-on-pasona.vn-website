import json
from flask import request, Response, session
from utils.response import create_response
from services.dashboard_service import DashboardService

def getData(): #done
    data = request.json

    try:
        time_type = data.get("Time")
        visual_name = data.get("Visual_name")

        visual_data = DashboardService.get_data(time_type, visual_name)
        
        return create_response(200, "Data received successfully", visual_data)
    
    except Exception as e:
        print(e)
        return create_response(500, "Data received unsuccessfully", e)

