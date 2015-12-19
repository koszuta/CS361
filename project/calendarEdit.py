from calendarClass import CalendarClass
from basehandler import BaseHandler, login_required, syllabus_required
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

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
  
  	      
class CalendarHandler(BaseHandler):
    @login_required	 
    @syllabus_required
    def get(self):
    
        message = ""
        user = self.current_user
        syllabus = self.current_syllabus
        term = self.current_term
        
        savedCalendars = CalendarClass.query(ancestor=user.key).filter(CalendarClass.workingCalendar == False).fetch()
        savedCalendarNames = []
        for i in savedCalendars:
            savedCalendarNames.append(i.myFilename)
        
        syllabusCalendars = CalendarClass.query(ancestor=user.key).filter(CalendarClass.workingCalendar == True).fetch()
        if syllabusCalendars:
            #should have exactly 0 or 1 calendar
            for i in syllabusCalendars:
                mySched = i
        else:
            mySched = None
            
        message = str(len(syllabusCalendars))
        
        moChecked = ""
        tuChecked = ""
        weChecked = ""
        thChecked = ""
        frChecked = ""
        saChecked = ""
        suChecked = ""
        
        if mySched:
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
            'mySchedule': mySched,
            'savedCalendars': savedCalendarNames,
            'mondayChecked': moChecked,
            'tuesdayChecked': tuChecked,
            'wednesdayChecked': weChecked,
            'thursdayChecked': thChecked,
            'fridayChecked': frChecked,
            'saturdayChecked': saChecked,
            'sundayChecked': suChecked,
            'msg': message
        }

        template = JINJA_ENVIRONMENT.get_template("calendarEdit.html")
        self.response.out.write(template.render(template_values))

    @login_required	 
    @syllabus_required
    def post(self):
        
        message = ""
        assignToSyllabus = self.request.get('assignToSyllabus')
        loadFile = self.request.get('loadFile')
        generateDates = self.request.get('generateCalendar')
        rowInsert = self.request.get('insertRow')
        rowRemove = self.request.get('removeRow')
        save = self.request.get('save')
        
        user = self.current_user
        syllabus = self.current_syllabus
        term = self.current_term


        syllabusCalendars = CalendarClass.query(ancestor=user.key).filter(CalendarClass.workingCalendar == True).fetch()
        if syllabusCalendars:
            #should have exactly 1 calendar
            for i in syllabusCalendars:
                mySched = i
        else:
            #should not be reachable state
            mySched = None
            
        if assignToSyllabus:
            assign = self.request.get('onSyllabus')
            if assign:
                if mySched:
                    if not mySched.onSyllabus:
                        mySched.workingCalendar = False
                        mySched.put()
                        onScheduleCalendar = CalendarClass.query(ancestor=syllabus.key).filter(CalendarClass.onSyllabus == True).fetch()
                        if onScheduleCalendar:
                            for i in onScheduleCalendar:
                                i.key.delete()                                
                        mySched = mySched.clone(syllabus.key)
                        mySched.onSyllabus = True
                        mySched.workingCalendar = True
                        mySched.put()
                    
        if loadFile:
            message = "loadFile"
            loadFileName = self.request.get('fileName')
            if loadFileName == 'new': 
                message = "newFile"
                if mySched:
                    mySched.workingCalendar = False
                    mySched.put()

                if syllabus.info and term and syllabus.info.days:            
                    mySched = CalendarClass(parent = user.key)
                    mySched.schedule.append('Date')
                    mySched.schedule.append('Reading')
                    mySched.schedule.append('Topic')
                    mySched.workingCalendar = True
                    
                    if 'M' in syllabus.info.days:
                        mySched.meetDays.append(0)                        
                    if 'T' in syllabus.info.days:
                        mySched.meetDays.append(1)
                    if 'W' in syllabus.info.days:
                        mySched.meetDays.append(2)
                    if 'R' in syllabus.info.days:
                        mySched.meetDays.append(3)
                    if 'F' in syllabus.info.days:
                        mySched.meetDays.append(4)
                        
                    mySched.startMonth = int(syllabus.info.startDate.split('/')[0])
                    mySched.startDate = int(syllabus.info.startDate.split('/')[1])
                    mySched.startYear = int(term.year)
                    mySched.numWeeks = 15
                    #mySched.generateDates()
                    mySched.myFilename = syllabus.info.subject + "-" + str(syllabus.info.number) + "-" + term.semester + str(term.year)
                        
                    mySched.put()
                else:                    
                    mySched = CalendarClass(parent = user.key)
                    mySched.schedule.append('Date')
                    mySched.schedule.append('Reading')
                    mySched.schedule.append('Topic')
                    mySched.workingCalendar = True
                    mySched.put()
            else:
                savedCalendars = CalendarClass.query(ancestor=user.key).filter(CalendarClass.workingCalendar == False).fetch()
                queriedCalendars = []
                for i in savedCalendars:
                    queriedCalendars.append(i)
                if mySched:
                    mySched.workingCalendar = False
                    mySched.put()
                mySched = queriedCalendars[int(loadFileName)]
                mySched.workingCalendar = True
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
            if newFileName == mySched.myFilename:                
                for i in range(len(mySched.schedule)):
                    for j in range(3):
                        mySched.setCell(j,i,self.request.get("r"+str(i)+"c"+str(j)))            
            else:
                mySched.workingCalendar = False
                mySched.put()
                mySched = mySched.clone(user.key)
                for i in range(len(mySched.schedule)):
                    for j in range(3):
                        mySched.setCell(j,i,self.request.get("r"+str(i)+"c"+str(j)))            
                mySched.myFilename = newFileName
                mySched.workingCalendar = True
            mySched.put()
            
        return self.redirect('/editcalendar')

