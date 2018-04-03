from quart import Blueprint, request, jsonify
from bilu.browser.duckduckgo import DuckDuckGoBrowser

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@api_v1.route('/hello', methods=['GET'])
async def hello():
    return 'Hello, World!!!'


@api_v1.route('/browse', methods=['POST'])
async def browse():
    data = await request.get_json()
    browser = DuckDuckGoBrowser(query=data['query'])
    image = browser.browse()
    return jsonify(image=image)


@api_v1.route('/access-result', methods=['POST'])
async def access_result():
    data = await request.get_json()
    browser = DuckDuckGoBrowser(query=data['query'])
    image = browser.access(data['link'])
    return jsonify(image=image)
