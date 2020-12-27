import globals
from transitions.extensions import GraphMachine

from datetime import date, datetime
import random
import math

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

    def is_going_to_checkSpendingMenu(self, event):
        text = event.message.text
        return text.lower() == "go to check spending menu"

    def is_going_to_checkSpending(self, event):
        text = event.message.text
        return text.lower() == "year" or text.lower() == "month" or text.lower() == "day"

    def is_going_to_tree(self, event):
        text = event.message.text
        return text.lower() == "go to tree"

    def is_going_to_treeIntro(self, event):
        text = event.message.text
        return text.lower() == "go to treeIntro"

    def is_going_to_myCurrentTree(self, event):
        text = event.message.text
        return text.lower() == "go to my current tree" or text.lower() == "back to my tree"

    def is_going_to_configInteractWithTree(self, event):
        text = event.message.text
        globals.treeAct = text.lower()
        return text.lower() == "water" or text.lower() == "sing" or text.lower() == "fertilize"

    def is_going_to_interactWithTree(self, event):
        text = event.message.text
        return text.lower() == "go to interact"

    def on_enter_menu(self, event):
        print("I'm entering menu")
        if globals.decreaseTreeTime == "":
            globals.decreaseTreeTime = event.timestamp
        labels = ["植物介面", "記帳介面"]
        texts = ["go to tree", "go to spending"]
        img = "https://as2.ftcdn.net/jpg/03/24/86/31/500_F_324863161_fdTcdogpUbv7gJvpngFxKD89f50NZtD4.jpg"

        reply_token = event.reply_token
        send_button_message(reply_token, img, "主選單", "請選擇你想使用的功能", labels, texts)

    def on_enter_spending(self, event):
        globals.setTodayFlag = False
        labels = ["設定今月花費上限", "記帳", "查看記帳", "主選單"]
        texts = ["set goal", "record spending", "go to check spending menu", "回到主選單"]
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
            if not globals.getPointDate == str(globals.year)+str(globals.month)+str(globals.day):
                globals.getPointDate = str(globals.year)+str(globals.month)+str(globals.day)
                print(f"\n\n{globals.getPointDate}\n\n")
                globals.point += 3
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
            globals.spending.append([globals.year, globals.month, globals.day, data[0], int(data[1])])
        else:
            globals.spending.append([int(data[0]), int(data[1]), int(data[2]), data[3], int(data[4])])
        labels = []
        labels.append("繼續")
        labels.append("結束")
        texts = []
        texts.append("back to set spending")
        texts.append("go to spending")
        send_yes_no_message(reply_token, "記錄完成", f"系統已紀錄您在{globals.spending[len(globals.spending) - 1][0]}年{globals.spending[len(globals.spending) - 1][1]}月{globals.spending[len(globals.spending) - 1][2]}日的{globals.spending[len(globals.spending) - 1][3]}支出為{globals.spending[len(globals.spending) - 1][4]}元，請問是否要繼續記錄？按結束以回到記帳選單。", labels, texts)

    def on_enter_checkSpendingMenu(self, event):
        globals.spending.sort(key = lambda l:l[3])
        globals.spending.sort(key = lambda l:l[2])
        globals.spending.sort(key = lambda l:l[1])
        globals.spending.sort(key = lambda l:l[0])
        bp = -1
        print(f"len = {len(globals.spending)}")
        for i in range(len(globals.spending)):
            if not globals.spending[i][0] == globals.year:
                typeDict = globals.pastYearSpending.get(globals.spending[i][0])#紀錄花費的類別的字典，內容如{"娛樂": 200, "食物" : 200}
                if typeDict == None:
                    globals.pastYearSpending.update({globals.spending[i][0] : {globals.spending[i][3] : globals.spending[i][4]}})
                    continue
                value = typeDict.get(globals.spending[i][3])
                if value == None:
                    typeDict.update({globals.spending[i][3] : globals.spending[i][4]})
                    continue
                typeDict.update({globals.spending[i][3] : value + globals.spending[i][4]})
            else:
                bp = i
                break
        if bp == -1:
            bp = len(globals.spending)
        for i in range(bp):
            globals.spending.pop(0)
        print(f"len = {len(globals.spending)}")
        bp = -1
        for i in range(len(globals.spending)):
            if not globals.spending[i][1] == globals.month:
                typeDict = globals.pastMonthSpending.get(globals.spending[i][1])#紀錄花費的類別的字典，內容如{"娛樂": 200, "食物" : 200}
                if typeDict == None:
                    globals.pastMonthSpending.update({globals.spending[i][1] : {globals.spending[i][3] : globals.spending[i][4]}})
                    continue
                value = typeDict.get(globals.spending[i][3])
                if value == None:
                    typeDict.update({globals.spending[i][3] : globals.spending[i][4]})
                    continue
                typeDict.update({globals.spending[i][3] : value + globals.spending[i][4]})
            else:
                bp = i
                break
        if bp == -1:
            bp = len(globals.spending)
        for i in range(bp):
            globals.spending.pop(0)
        print(f"\n\n\nglobals.spending = {globals.spending}\ntempRecordYearSpending = {globals.pastYearSpending}\ntempRecordMonthSpending = {globals.pastMonthSpending}\n\n\n")
        record, t, d = 0, globals.spending[0][3], globals.spending[0][2]
        for i, ele in enumerate(globals.spending):
            if i == 0: continue
            if ele[3] == t and ele[2] == d:
                globals.spending[record][4] += ele[4]
            else :
                record += 1
                d = ele[2]
                t = ele[3]
                globals.spending[record] = ele
        for i in range(record + 1, len(globals.spending)):
            globals.spending.pop(record + 1)
        print(f"\n\n\nglobals.spending = {globals.spending}\ntempRecordYearSpending = {globals.pastYearSpending}\ntempRecordMonthSpending = {globals.pastMonthSpending}\n\n\n")

        labels = []
        labels.append("過去年度紀錄")
        labels.append("今年月分紀錄")
        labels.append("今月每日紀錄")
        texts = []
        texts.append("year")
        texts.append("month")
        texts.append("day")

        reply_token = event.reply_token
        send_button_message(reply_token, "https://as2.ftcdn.net/jpg/01/06/75/95/500_F_106759526_UoGu2eWG39GZayy4TgluEV9096L9dAqy.jpg", "帳款紀錄", "請選擇你想使用的功能", labels, texts)

    def on_enter_checkSpending(self, event):
        tempSum = 0
        countGreaterThenNow = 0
        countSmallerThenNow = 0
        replyStr = ""
        if event.message.text == "year":
            if globals.pastYearSpending:
                replyStr += "您過去各年度的花費如下：\n"
                for y in globals.pastYearSpending.keys():
                    replyStr += f"\n\n{y}年 ：\n"
                    tempSum = 0
                    for t in globals.pastYearSpending.get(y).keys():
                        replyStr += f"\n{t}花費為{globals.pastYearSpending.get(y).get(t)}元"
                        tempSum += globals.pastYearSpending.get(y).get(t)
                    if globals.goal > 0:
                        if (tempSum / 12) / globals.goal > 1.1:
                            countGreaterThenNow += 1
                        elif (tempSum / 12) / globals.goal < 0.9:
                            countSmallerThenNow += 1
                if globals.goal > 0:
                    replyStr += f"\n\n其中共有{countGreaterThenNow}年的平均花費大於現在目標，有{countSmallerThenNow}年的平均花費小於現在目標。"
                    if countGreaterThenNow > countSmallerThenNow:
                        replyStr += "\n依過去數年的紀錄來看，現在目標訂得有挑戰性喔！請好好加油！"
                    else:
                        replyStr += "\n依過去數年的紀錄來看，可能可以自己斟酌要不要把記帳目標的難度再調高一點喔。"
        elif event.message.text == "month":
            if globals.pastMonthSpending:
                replyStr += "您今年各月份的花費如下：\n"
                for y in globals.pastMonthSpending.keys():
                    print(f"{y}\n")
                    replyStr += f"\n\n{y}月 ：\n"
                    tempSum = 0
                    print(globals.pastMonthSpending.get(y))
                    for t in globals.pastMonthSpending.get(y).keys():
                        replyStr += f"\n{t}花費為{globals.pastMonthSpending.get(y).get(t)}元"
                        tempSum += globals.pastMonthSpending.get(y).get(t)
                    if globals.goal > 0:
                        if tempSum / globals.goal > 1.1:
                            countGreaterThenNow += 1
                        elif tempSum / globals.goal < 0.9:
                            countSmallerThenNow += 1
                if globals.goal > 0:
                    replyStr += f"\n\n其中共有{countGreaterThenNow}個月的平均花費大於現在目標，有{countSmallerThenNow}個月的平均花費小於現在目標。"
                    if countGreaterThenNow > countSmallerThenNow + 1:
                        replyStr += "\n依過去數個月的紀錄來看，現在目標訂得有挑戰性喔！請好好加油！"
                    elif countGreaterThenNow < countSmallerThenNow - 1:
                        replyStr += "\n依過去數個月的紀錄來看，可能可以自己斟酌要不要把記帳目標的難度再調高一點喔。"
                    else:
                        replyStr += "\n依過去數個月的紀錄來看，目前的目標大約與過去持平。"
        elif event.message.text == "day":
            if globals.spending:
                d = 0
                countDay = 0
                replyStr += "您本月的花費如下：\n"
                for ele in globals.spending:
                    print(ele)
                    if not d == ele[2]:
                        d = ele[2]
                        countDay += 1
                        replyStr += f"\n\n{ele[1]}月{ele[2]}號：\n"
                    replyStr += f"\n{ele[3]}花費{ele[4]}元"
                    tempSum += ele[4]
                if globals.goal > 0:
                    if (tempSum / countDay) / globals.goal > 1.1:
                        replyStr += "\n依目前情況來看，這個月可能要節省一點才能達到目標喔。"
                    elif (tempSum / countDay) / globals.goal < 0.9:
                        replyStr += "\n依目前情況來看，這個月的目標離你很近了！"
                    else:
                        replyStr += "\n依目前情況來看，只要再節儉一點就一定能達到目標了喔！"
        reply_token = event.reply_token
        if replyStr == "":
            replyStr = "沒有紀錄！！"
        message = []
        message.append(TextSendMessage(text=replyStr))
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

    def on_enter_tree(self, event):
        print("I'm entering 植物")
        labels = ["查看目前植物狀態",  "主選單", ]#"查詢樹種",
        texts = ["go to my current tree",  "回到主選單", ]#"go to treeIntro",
        img = "https://as1.ftcdn.net/jpg/01/67/72/04/500_F_167720496_af8JnHFQM7QMyIIz31tgp289ukGtlXKB.jpg"

        reply_token = event.reply_token
        send_button_message(reply_token, img, "植物界面", "請選擇你想使用的功能", labels, texts)

    def on_enter_myCurrentTree(self, event):
        img = "https://as1.ftcdn.net/jpg/00/83/50/24/500_F_83502495_xS01iodgg9kq01SjjQUApvWbc6Ty6gwu.jpg"
        elaHour = math.floor((event.timestamp - globals.decreaseTreeTime) / 12)
        # if elaHour > 0:
        #     globals.water -= elaHour
        #     globals.nutrient -= elaHour
        #     globals.decreaseTreeTime = event.timestamp
        message = []
        # if globals.water <= 0 or globals.nutrient <= 0:
        #     message.append(TextSendMessage(text=f"經過您這段時間的放置後，小樹成為了一顆枯樹了！真可憐！詳細介紹請至植物選單查看喔。\n同時您得到了一棵新的小樹，一切數值將歸零重新計算，不要再養死了喔。"))
        #     globals.water = 10
        #     globals.nutrient = 10
        #     globals.happy = 0
        # if globals.water > 30 and globals.nutrient > 30:
        #     message.append(TextSendMessage(text=f"經過您這段時間的照顧後，小樹成為了一顆大樹了！詳細介紹請至植物選單查看喔。\n同時您得到了一棵新的小樹，一切數值將歸零重新計算。"))
        #     globals.water = 10
        #     globals.nutrient = 10
        #     globals.happy = 0
        replyStr = f"您目前的小樹水分值為{globals.water}，養分值為{globals.nutrient}，而您共有{globals.point}分可進行消費。\n請注意，水分值和養分值只要有一個歸零，小樹都有可能枯死喔。"
        
        message.append(TextSendMessage(text=replyStr))
        message.append(
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title="您的小樹",
                    text="請選擇行動",
                    actions=[
                        MessageTemplateAction(
                            label="澆水",
                            text="water"
                        ),
                        MessageTemplateAction(
                            label="施肥",
                            text="fertilize"
                        ),
                        MessageTemplateAction(
                            label="唱歌",
                            text="sing"
                        ),
                        MessageTemplateAction(
                            label="回到植物頁面",
                            text="go to tree"
                        ),
                    ]
                )
            )
        )
        reply_token = event.reply_token
        send_multi_mess(reply_token, message)

    def on_enter_configInteractWithTree(self, event):
        replyStr = ""
        if globals.treeAct == "water":
            replyStr = f"您確定要花費{globals.treeActPoint[0]}點體力值來替小樹澆水嗎？"
        elif globals.treeAct == "fertilize":
            replyStr = f"您確定要花費{globals.treeActPoint[1]}點體力值來替小樹施肥嗎？"
        elif globals.treeAct == "sing":
            replyStr = f"您確定要花費{globals.treeActPoint[2]}點體力值來對小樹唱歌嗎？"

        labels = []
        labels.append("確定")
        labels.append("取消")
        texts = []
        texts.append("go to interact")
        texts.append("back to my tree")
        reply_token = event.reply_token
        send_yes_no_message(reply_token, "系統提示", replyStr, labels, texts)

    def on_enter_interactWithTree(self, event):
        replyStr = ""
        if globals.treeAct == "water":
            if globals.point >= 1:
                globals.point -= 1
                temp = random.randint(1, 3)
                globals.water += temp
                replyStr = f"你替小樹澆了水，水分值增加{temp}。\n小數現在水分值為{globals.water}"
        elif globals.treeAct == "fertilize":
            if globals.point >= 1:
                globals.point -= 1
                temp = random.randint(1, 3)
                globals.nutrient += temp
                replyStr = f"你替小樹施了肥，養分值增加{temp}。\n小數現在養分值為{globals.nutrient}"
        elif globals.treeAct == "sing":
            if globals.point >= 2:
                globals.point -= 2
                temp = random.randint(1, 3)
                globals.happy += temp
                replyStr = f"你對著小樹唱了歌！不知道小樹聽不聽得懂但總之你很快樂！"

        if replyStr == "":
            replyStr = f"錯誤！您剩餘的體力點為{globals.point}點，不足進行此行動。"
        message = []
        message.append(TextSendMessage(text=replyStr))
        message.append(
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title="回到我的小樹",
                    text="請點選按鈕以回到我的小樹",
                    actions=[
                        MessageTemplateAction(
                            label="回到我的小樹",
                            text="go back"
                        )
                    ]
                )
            )
        )
        reply_token = event.reply_token
        send_multi_mess(reply_token, message)
        
    def on_enter_treeIntro(self, event):
        replyStr = ""
        reply_token = event.reply_token
        send_text_message(reply_token, "目前已有的樹種：\n\n普通的樹：\n毫無反應就是一棵樹。\n中規中矩的種法可得。\n\n枯樹：\n曾經是樹，現在已經不是了，只是一堆木材，還不能拿來加工。放置太久會造成的結果\n\n請輸入任意鍵以離開")
