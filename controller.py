from flask import Blueprint, request
from typing import Optional
#import service
#import model

bp = Blueprint('main', __name__, url_prefix='')

@bp.route('/hello', methods=['GET'])
def hello():
    return 'Hello World!'
