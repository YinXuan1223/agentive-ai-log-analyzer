from flask import Blueprint, request, jsonify
import json
from modules.parse_question import parse_question
from modules.influx_query import query_oss_data
from modules.llm_response import generate_answer

api_blueprint = Blueprint("api", __name__)

@api_blueprint.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')
    parse_result = parse_question(user_question)

    
    if not parse_result['need_data']:
        return jsonify({
            'answer': parse_result['direct_answer'],
            'used_data': []
        })

    else :
        data = query_oss_data(parse_result['tables'], parse_result['time_range'])
        print('user question:  ', user_question )
        print('data: ', data)
        answer = generate_answer(user_question, data)

        return jsonify({
            'answer': answer,
            'used_data': data
        })