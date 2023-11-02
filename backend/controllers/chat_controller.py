import json
from flask import request, Response, session
from utils.response import create_response
from services.job_search_service import SearchService
from services.cust_info_service import CustService
from services.chat_hist_service import ChatService
from services.process_text_service import raw_text_clean
from services.topic_identifier import Topic
from services.response_service import Query
from services.verification_service import Verify
import traceback

def userInfo(): #done
    data = request.json

    try:
        name = data.get("Name")
        email = data.get("Email")
        phone = data.get("Phone")

        #email_phone_verify: check mail/phone return true/false
        #true: update, false: create
        check_dict = {'email': email, 'phone_no':phone}
        cust_id = Verify.verify_db(check_dict, "cust_info", "customer_id")

        if cust_id == "new":
            # Insert to database Start
            new_cust = CustService.create_cust(name, email, phone)
            # Insert to database End
            cust_id = new_cust.customer_id
        else:
            # Update database Start
            update_cust = CustService.update_existing_cust(cust_id, name, email, phone)
            # Udate database End
        
        return create_response(200, "Data received successfully", cust_id)

    # except :
    #     return create_response(500, "Data received unsuccessfully")
    except Exception as e:
        print(
        f"An error of type {type(e)} occurred: {e} {traceback.extract_tb(e.__traceback__)[0].lineno}")


def search(): #done, call API from laravel to display the search result
    data = request.json
    #print(data)
    try:

        cust_id = data.get("Customer_ID")
        keyword = data.get("Keyword")
        location = data.get("Location")
        industry = data.get("Industry")
        salary = data.get("Salary")
        language = data.get("Language")
        
        # Insert to database Start
        new_search = SearchService.create_search(cust_id, keyword, industry, language, location, salary)
        # Insert to database End

        return create_response(200, "Data received successfully")

    except:
        return create_response(500, "Data received unsuccessfully")

def chat(): #receive message
    data = request.json

    try:
        #get data from client
        mes = data.get("Mes")
        cust_id = data.get('Cust_id')

        # # Process input data Start # #

        # data cleaning -> return a clean text
        data_pos = raw_text_clean.clean_data(mes) #dict: dict of POStagger, string of clean sentences, dict of ner
        
        filteredDictionary = data_pos['filtered_dict'] #POSTagger dict
        ner = data_pos['ner_dict'] #NER dict
        clean_text = data_pos['clean_text'] #cleaned message

        # # Process input data End # #
        
        # # check whether the message is relevant to job topic or not
        # if check_mes == "trivia": return "sorry, your mess is beyond our knowledge."
        # else: query 

        # # Get response Start # #

        # Identify main topic of the message Start #
        topic_dict = ['amount', 'salary', 'trivia']
        topic = Topic.topic_identifier({index: value for index, value in enumerate(topic_dict)}, clean_text)['topic']
        # Identify main topic of the message End #

        #new clean text after replace the similar word in the text by the topic name (if matched)
        clean_text = Topic.topic_identifier({index: value for index, value in enumerate(topic_dict)}, clean_text)['label_sent'] 

        if topic == 'trivia': #not related to job topic
            # Insert to database Start
            new_chat = ChatService.create_chat(cust_id, mes, topic, clean_text, "sorry")
            # Insert to database End

            return create_response(200, "Data received successfully - trivia question", "Sorry, this information has not been updated in our system.")

        else: #related to job topics (amount of job positions / salary)
            #generate the SQL query
            query_sent_component = Query.query_sent(clean_text, filteredDictionary, ner, topic)

            #execute the query, format the response 
            response = ChatService.get_reponse(query_sent_component['sql'], query_sent_component['cal_on'], topic, query_sent_component['location'], query_sent_component['date'])
            
            # Insert to database Start #
            new_chat = ChatService.create_chat(cust_id, mes, topic, clean_text, response)
            # Insert to database End #
            
            return create_response(200, "Data received successfully", {'response':new_chat.response, 'chat_id':new_chat.chat_id})
        
        # # Get response END # #
    
    except:
        return create_response(500, "Data received unsuccessfully")

def rating_chatbot(): #done
    """
    - save customer rating on the overal experience with chatbot
    """
    data = request.json
    
    try:
        cust_id = data.get("Customer_ID")
        rating = data.get("Rating")

        # Insert to database Start
        new_rating = CustService.update_rating(cust_id, rating)
        # Insert to database End

        return create_response(200, "Data received successfully")
    except:
        return create_response(500, "Data received unsuccessfully")

def rating_response():
    """
    - get the rating on the given response and update on chat history
    """
    data = request.json

    try:
        chat_id = data.get('Chat_ID')
        rating = data.get('Rating')

        # Update database Start
        new_rating = ChatService.update_rating(chat_id, rating)        
        # Update database End
        return create_response(200, "Data received successfully")
    except:
        return create_response(500, "Data received unsuccessfully")

def furtherrequest():

    data = request.json

    try:

        cust_id = data.get('Cust_id')
        type_request = data.get('type_')

        result = ChatService.furtherrequest(type_request)['result']

        new_chat = ChatService.create_chat(cust_id, "button_choice", ChatService.furtherrequest(type_request)['topic'], ChatService.furtherrequest(type_request)['keyword'], '; '.join([f"{d['name_']}: {d['value_s']}" for d in result]) )
        
        return create_response(200, "Data received successfully")
    except Exception:
        return create_response(500, "Data received unsuccessfully")
