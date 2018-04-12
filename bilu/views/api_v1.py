from quart import Blueprint, request, jsonify

from bilu import logger
from bilu.browser.exceptions import InvalidChoiceException
from bilu.chatbot.core import get_results, get_result_page

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@api_v1.route('/health', methods=['GET'])
async def health():
    return 'Everything is fine!'


@api_v1.route('/browse', methods=['POST'])
async def browse():
    data = await request.get_json()
    image = await  get_results(query=data['query'])
    return jsonify(image=image)


@api_v1.route('/access-result', methods=['POST'])
async def access_result():
    data = await request.get_json()
    try:
        image = await get_result_page(query=data['query'], choice=data['choice'])
        return jsonify(image=image)
    except InvalidChoiceException as e:
        logger.exception(e)
        return jsonify(error=str(e)), 400
