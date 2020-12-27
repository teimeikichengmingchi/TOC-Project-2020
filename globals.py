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
    global nutrient, water, point, happy
    nutrient, water, point, happy = 10, 10, 0, 0
    global treeAct
    treeAct = ""
    global treeActPoint
    treeActPoint = [1, 1, 2]
    global getPointDate
    getPointDate = ""
    global decreaseTreeTime
    decreaseTreeTime = 0
    global treeType
    treeType = ["枯樹", "普通的樹", "肥樹", "水系樹", "說話樹", "火樹"]
    #global tempSpending
    #tempSpending = [0, 0, 0, 0, 0]