from flask import Flask,request
from flask_restful import Resource, Api
from flask_cors import CORS

from logic_and_apis.ping import Ping


app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Ping, '/tictactoe/ping/')

 
if __name__ == '__main__':
    app.run(debug=True , port = 6756)
