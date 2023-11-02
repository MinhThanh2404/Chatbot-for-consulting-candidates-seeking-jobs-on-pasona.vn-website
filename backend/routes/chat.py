from flask import Blueprint, request
from controllers.chat_controller import userInfo
from controllers.chat_controller import search
from controllers.chat_controller import chat
# from controllers.chat_controller import end
from controllers.chat_controller import rating_chatbot
from controllers.chat_controller import rating_response
from controllers.chat_controller import furtherrequest

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/userInfo', methods=['POST']) #insert new user info, update current user info
def userInfo_route():
    return userInfo()


@chat_bp.route('/search', methods=['POST'])
def search_route():
    return search()

@chat_bp.route('/chat', methods=['POST']) #process message, execute the SQL query (if necessary), save chat history
def chat_route():
    return chat()

@chat_bp.route('/rating_response', methods=['POST']) #update the rating for the quality of the response
def ratingResponse_route():
    return rating_response()

@chat_bp.route('/rating_chatbot', methods=['POST']) # update rating of customer for the chatbot
def ratingChatbot_route():
    return rating_chatbot()

# @chat_bp.route('/FurtherRequest', methods = ['POST'])
# def furtherrequest_route():
#     return furtherrequest()

# @chat_bp.route('/ChartData', methods = ['POST'])
# def furtherrequest_route():
#     return furtherrequest()