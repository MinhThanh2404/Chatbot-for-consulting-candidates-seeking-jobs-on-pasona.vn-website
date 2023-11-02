# import libraries
import numpy as np
import spacy
import spacy.cli
from nltk.corpus import wordnet
from transformers import BertForSequenceClassification, BertTokenizer
import torch
from datetime import datetime as dt
import calendar
import nltk
from nltk.stem import WordNetLemmatizer
from services.topic_identifier import Topic
from number_parser import parse_ordinal
from dateutil import parser
import traceback


class Query():
    def condition_check(word, filteredDictionary, adj, verb):
        """
        - combine and check the condition to classify the upcoming case and return True/False
        - params: 
            + word (str): word to check the condition
            + filteredDictionary (dict) : dictionary of POSTagger and words that are not in the list of stopwords
            + adj (boolean): def-False; consider if combining adj check (True: included, False: not included)
            + verb (boolean): like adj
        - return: True/False
        """
        con = False

        n_check = (filteredDictionary[word] == "NN") | (
            filteredDictionary[word] == "NNP") | (filteredDictionary[word] == "NNS")  # noun
        j_check = (filteredDictionary[word] == "JJ")  # adj
        v_check = (filteredDictionary[word] == "VV")  # verb

        if (adj and verb):
            con = (n_check | j_check | v_check)
        elif adj:
            con = (n_check | j_check)
        elif verb:
            con = (n_check | v_check)
        else:
            con = n_check

        return con

    def index_check(sent_list, word, jump):
        """
        - check whether the index is out of range or not, if yes -> return len(list) - 1; if not, return its position
        - params:
            + sent_list (list): list of items
            + word (str): item whose index needs checking:
            + position (int): jumps
        - return: index (int)
        """
        if sent_list.index(word)+jump > len(sent_list) - 1:
            return len(sent_list)-1
        else:
            return sent_list.index(word)+jump

    def label_fields(filteredDictionary, sent, ner, topic, position, adj=False, verb=False):
        """
        - identify 3 components:
            + cal_on: calculate on which column
            + location: replace "location" by the original location words
            + keyword: collection for where
        - params:
            + topic (str): what type of query (count, salary, list,...)
            + position (str): where to get the cal_on
            + adj (bool): default=False, if the condition includes adj --> True
            + verb (bool): default=False, if the condition includes verb --> True
            + filteredDictionary (dict): contains words and its tagger -> raw_text_clean().POStagger()
            + ner (dict): NER tagger, to replace location / date -> from raw_text_clean().grammar_vocab()
        - return: a dictionary includes cal_on (list), location (list), keyword (list), date (list)
        """

        column_name = {'position': 'job_posititon', 'opening': 'job_posititon',
                       'vacancy': 'job_posititon', 'salary': 'job_minsalary', "skill": "job_memo", "tool": "job_memo"}

        cal_on = ""
        location = []
        date = []
        # keyword = []
        open = False
        try:
            for word in sent.split():
                if word != topic:
                    con = Query.condition_check(
                        word, filteredDictionary, adj, verb)
                    if con:
                        match filteredDictionary[word]:
                            case "NN" | "NNP" | 'NNS':  # if the word is noun
                                column = ""
                                if ((sent.split()[Query.index_check(sent.split(), word, position)] == topic) | (sent.split()[Query.index_check(sent.split(), word, position-1)] == topic)) & (cal_on == ""):
                                    # check if there is the topic word near this word
                                    # find the column to count on
                                    column = column_name.get(word, '')
                                if column != "":
                                    cal_on = column  # label column
                                    continue
                                else:
                                    if 'location' in word:  # save to location list
                                        location.append(list(ner.values())[
                                                        list(ner.keys()).index(word)])
                                    elif "date" in word:  # save to date list
                                        date.append(list(ner.values())[
                                                    list(ner.keys()).index(word)])
                                    # else:
                                    #     if word not in ['job', 'role', 'position', 'count', 'volume']: #save to keyword
                                    #         keyword.append(word)

                            case "JJ" | "JJR" | "JJS":  # if the word is adj
                                # find the column to count on
                                if (sent.split()[Query.index_check(sent.split(), word, position)] == topic) | (sent.split()[Query.index_check(sent.split(), word, position+1)] == topic):
                                    # check if there is the topic word near this word
                                    cal_on = (word)
                                    continue

        except Exception as e:
            print(
                f"An error of type {type(e)} occurred: {e} {traceback.extract_tb(e.__traceback__)[0].lineno}")

        if not date:  # if the message doesnt't mention specific period of time
            match topic:
                case "amount":  # job_phase def is open
                    open = True
                case "salary":  # choose all options of job_phase
                    open = False

        return {'cal_on': cal_on, "location": location, "date": date, 'open': open}

    def generate_linked_keywords(keyword_list):
        """
        - extract, combine words in a list, and generate the "where" statements for query
        - params: keyword_list (list)
        - return: condition (str) 
        """
        keywords = []

        for i in range(len(keyword_list)):
            for j in range(i, len(keyword_list)):
                keyword = ' '.join(keyword_list[i:j+1])
                keywords.append(keyword)

        condition = ""
        if keywords:
            for i in keywords:
                condition += f'(job_posititon LIKE "% {i} %" OR job_memo LIKE  "% {i} %" OR job_industry_name LIKE "% {i} %") OR '
            condition = f'AND ({condition[:-4]})'

        return condition

    def query_format(topic, cal_on, location, date, open=True):
        """
        - write the query based on given param (select what, where)
        - params:
            + cal_on (str): select what
            + location (list): where job_area_name LIKE
            + keyword (list): where job_posititon LIKE OR job_industry_name LIKE or job_memo LIKE
            + date (list): where YEAR(job_update) = 
        - return: dict 
            + sql (str): SQL query statement
            + cal_on, location, date (str): for formatting response
        """
        select_add = ""
        groupby_add = "GROUP BY "
        orderby_add = "ORDER BY "

        # # Determine the year START
        year = ""
        if date:
            for i in date:
                time_component_dict = Time_Analyse.main_time_component(i)  # analyse time phrase

                if time_component_dict['maintime'] == 'year':
                    year = f"YEAR(DATE(job_update))={time_component_dict['timeword']} AND"
                    having = f"HAVING Year_ = {time_component_dict['timeword']}"
                elif time_component_dict['year'] != "":
                    year = f"YEAR(DATE(job_update))={time_component_dict['year']} AND"
                    having = f"HAVING Year_ = {time_component_dict['year']}"

                select_add += (
                    time_component_dict['time_component_dict']['select']+", ")
                groupby_add += (
                    time_component_dict['time_component_dict']['groupby']+", ")
                orderby_add += (
                    time_component_dict['time_component_dict']['orderby']+", ")

        if year == "":
            if dt.now().month <= 8:
                year = f"YEAR(DATE(job_update))={dt.now().year -1}"
                having = f'HAVING Year_ = {dt.now().year -1}'
            else:
                year = f"YEAR(DATE(job_update))={dt.now().year}"
                having = f'HAVING Year_ = {dt.now().year}'

        # # Determine the year END

        # # Generate location condition phrase START

        location_filter = ""

        if location:
            for i in location:
                location_filter += f'(job_area_name LIKE "% {i} %" OR job_area_summary LIKE "% {i} %") OR '
            location_filter = f'AND ({location_filter[:-4]})'

        # # Generate location condition phrase END

        # condition = Query.generate_linked_keywords(keyword) #generate keyword condition phrase

        # Add job_phase condition phrases if the message directs "open position/vacancy"
        if open:
            having += ' AND job_phase = "Open"'
            select_add += "job_phase, "
            year += ' AND job_phase = "Open" '

        # if there is no requirement on groupby and orderby, 2 vari turn into white space
        if (groupby_add[groupby_add.find("BY")+2:] == " "):
            groupby_add = ""
            having = ""
        if (orderby_add[orderby_add.find("BY")+2:] == " "):
            orderby_add = ""
            having = ""

        # # Complete the query statement START
        match topic:
            case "amount":
                if cal_on == "":
                    cal_on = "job_posititon"
                sql = f'SELECT {select_add}COUNT({cal_on}) as Count_ FROM jobs WHERE is_hide = 0 AND {year} {location_filter} {groupby_add[:-2]} {having} {orderby_add[:-2]}'
            case "salary":
                match cal_on:
                    case "average" | "standard" | "":
                        cal_on = 'average'
                        sql = f'SELECT {select_add}CONCAT(ROUND(AVG(job_minsalary)), " - ", ROUND(AVG(job_maxsalary)), " (USD)") AS AVG_ FROM jobs WHERE is_hide = 0 AND {year} AND job_minsalary <> 0 AND job_maxsalary <> 0 {location_filter} {groupby_add[:-2]} {having} {orderby_add[:-2]}'
                        # print(sql)
                        # breakpoint()
                    case 'highest' if cal_on in wordnet.sysnets('highest').lemmas():
                        sql = f'SELECT {select_add}CONCAT(ROUND(AVG(job_minsalary)), " - ", ROUND(AVG(job_maxsalary)), " (USD)") AS AVG_ FROM jobs WHERE is_hide = 0 AND {year} AND job_minsalary <> 0 AND job_maxsalary <> 0 {location_filter} {groupby_add[:-2]} {having} {orderby_add[:-2]} LIMIT 1'
                    case _:
                        try:
                            cal_on = "average"
                            sql = f'SELECT {select_add}CONCAT(ROUND(AVG(job_minsalary)), " - ", ROUND(AVG(job_maxsalary)), " (USD)") AS AVG_ FROM jobs WHERE is_hide = 0 AND {year} AND job_minsalary <> 0 AND job_maxsalary <> 0 {location_filter} {groupby_add[:-2]} {having} {orderby_add[:-2]}'
                        except Exception as e:
                            print(
                                f"An error of type {type(e)} occurred: {e} {traceback.extract_tb(e.__traceback__)[0].lineno}")
        # # Complere the query statement END

        return {"sql": sql, "cal_on": cal_on, "location": " and ".join(location), 'date': " ".join(date)}

    def query_sent(sent, filteredDictionary, ner_dict, topic):
        """
        - identify the components and generate the SQL query based on the topic of the message
        - params:
            + sent (str): clean sentences
            + filteredDictionary (dict): contains words and their tagger -> raw_text_clean().POStagger()
            + ner (dict): NER tagger, to replace location / date -> from raw_text_clean().grammar_vocab()
        - return: query (str)
        """
        try:
            if topic == "amount":
                fields = Query.label_fields(
                    filteredDictionary, sent, ner_dict, topic, -2)
                query = Query.query_format(
                    topic, fields['cal_on'], fields['location'], fields['date'], fields['open'])

            elif topic == "salary":
                fields = Query.label_fields(
                    filteredDictionary, sent, ner_dict, topic, 1, True)
                query = Query.query_format(
                    topic, fields['cal_on'], fields['location'], fields['date'], fields['open'])

            return query
        except Exception as e:
            print(
                f"An error of type {type(e)} occurred: {e} {traceback.extract_tb(e.__traceback__)[0].lineno}")


