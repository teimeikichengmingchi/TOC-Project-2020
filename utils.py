import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage, MessageTemplateAction, TemplateSendMessage, ButtonsTemplate


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_multi_mess(reply_token, mess):
    line_bot_api = LineBotApi(channel_access_token)

    line_bot_api.reply_message(reply_token, mess)

    return "OK"

def send_button_message(reply_token, img, title, uptext, labels, texts):#(img, title, uptext, labels, texts):
    line_bot_api = LineBotApi(channel_access_token)
    
    acts = []
    for i, lab in enumerate(labels):
        acts.append(
            MessageTemplateAction(
                label=lab,
                text=texts[i]
            )
        )

    if img != "":
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
            thumbnail_image_url=img,
            title=title,
            text=uptext,
            actions=acts
            )
        )
    else :
        message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
            title=title,
            text=uptext,
            actions=acts
            )
        )

    line_bot_api.reply_message(reply_token, message)
    return "OK"

"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
