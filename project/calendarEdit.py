from calendarClass import CalendarClass
from basehandler import BaseHandler
from syllabus import Syllabus
from term import Term
from user import User 

import os
import urllib
import cgi

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
                        
message = ""

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
        
class CalendarHandler(BaseHandler):
    def get(self):
        userKey = self.session.get('user')
        user = ndb.Key(urlsafe = userKey).get()
        syllabusKey = self.session.get('syllabus')
        syllabus = ndb.Key(urlsafe = syllabusKey).get()
        myCalendars = CalendarClass.query(ancestor = syllabus.key).fetch()
        if myCalendars:
            for i in myCalendars:
                mySched = i
        else:
            CalendarClass.generateDummyCalendar()
            mySched = CalendarClass(parent = syllabus.key)
            mySched.schedule.append('Date')
            mySched.schedule.append('Chapter')
            mySched.schedule.append('Topic')
            mySched.put()
            
    
        savedCalendars = CalendarClass.query()
        savedCalendarNames = []
        for i in savedCalendars:
            savedCalendarNames.append(i.myFilename)
        
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
            'savedCalendars': savedCalendarNames,
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
        
        userKey = self.session.get('user')
        user = ndb.Key(urlsafe = userKey).get()
        syllabusKey = self.session.get('syllabus')
        syllabus = ndb.Key(urlsafe = syllabusKey).get()
        userKey = self.session.get('user')
        user = ndb.Key(urlsafe = userKey).get()
        syllabusKey = self.session.get('syllabus')
        syllabus = ndb.Key(urlsafe = syllabusKey).get()
        myCalendars = CalendarClass.query(ancestor = syllabus.key).fetch()
        if myCalendars:
            for i in myCalendars:
                mySched = i
        else:
            mySched = CalendarClass.generateDummyCalendar()
            mySched = CalendarClass(parent = syllabus.key)
            
        if loadFile:
            message = "loadFile"
            loadFileName = self.request.get('fileName')
            if loadFileName == 'new': 
                message = "newFile"
                mySched.parent = None
                mySched = CalendarClass.new()
                mySched.parent = syllabus.key
                mySched.put()
            else:
                savedCalendars = CalendarClass.query()
                message = ""
                queriedCalendars = []
                for i in savedCalendars:
                    queriedCalendars.append(i)
                    message = message + queriedCalendars[len(queriedCalendars)-1].myFilename + ", "
                mySched.parent = None
                mySched.put()
                mySched = queriedCalendars[int(loadFileName)]
                mySched.parent = syllabus.key
                mySched.put()
        
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
            mySched.put()
                
        if rowInsert:
            message = "insertRow"
            try:
                mySched.insertNewRowAfter(int(self.request.get("targetRowInsert")))
                mySched.put()
            except:
                message = "invalidInput"
                
        if rowRemove:
            message = "removeRow"
            try:
                mySched.deleteRow(int(self.request.get("targetRowRemove")))
                mySched.put()
            except:
                message = "invalidInput"
        
        if save:
            message = "saved"
            newFileName = self.request.get('fileName')
            for i in range(len(mySched.schedule)):
                for j in range(3):
                    mySched.setCell(j,i,self.request.get("r"+str(i)+"c"+str(j)))
            if (mySched.myFilename != newFileName):
                mySched.myFilename = newFileName
                mySched = mySched.clone()
            mySched.put()
            
        return self.redirect('/editcalendar')

