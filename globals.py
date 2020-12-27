def initGlobals():
    global goal
    goal = 0
    global year, month, day
    year, month, day = 0, 0, 0
    global setToday, setTodayFlag
    setToday, setTodayFlag = False, False
    global spending
    spending = [[], [], [], [], []]
    tempSpending = [0, 0, 0, 0, 0]