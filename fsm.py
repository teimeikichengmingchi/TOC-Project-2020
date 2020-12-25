import globals
from transitions.extensions import GraphMachine

from utils import send_text_message, send_button_message, send_multi_mess
from linebot.models import MessageEvent, TextMessage, TextSendMessage, MessageTemplateAction, TemplateSendMessage, ButtonsTemplate


#本月花費目標的目標應該無法紀錄下來，然後is_going_to_storeGoal的typeErr問題沒有處理

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    
    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "回到主選單"

    def is_going_to_spending(self, event):
        text = event.message.text
        return text.lower() == "進入記帳介面"

    def is_going_to_setGoal(self, event):
        text = event.message.text
        return text.lower() == "set goal"

    def is_going_to_storeGoal(self, event):
        text = event.message.text
        try :
            int(text)
        except ValueError:
            return False
        return True

    def is_going_to_recordSpending(self, event):
        text = event.message.text
        return text.lower() == "record spending"

    def is_going_to_tree(self, event):
        text = event.message.text
        return text.lower() == "進入植物介面"

    def on_enter_menu(self, event):
        print("I'm entering menu")
        labels = ["植物介面", "記帳介面"]
        texts = ["進入植物介面", "進入記帳介面"]
        img = "https://as2.ftcdn.net/jpg/03/24/86/31/500_F_324863161_fdTcdogpUbv7gJvpngFxKD89f50NZtD4.jpg"

        reply_token = event.reply_token
        send_button_message(reply_token, img, "主選單", "請選擇你想使用的功能", labels, texts)

    def on_enter_spending(self, event):
        print("I'm entering 記帳")
        labels = ["設定今月花費上限", "主選單"]
        texts = ["set goal", "回到主選單"]
        img = "https://as2.ftcdn.net/jpg/02/70/93/41/500_F_270934199_os6kuoM8GUAUnqgT3BzvLY4ZueAgrDGW.jpg"

        reply_token = event.reply_token
        send_button_message(reply_token, img, "記帳介面", "請選擇你想使用的功能", labels, texts)

    def on_enter_setGoal(self, event):
        print("I'm entering menu")

        reply_token = event.reply_token
        send_text_message(reply_token, "請設定您本月份目標花費上限，以純整數方式輸入\n\n格示範例：\n4000\n\n請努力讓自己的花費不要超過這個金額喔！")

    def on_enter_storeGoal(self, event):
        print("I'm entering storeGoal")

        text = event.message.text
        globals.goal = int(text)
        reply_token = event.reply_token
        message = []
        message.append(TextSendMessage(text="您的目標目前訂為" + str(globals.goal) + "元，希望您可以達到喔！加油！！"))
        message.append(
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title="回到記帳選單",
                    text="請點選按鈕以回到記帳選單",
                    actions=[
                        MessageTemplateAction(
                            label="回到記帳選單",
                            text="回選單"
                        )
                    ]
                )
            )
        )
        send_multi_mess(reply_token, message)

    def on_enter_recordSpending(self, event):
        labels = ["今日記帳", "紀錄其他日期", "回到記帳選單"]
        texts = ["set goal", "烏", "回到主選單"]
        img = "https://as1.ftcdn.net/jpg/02/00/52/34/500_F_200523424_HzY3FumKGTn10RdqjbUNBuJ6QbwFKVFS.jpg"

        reply_token = event.reply_token
        send_button_message(reply_token, img, "記帳", "請選擇你想紀錄今日還是紀錄其他天", labels, texts)


    def on_enter_tree(self, event):
        print("I'm entering 植物")
        labels = ["主選單"]
        texts = ["回到主選單"]
        img = "https://as1.ftcdn.net/jpg/01/67/72/04/500_F_167720496_af8JnHFQM7QMyIIz31tgp289ukGtlXKB.jpg"

        reply_token = event.reply_token
        send_button_message(reply_token, img, "植物界面", "請選擇你想使用的功能", labels, texts)
