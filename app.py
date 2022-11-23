from flask import Flask
from flask_cors import CORS
import controller

# app factory function
def create_app():
    app = Flask(__name__) #create flask app
    CORS(app) #CORS setting
    app.register_blueprint(controller.bp) #register blueprint
    return app

if __name__=='__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
