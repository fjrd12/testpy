from flask import Flask, Blueprint, request, abort, redirect, jsonify
from url_shortener.adapters import url_mapping
from flask_swagger_ui import get_swaggerui_blueprint
import json

url_obj = url_mapping()
bp = Blueprint("url_shortener", __name__)
url_obj = url_mapping()


def create_app():
    app = Flask(__name__)
    SWAGGER_URL = '/swagger1'
    API_URL = '/swagger1.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "URL Translation"
        }
        )
    app.register_blueprint(bp)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    return app


@bp.route("/add", methods=['POST'])
def create():
    "Create a translatable address"
    if request.method == 'POST':
        objeto = request.json
        print(objeto)
        url_obj.add(objeto['url_short'], objeto['url_long'])
    return 'Creación realizada'


@bp.route("/get", methods=['GET'])
def get():
    if request.method == 'GET':
        url_short = request.args.get('url_short')
        result = url_obj.get(url_short)
    return jsonify(result)


@bp.route("/", methods=['GET'])
@bp.route("/<path:path>")
def home(path=''):
    if len(path) == 0:
        print(request.url_root + 'swagger1/')
        resulta = redirect(request.url_root + 'swagger1/')
        return resulta
    long_url = request.url_root + path
    result = url_obj.get(long_url)
    if result is None:
        abort(404, description="The url {} does not found".format(long_url))
    else:
        url_obj.update_count(result.url_short)
        print(result.url_long)
        resulta = redirect(result.url_long)
    return resulta


@bp.route('/swagger1.json')
def swagger(path=None):
    with open('swagger1.json', 'r') as f:
        return jsonify(json.load(f))