class Time_Analyse():  # analyze time phrase
    def convert_month(month_int):
        """
        - convert month from number to name
        - param: month_int (int)
        - return: month_name (str)
        """
        month_int = dt.strptime(month_int, '%m')
        month_name = month_int.strftime('%B')
        return month_name

    def identify_date_type(word):
        """
        - identify the date element is month or year
        - param: date_string (str)
        - return: type_of_date (str)
        """
        month_names = list(
            calendar.month_name[1:])  # Get a list of month names
        result_list = []

        for date_string in word.split():
            if date_string.capitalize() in month_names:  # identify month
                result_list.append(
                    {"type": "month", "word": date_string, 'converted': parser.parse(date_string).month})
            elif date_string.isdigit():
                try:
                    month_name = Time_Analyse.convert_month(date_string)
                    if month_name.capitalize() in month_names:  # identify month
                        result_list.append(
                            {"type": "month", "word": month_name, 'converted': date_string})
                except ValueError:
                    year = int(date_string)
                    if (2000 <= year) & (year <= 2100):  # identify year
                        result_list.append({"type": "year", "word": year})
        year = ""
        for i in result_list:
            for key, value in i.items():
                if value == "year":  # extract year data
                    year = i['word']

        if not result_list:
            return {'main_time': '', 'year': year}
        else:
            return {'main_time': result_list[0], 'year': year}

    def time_interpretion(select_list, groupby_list, orderby_list):
        """
        - interpret the time elements and generate queries for each part
        - params:
            + select_list (list): list of columns will be dislplayed
            + groupby_list (list): list of time periods in order
            + orderby_list (list): list of time periods in order
        - return: (dict) {"select": select_component, "groupby": groupby_component, "orderby": orderby_component}
        """
        def list_to_sent(list, common_phrase, num_omission, as_col=False):
            """
            - format the component of select/groupby/orderby components and concate these components to a string
            - params:
                + list (list): list of items to format
                + common_phrase (str): phrase to format by the items in the list
                + num_omission (int): how many characters will be cut off at the end of the final string
                + as_col (boolean): def = False, confirm if the list containing column names
            - return: dict {select_phrase, groupby_phrase, orderby_phrase}
            """
            sent = ""
            for i in list:
                if as_col:
                    sent += f"{i}{common_phrase} AS {i.capitalize()}_, "
                else:
                    sent += f"{i}{common_phrase}"
            sent = sent[:-num_omission]
            return sent

        select_component = list_to_sent(
            select_list, "(DATE(job_update))", 2, True)

        groupby_component = list_to_sent(
            groupby_list, "(DATE(job_update)), ", 2)

        orderby_component = list_to_sent(
            orderby_list, "(DATE(job_update)) DESC, ", 2)

        return {"select": select_component, "groupby": groupby_component, "orderby": orderby_component}

    def main_time_component(word):
        """
        - Identify time component and generate the query components
        - param:
            + word (str): value labeled DATE in ner dict
        - return: (dict) {maintime, timeword, time_component_dict, year}
        """
        date_ent = ['year', 'quarter', 'month', 'week']
        maintime = list(set([WordNetLemmatizer().lemmatize(n) for n in word.split(
        )]).intersection(set(date_ent)))  # get the date word in the time phrase
        if maintime:
            maintime = maintime[0]
        else:
            maintime = ""
        time_word = maintime
        if maintime == "":
            maintime = Time_Analyse.identify_date_type(
                word)['main_time']['type']
            time_word = Time_Analyse.identify_date_type(
                word)['main_time']['word']

        match maintime:
            case "year":
                return {'maintime': maintime, 'timeword': time_word, \
                        'time_component_dict': Time_Analyse.time_interpretion(['YEAR'], ['YEAR'], ['YEAR']), \
                            'year': Time_Analyse.identify_date_type(word)['year']}
            case "quarter":
                return {'maintime': maintime, 'timeword': time_word, \
                        'time_component_dict': Time_Analyse.time_interpretion(['QUARTER', 'YEAR'], ['QUARTER'], ['YEAR', 'QUARTER']), \
                            'year': Time_Analyse.identify_date_type(word)['year']}
            case "month":
                return {'maintime': maintime, 'timeword': time_word, \
                        'time_component_dict': Time_Analyse.time_interpretion(['MONTH', 'YEAR'], ['MONTH'], ['MONTH']), \
                            'year': Time_Analyse.identify_date_type(word)['year']}
            case "week":
                return {'maintime': maintime, 'timeword': time_word, \
                        'time_component_dict': Time_Analyse.time_interpretion(['WEEK', 'MONTH', 'YEAR'], ['WEEK'], ['WEEK']), \
                            'year': Time_Analyse.identify_date_type(word)['year']}

    def num_columns(time_phrase):  # incomplete
        """
        - determine elements to select displayed values in response
        - params:
            + time_phrase (str): value labeled DATE in ner dict
        - return:
            + column_where (str): the column applied filtering value
            + filtered_value (str): value to filter
            + column_display (str): column to get displaying values
            + num_start (int): from which row
            + num_length (int): to which row
        """
        prep = ['last', 'this']
        # get the date word in the time phrase
        step_word = ''.join(
            list(set(prep).intersection(set(time_phrase.split()))))
        timeword = Time_Analyse.time_interpretion(time_phrase)['timeword']
        maintime = Time_Analyse.time_interpretion(time_phrase)['maintime']
        match step_word:
            case "last":
                if (WordNetLemmatizer().lemmatize(time_phrase.split()[time_phrase.split().index(step_word)+1]) == timeword):
                    if timeword == maintime:
                        start = 1
                        count = 2
                    else:
                        start = 1
                        count = int
                else:
                    if (time_phrase.split()[time_phrase.index(step_word)+1].isdigit()) & (time_phrase.split()[time_phrase.index(step_word)+1] != timeword):
                        start = 1
                        count = int(time_phrase.split()[
                                    time_phrase.index(step_word)+1])
                    elif time_phrase.split()[time_phrase.index(step_word)+1] == timeword:
                        try:
                            start = parser.parse(timeword).month
                            count = 2
                        except Exception as e:
                            pass
            case 'this':
                if (WordNetLemmatizer().lemmatize(time_phrase.split()[time_phrase.split().index(step_word)+1]) == timeword) & (timeword == maintime):
                    start = 0
                    count1 = 1
                elif time_phrase.split()[time_phrase.index(step_word)+1] == timeword:
                    try:
                        start = parser.parse(timeword).month
                        count = 2
                    except Exception as e:
                        pass
            case _:
                for i in time_phrase.split():
                    if i == timeword:
                        if i.isdigit():
                            start = int(i)
                            count = 2
                    else:
                        try:
                            start = parser.parse(timeword).month
                            count = 2
                        except Exception as e:
                            pass
