import globals
from transitions.extensions import GraphMachine

from datetime import date

from utils import send_text_message, send_button_message, send_multi_mess, send_yes_no_message
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
        return text.lower() == "go to spending"

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

    def is_going_to_setSpendingMenu(self, event):
        text = event.message.text
        return text.lower() == "record spending"

    def is_going_to_setSpending(self, event):
        text = event.message.text
        if not globals.setTodayFlag:
            if text.lower() == "set today":
                globals.setToday = True
            else:
                globals.setToday = False
        globals.setTodayFlag = True
        return text.lower() == "set today" or text.lower() == "set other days" or text.lower() == "back to set spending"

    def is_going_to_storeSpending(self, event):
        data = (event.message.text).split(" ")
        if (globals.setToday and not len(data) == 2) or (not globals.setToday and not len(data) == 5):
            send_text_message(event.reply_token, "輸入的數目不正確，請確認輸入是否有錯")
            return False
        for i, ele in enumerate(data):
            try :
                int(ele)
            except ValueError:
                if (i == 0 and len(data) == 2) or  (i == 3 and len(data) == 5):
                    continue
                send_text_message(event.reply_token, "內容含有非正整數")
                return False
        if len(data) == 5:
            try:
                date(int(data[0]), int(data[1]), int(data[2]))
            except ValueError:
                send_text_message(event.reply_token, "您輸入的日期不存在")
                return False
        return True

    def is_going_to_tree(self, event):
        text = event.message.text
        return text.lower() == "go to tree"

    def on_enter_menu(self, event):
        print("I'm entering menu")
        labels = ["植物介面", "記帳介面"]
        texts = ["go to tree", "go to spending"]
        img = "https://as2.ftcdn.net/jpg/03/24/86/31/500_F_324863161_fdTcdogpUbv7gJvpngFxKD89f50NZtD4.jpg"

        reply_token = event.reply_token
        send_button_message(reply_token, img, "主選單", "請選擇你想使用的功能", labels, texts)

    def on_enter_spending(self, event):
        globals.setTodayFlag = False
        labels = ["設定今月花費上限", "記帳", "主選單"]
        texts = ["set goal", "record spending", "回到主選單"]
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

    def on_enter_setSpendingMenu(self, event):
        labels = ["今日記帳", "紀錄其他日期", "回到記帳選單"]
        texts = ["set today", "set other days", "go to spending"]
        img = "https://as1.ftcdn.net/jpg/02/00/52/34/500_F_200523424_HzY3FumKGTn10RdqjbUNBuJ6QbwFKVFS.jpg"

        reply_token = event.reply_token
        send_button_message(reply_token, img, "記帳", "請選擇你想紀錄今日還是紀錄其他天", labels, texts)

    def on_enter_setSpending(self, event):

        reply_token = event.reply_token
        if globals.setToday:
            if event.message.text == "back to set spending":
                send_text_message(reply_token, f"請輸入下一筆計帳資料\n\n格示範例：\n娛樂 200")
            else :
                send_text_message(reply_token, f"請輸入您今日({globals.year}/{globals.month}/{globals.day})的花費金額，前為項目分類，後為花費，中間請空一格並一次輸入一行就好\n\n格示範例：\n娛樂 200\n\n代表要在「娛樂」這個項目紀錄200元的花費")
        else:
            if event.message.text == "back to set spending":
                send_text_message(reply_token, "請輸入下一筆計帳資料\n\n格示範例：\n2020 6 28 娛樂 200")
            else :
                send_text_message(reply_token, "請輸入您欲紀錄的日期、項目及花費金額，前為年、月、日，中間為項目分類，後為花費。中間請空一格並一次輸入一行就好\n\n格示範例：\n2020 6 28 娛樂 200\n\n代表要在2020年6月28日的「娛樂」這個項目紀錄200元的花費")

    def on_enter_storeSpending(self, event):

        reply_token = event.reply_token
        data = (event.message.text).split(" ")
        if globals.setToday:
            globals.spending[0].append(globals.year)
            globals.spending[1].append(globals.month)
            globals.spending[2].append(globals.day)
            globals.spending[3].append(data[0])
            globals.spending[4].append(data[1])
        else:
            globals.spending[0].append(data[0])
            globals.spending[1].append(data[1])
            globals.spending[2].append(data[2])
            globals.spending[3].append(data[3])
            globals.spending[4].append(data[4])
        labels = []
        labels.append("繼續")
        labels.append("結束")
        texts = []
        texts.append("back to set spending")
        texts.append("go to spending")
        send_yes_no_message(reply_token, "記錄完成", f"系統已紀錄您在{globals.spending[0][len(globals.spending[0]) - 1]}年{globals.spending[1][len(globals.spending[0]) - 1]}月{globals.spending[2][len(globals.spending[0]) - 1]}日的{globals.spending[3][len(globals.spending[0]) - 1]}支出為{globals.spending[4][len(globals.spending[0]) - 1]}元，請問是否要繼續記錄？按結束以回到記帳選單。", labels, texts)


    def on_enter_tree(self, event):
        print("I'm entering 植物")
        labels = ["主選單"]
        texts = ["回到主選單"]
        img = "https://as1.ftcdn.net/jpg/01/67/72/04/500_F_167720496_af8JnHFQM7QMyIIz31tgp289ukGtlXKB.jpg"

        reply_token = event.reply_token
        send_button_message(reply_token, img, "植物界面", "請選擇你想使用的功能", labels, texts)
