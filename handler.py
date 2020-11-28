from flask import Flask, render_template, request, jsonify
import json
import os
import requests
import traceback
import urllib.parse

ADMIN = '452549370'
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]


app = Flask(__name__, static_url_path='')


def errorAdmin():
    requests.get(
        "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" %
        (TOKEN, ADMIN, str(traceback.format_exc())))


def msgAdmin(message):
    try:
        message = json.dumps(message, sort_keys=True, indent=4)
    except:
        message = str(message)
    message = urllib.parse.quote(message)
    requests.get(
        "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" %
        (TOKEN, ADMIN, message))

# msgAdmin("bot running")
try:
    import main
    main.msgAdmin = msgAdmin
    main.errorAdmin = errorAdmin
    main.api.msgAdmin = msgAdmin
    main.fs.msgAdmin = msgAdmin
    
    @app.route('/', methods=['POST'])
    def lambda_handler():
        body = request.json
        try:

            if 'callback_query' in body:
                callback_query = body['callback_query']
                main.handleCallbackQuery(callback_query)

            elif 'message' in body:
                message = body['message']
                main.handleMessage(message)

            elif 'channel_post' in body:
                channel_post = body['channel_post']

            elif 'edited_channel_post' in body:
                edited_channel_post = body['edited_channel_post']

            elif 'inline_query' in body:
                inline_query = body['inline_query']

            else:
                msgAdmin("unknown handler json")
                msgAdmin(body)

            return jsonify({})
                
        except:
            errorAdmin()
            
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080, debug=True)
except:
    errorAdmin()
