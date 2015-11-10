import calendar
import os
import urllib
import cgi

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

class CalendarClass:
    
    def __init__(self):
        self.myFilename = "myCourseSchedule.cal"
        self.myCalendar = calendar.Calendar(0)
        self.startMonth = -1
        self.startDate = -1
        self.startYear = -1
        self.numWeeks = 0
        self.meetDays = []
        self.schedule = []
        temp = CalendarClass.CalendarClassTableRow()
        temp.date = "Date"
        temp.chapter = "Chapter"
        temp.topic = "Topic"
        self.schedule.append(temp)
        
    def validGenerateDatesState(self):
    
        if not ((0 < self.startMonth) and (self.startMonth < 13)):
            return False
        if self.startYear < 0:
            return False
            
        testI = self.myCalendar.itermonthdates(self.startYear, self.startMonth)
        hasDate = False
        i = next(testI, None)
        while not(i is None):
            if i.day == self.startDate:
                hasDate = True
            i = next(testI, None)
        if not(hasDate):
            return False
        
        if len(self.meetDays) > 7:
            return False
        hasMon = False
        hasTue = False
        hasWed = False
        hasThu = False
        hasFri = False
        hasSat = False
        hasSun = False
        for j in self.meetDays:
            if ((j < 0) or (j > 6)):
                return False
            if j == 0:
                if hasMon == True:
                    return False
                hasMon = True
            if j == 1:
                if hasTue == True:
                    return False
                hasTue = True            
            if j == 2:
                if hasWed == True:
                    return False
                hasWed = True            
            if j == 3:
                if hasThu == True:
                    return False
                hasThu = True
            if j == 4:
                if hasFri == True:
                    return False
                hasFri = True
            if j == 5:
                if hasSat == True:
                    return False
                hasSat = True
            if j == 6:
                if hasSun == True:
                    return False
                hasSun = True
        
        return True
                
    def generateDates(self):
        if self.validGenerateDatesState():
            startMonth = self.startMonth
            startDate = self.startDate 
            startYear = self.startYear
            numWeeks = self.numWeeks
            if len(self.meetDays) == 0:
                meetDays = [0]
            else:
                meetDays = self.meetDays

            weekNum = 0
            thisMonth = startMonth
            thisYear = startYear
            scheduleDays = []

            while weekNum <= numWeeks:
                
                i = self.myCalendar.itermonthdates(thisYear, thisMonth)
                calendarOffset = 0
                v = next(i, None)
                #iterate to start of thisMonth
                while (not(v is None)) and v.month != thisMonth:
                    calendarOffset = calendarOffset+1
                    v = next(i, None)

                #iterate to startDate (only on first pass through while loop)
                while (not(v is None)) and (thisMonth == startMonth) and (thisYear == startYear) and (v.day < startDate):
                    calendarOffset = calendarOffset+1
                    v = next(i, None)

                #iterate through thisMonth and save dates that are meetDays
                while (not(v is None)) and (v.month == thisMonth) and (weekNum <= numWeeks):
                    for meetday in meetDays:       
                        if (calendarOffset % 7) == meetday:
                            scheduleDays.append(v)
                    v = next(i, None)
                    calendarOffset = calendarOffset+1
                    if (calendarOffset%7) == 0:
                        weekNum = weekNum + 1
                        
                #advance to next month, or next year and reset month to 1
                thisMonth = thisMonth+1
                if thisMonth == 13:
                    thisYear = thisYear +1
                    thisMonth = 1
            
            #place days in self.schedule and extend it when needed
            counter = 0
            for i in scheduleDays:
                if (counter + 2) > len(self.schedule):
                    temp = CalendarClass.CalendarClassTableRow()
                    temp.date = str(i.month) + "/" + str(i.day)
                    self.schedule.append(temp)
                else:
                    self.schedule[counter+1].date = str(i.month) + "/" + str(i.day)
                counter = counter +1
                
        else:
            print "internal state is not valid for generating dates"
    
    def insertNewRowAfter(self, index):
        if index > -1:
            temp = CalendarClass.CalendarClassTableRow()
            if index < len(self.schedule):
                self.schedule.insert(index+1, temp)
            else:
                self.schedule.append(temp)
                
    def deleteRow(self, index):
        if (index > 0) and (index < len(self.schedule)):
            self.schedule.pop(index)
            
    def getCell(self, column, row):
        if (row > -1) and (row < len(self.schedule)):
            if column == 0:
                return self.schedule[row].date
            if column == 1:
                return self.schedule[row].chapter
            if column == 2:
                return self.schedule[row].topic
        return ""
        
    def setCell(self, column, row, value):
        if (row > -1) and (row < len(self.schedule)):
            if column == 0:
                self.schedule[row].date = str(value)
            if column == 1:
                self.schedule[row].chapter = str(value)
            if column == 2:
                self.schedule[row].topic = str(value)

    def printToConsole(self):
        for i in self.schedule:
            print i.toString()
                
    class CalendarClassTableRow:       
        def __init__(self):
            self.date = ""
            self.chapter = ""
            self.topic = ""
            
        def toString(self):
            return self.date + ", " + self.chapter + ", " + self.topic

