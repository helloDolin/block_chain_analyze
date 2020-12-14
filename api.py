import flask
from spider_price import format_response_data
import ast
from flask_cors import CORS

server =  flask.Flask(__name__)
CORS(server, resources=r'*')

@server.route('/get_data', methods=['post'])
def api_data():
    data_bytes = flask.request.get_data()
    data_str = str(data_bytes, encoding='utf-8')
    data_dic = None
    if len(data_str) > 0:
        data_dic = ast.literal_eval(data_str)
    data = format_response_data(req=data_dic)
    return data

server.run(port=8020, debug=True, host='127.0.0.1')