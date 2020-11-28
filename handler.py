import json
import os
import requests
import traceback
import urllib.parse

ADMIN = '452549370'
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]


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
    
    def lambda_handler(event, context):
        try:
            if 'body' in event:
                body = json.loads(event['body'])
                # msgAdmin("haandler")
                #msgAdmin(body)

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
                    
                else:
                    msgAdmin("unknown lambda body")
                    msgAdmin(body)
                    
            elif 'Records' in event:
                records = event['Records']
                for r in records:
                    if 'Sns' in r:
                        sns = r['Sns']
                        message = 'Message' in sns and sns['Message']
                        subject = 'Subject' in sns and sns['Subject']
                        msgAdmin("SNS (%s):\n%s"%(subject, message))
                    else:
                        msgAdmin("unknown lambda record")
                        msgAdmin(event)
                        
            else:
                msgAdmin("unknown lambda event")
                msgAdmin(event)
            return {'statusCode': 200}
        except:
            errorAdmin()
except:
    errorAdmin()