mySched = CalendarClass()
message = ""

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
    
class CalendarHandler(webapp2.RequestHandler):
    def get(self):    
        moChecked = ""
        tuChecked = ""
        weChecked = ""
        thChecked = ""
        frChecked = ""
        saChecked = ""
        suChecked = ""
        if 0 in mySched.meetDays:
            moChecked = "checked"
        if 1 in mySched.meetDays:
            tuChecked = "checked"
        if 2 in mySched.meetDays:
            weChecked = "checked"
        if 3 in mySched.meetDays:
            thChecked = "checked"
        if 4 in mySched.meetDays:
            frChecked = "checked"
        if 5 in mySched.meetDays:
            saChecked = "checked"
        if 6 in mySched.meetDays:
            suChecked = "checked"                       
           
        template_values = {
            'startMonth': mySched.startMonth,
            'startDate': mySched.startDate,
            'startYear': mySched.startYear,
            'numWeeks': mySched.numWeeks,
            'mondayChecked': moChecked,
            'tuesdayChecked': tuChecked,
            'wednesdayChecked': weChecked,
            'thursdayChecked': thChecked,
            'fridayChecked': frChecked,
            'saturdayChecked': saChecked,
            'sundayChecked': suChecked,
            'myCalendarSchedule': mySched.schedule,
            'myFileName': mySched.myFilename,
            'msg': message
        }

        template = JINJA_ENVIRONMENT.get_template("calendarEdit.html")
        self.response.out.write(template.render(template_values))

    def post(self):
        global message
        global mySched
        
        loadFile = self.request.get('loadFile')
        generateDates = self.request.get('generateCalendar')
        rowInsert = self.request.get('insertRow')
        rowRemove = self.request.get('removeRow')
        save = self.request.get('save')
        
        if loadFile:
            message = "loadFile"
            if self.request.get('fileName') == 'new': 
                message = "newFile"
                mySched = CalendarClass()
        
        if generateDates:
            message = "generateDates"
            try:
                startMonth = int(self.request.get("startMonth"))
                startDate = int(self.request.get("startDate"))
                startYear = int(self.request.get("startYear"))
                numWeeks = int(self.request.get("weeksThisSemester"))
            except:
                message = "invalid input"
                startMonth = mySched.startMonth
                startDate = mySched.startDate
                startYear = mySched.startYear
                numWeeks = mySched.numWeeks
            
            meetMonday = self.request.get('Monday')
            meetTuesday = self.request.get('Tuesday')
            meetWednesday = self.request.get('Wednesday')
            meetThursday = self.request.get('Thursday')
            meetFriday = self.request.get('Friday')
            meetSaturday = self.request.get('Saturday')
            meetSunday = self.request.get('Sunday')

            mySched.startMonth = startMonth
            mySched.startDate = startDate
            mySched.startYear = startYear
            mySched.numWeeks = numWeeks
            mySched.meetDays = []
            if meetMonday:
                mySched.meetDays.append(0)
            if meetTuesday:
                mySched.meetDays.append(1)
            if meetWednesday:
                mySched.meetDays.append(2)
            if meetThursday:
                mySched.meetDays.append(3)
            if meetFriday:
                mySched.meetDays.append(4)
            if meetSaturday:
                mySched.meetDays.append(5)
            if meetSunday:
                mySched.meetDays.append(6)
                
            mySched.generateDates()
                
        if rowInsert:
            message = "insertRow"
            try:
                mySched.insertNewRowAfter(int(self.request.get("targetRowInsert")))
            except:
                message = "invalidInput"
                
        if rowRemove:
            message = "removeRow"
            try:
                mySched.deleteRow(int(self.request.get("targetRowRemove")))
            except:
                message = "invalidInput"
        
        if save:
            message = "saved"
            mySched.myFilename = self.request.get('fileName')
            for i in range(len(mySched.schedule)):
                for j in range(3):
                    mySched.setCell(j,i,self.request.get("r"+str(i)+"c"+str(j)))
                    
            
        self.redirect('/editcalendar')