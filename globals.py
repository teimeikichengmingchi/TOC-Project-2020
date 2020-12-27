def initGlobals():
    global goal
    goal = 0
    global year, month, day
    year, month, day = 0, 0, 0
    global setToday, setTodayFlag
    setToday, setTodayFlag = False, False
    global spending
    spending = [[2020, 12, 27, "娛樂", 20], [2020, 12, 27, "娛樂", 20], [2020, 12, 27, "食物", 6], [2020, 12, 27, "娛樂", 20], [2020, 12, 26, "娛樂", 17],] 
    global pastMonthSpending, pastYearSpending
    pastMonthSpending, pastYearSpending = {}, {}
    #global tempSpending
    #tempSpending = [0, 0, 0, 0, 0]