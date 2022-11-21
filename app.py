from flask import Flask
from flask_cors import CORS
import controller

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(controller.bp)
    return app

if __name__=='__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
