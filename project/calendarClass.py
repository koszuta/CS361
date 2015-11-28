import calendar

from google.appengine.api import users
from google.appengine.ext import ndb

class CalendarClass(ndb.Model):

    myFilename = ndb.StringProperty(default = 'myCalendar.cal')
    startMonth = ndb.IntegerProperty(default = -1)
    startDate = ndb.IntegerProperty(default = -1)
    startYear = ndb.IntegerProperty(default = -1)
    numWeeks = ndb.IntegerProperty(default = -1)
    meetDays = ndb.IntegerProperty(repeated = True)
    schedule = ndb.StringProperty(repeated = True)
    
    @staticmethod
    def new():
        nc = CalendarClass()
        nc.schedule.append("Date")
        nc.schedule.append("Chapter")
        nc.schedule.append("Topic")
        return nc
    
    def validGenerateDatesState(self):
    
        if not ((0 < self.startMonth) and (self.startMonth < 13)):
            return False
        if self.startYear < 0:
            return False
        
        tempCal = calendar.Calendar(0)
        testI = tempCal.itermonthdates(self.startYear, self.startMonth)
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
            tempCal = calendar.Calendar(0)
            
            while weekNum <= numWeeks:
                
                i = tempCal.itermonthdates(thisYear, thisMonth)
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
                if (3*(counter + 2)) > len(self.schedule):
                    self.schedule.append(str(i.month) + "/" + str(i.day))
                    self.schedule.append("")
                    self.schedule.append("")
                else:
                    self.schedule[3*(counter+1)] = str(i.month) + "/" + str(i.day)
                counter = counter +1
                
        else:
            print "internal state is not valid for generating dates"
    
    def insertNewRowAfter(self, index):
        if index > -1:
            if (3*index) < len(self.schedule):
                self.schedule.insert(3*(index+1), "")
                self.schedule.insert(3*(index+1), "")
                self.schedule.insert(3*(index+1), "")
            else:
                self.schedule.append("")
                self.schedule.append("")
                self.schedule.append("")
                
    def deleteRow(self, index):
        if (index > 0) and (3*index < len(self.schedule)):
            self.schedule.pop(3*index)
            self.schedule.pop(3*index)
            self.schedule.pop(3*index)
            
    def getCell(self, column, row):
        if (row > -1) and ((3*row + column) < len(self.schedule)):
            if (column > -1) and (column < 3):
                return self.schedule[(3*row + column)]
        return ""
        
    def setCell(self, column, row, value):
        if (row > -1) and ((3*row + column) < len(self.schedule)):
            if (column > -1) and (column < 3):
                self.schedule[(3*row + column)] = str(value)
                
    def clone(self):
        newCal = CalendarClass()
        newCal.myFilename = self.myFilename
        newCal.startMonth = self.startMonth
        newCal.startDate = self.startDate
        newCal.startYear = self.startYear
        newCal.numWeeks = self.numWeeks
        for i in self.meetDays:
            newCal.meetDays.append(i)
        for j in self.schedule:
            newCal.schedule.append(j)
        return newCal
        
    @staticmethod
    def generateDummyCalendar():
        dummyCal = CalendarClass.new()
        dummyCal.myFilename = "CS361FALL2015.cal"
        dummyCal.startMonth = 9
        dummyCal.startDate = 2
        dummyCal.startYear = 2015
        dummyCal.numWeeks = 16
        dummyCal.meetDays.append(2)
        dummyCal.generateDates()
        dummyCal.deleteRow(17)
        dummyCal.setCell(1,1,"1")
        dummyCal.setCell(1,2,'2,<a href="http://www.w3.org/wiki/Web_Standards_Curriculum">HTML5/CSS</a>')
        dummyCal.setCell(1,3,"3,Scrum")
        dummyCal.setCell(1,4,"4")
        dummyCal.setCell(1,5,"")
        dummyCal.setCell(1,6,'<a href="https://www.scrum.org/About/All-Articles">Test-Driven Dev</a>')
        dummyCal.setCell(1,7,"Midterm")
        dummyCal.setCell(1,8,"S: ch.7")
        dummyCal.setCell(1,9,"Sprint 1")
        dummyCal.setCell(1,10,"S: ch.5")
        dummyCal.setCell(1,11,"Z: ch 6")
        dummyCal.setCell(1,12,"Sprint 2")
        dummyCal.setCell(1,13,"Sprint 2")
        dummyCal.setCell(1,14,"S: ch. 9")
        dummyCal.setCell(1,15,"")
        dummyCal.setCell(1,16,"Final Exam")

        dummyCal.setCell(2,1,"What is software engineering?")
        dummyCal.setCell(2,2,"HTML5/CSS")
        dummyCal.setCell(2,3,"Scrum: Intro, PB grooming")
        dummyCal.setCell(2,4,"Lecture 1: Scrum: Sprint planning; Lecture 2: introduce project: sprint 0; Lab PB grooming, sprint planning")
        dummyCal.setCell(2,5,"Lecture 1: daily scrum, execution")
        dummyCal.setCell(2,6,"")
        dummyCal.setCell(2,7,"")
        dummyCal.setCell(2,8,"Test driven development")
        dummyCal.setCell(2,9,"")
        dummyCal.setCell(2,10,"Encapsulation")
        dummyCal.setCell(2,11,"Interface Oriented Design")
        dummyCal.setCell(2,12,"")
        dummyCal.setCell(2,13,"")
        dummyCal.setCell(2,14,"Continuous integration")
        dummyCal.setCell(2,15,"")
        dummyCal.setCell(2,16,"")
        
        return dummyCal