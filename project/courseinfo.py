import webapp2
import jinja2
import os
from google.appengine.ext import ndb

from webscrape import WebScraper

class Info(ndb.Model):
    title = ndb.StringProperty()
    subject = ndb.StringProperty()
    number = ndb.IntegerProperty()
    section = ndb.IntegerProperty()
    building = ndb.StringProperty()
    room = ndb.StringProperty()
    days = ndb.StringProperty()
    start = ndb.StringProperty()
    end = ndb.StringProperty()
    startDate = ndb.StringProperty()
    endDate = ndb.StringProperty()
    
    @webapp2.cached_property
    def url(self):
        abbr = ""
        if self.subject == "COMPSCI":
            abbr = "CS"
        elif self.subject == "ELECENG":
            abbr = "EE"
        else:
            for c in self.subject:
                abbr = abbr + ("_" if c == " " else c)
        
        return abbr + str(self.number) + "-" + str(self.section)
    
    @webapp2.cached_property
    def number_string(self):
        if self.number < 10:
            return '00' + str(self.number)
        elif self.number < 100:
            return '0' + str(self.number)
        else:
            return str(self.number)
        
    @webapp2.cached_property
    def section_string(self):
        if self.section < 10:
            return '00' + str(self.section)
        elif self.section < 100:
            return '0' + str(self.section)
        else:
            return str(self.section)
    
from basehandler import BaseHandler, login_required, syllabus_required

template_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.getcwd())
    )  
    
class InfoEditHandler(BaseHandler):
    @login_required
    @syllabus_required
    def get(self):
        syllabus = self.current_syllabus
        
        template = template_env.get_template('courseinfo.html')
        context = {
            'info': syllabus.info
        }

        self.response.write(template.render(context))
        
    @login_required
    @syllabus_required
    def post(self):
        term = self.current_term
        syllabus = self.current_syllabus
        
        select = self.request.get('button')
        subject = str(self.request.get('subjectSelect'))
        number = int(self.request.get('courseNumber'))
        section = int(self.request.get('sectionNumber'))
        
        syllabus.info.subject = subject
        syllabus.info.number = number            
        syllabus.info.section = section
        
        if select == 'Rescrape':
            course_list = WebScraper.scrapeCourseNames(str(term.semester), int(term.year), syllabus.info.subject)
            course_name = None
            for c in course_list:
                if WebScraper.getCourseSubjectFromCourseName(c) == str(syllabus.info.subject) and WebScraper.getCourseNumberFromCourseName(c) == syllabus.info.number_string:
                    course_name = c
                    break
                    
            if course_name:
                syllabus.info.title = WebScraper.getCourseTitleFromCourseName(course_name)
            
                sections_list = WebScraper.scrapeCourseSections(str(term.semester), int(term.year), course_name)
                course_section = None
                for s in sections_list:
                    section = WebScraper.getSectionFromCourseSection(s)
                    if section == 'LEC ' + syllabus.info.section_string or section == 'LAB ' + syllabus.info.section_string:
                        course_section = s
                        break
                        
                if course_section:
                    room = WebScraper.getRoomFromCourseSection(course_section)
                    if room:
                        syllabus.info.building = room.split()[0]
                        syllabus.info.room = room.split()[1]
                        
                    syllabus.info.days = WebScraper.getMeetDaysFromCourseSection(course_section)
                    
                    time = WebScraper.getMeetTimeFromCourseSection(course_section)
                    if time:
                        syllabus.info.start = self.military(time.split('-')[0])
                        syllabus.info.end = self.military(time.split('-')[1])
                        
                    instructor = WebScraper.getInstructorFromCourseSection(course_section)
                    if instructor:
                        syllabus.prime = instructor

                    dates = WebScraper.getDatesFromCourseSection(course_section)
                    if dates:
                        syllabus.info.startDate = dates.split('-')[0]
                        syllabus.info.endDate = dates.split('-')[1]
                        
        else:            
            title = str(self.request.get('courseTitle'))
            syllabus.info.title = title
            
            days = ""
            monday = str(self.request.get('mondayCheck'))
            days = days + monday
            tuesday = str(self.request.get('tuesdayCheck'))
            days = days + tuesday
            wednesday = str(self.request.get('wednesdayCheck'))
            days = days + wednesday
            thursday = str(self.request.get('thursdayCheck'))
            days = days + thursday
            friday = str(self.request.get('fridayCheck'))
            days = days + friday
            syllabus.info.days = days
            
            start = str(self.request.get('startTime'))
            syllabus.info.start = start
            
            end = str(self.request.get('endTime'))
            syllabus.info.end = end
            
            building = str(self.request.get('meetingBuilding'))
            syllabus.info.building = building
            
            room = str(self.request.get('meetingRoom'))
            syllabus.info.room = room
        
        syllabus.put()
        
        self.redirect('/#administratorViewCourseTitleMain')
      