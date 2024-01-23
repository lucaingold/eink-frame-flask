from flask import Blueprint
from flask import render_template


def construct_blueprint():
    blueprint = Blueprint('home-api', __name__, url_prefix='/')

    @blueprint.route('/', methods=['GET'])
    def index():
        return render_template('home.html', title='E-Ink Frame')

    return blueprint
