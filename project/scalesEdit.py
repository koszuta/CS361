import jinja2
import webapp2
import os
from google.appengine.ext import ndb

from basehandler import BaseHandler, login_required

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

# create a new grading scale and save to data store
class GradeScale:
	scaleName = ndb.StringProperty()
	onSyllabus = ndb.BooleanProperty(default = False)
	def __init__(self):
		self.scaleName = ""
		self.minAVal = 0
		self.scaleDiff = 0
		self.grades = []
		self.normal = ["A","B","C","D","F"]
		self.half = ["A","A-","B+","B","B-","C+","C","C-","D+","D","D-","F"]
		self.halfScale = False
		self.normScale = False
	def createNewScale(self):
		scaleName = self.scaleName
		minAVal = self.minAVal
		scaleDiff = self.scaleDiff
		
		
		if self.normScale:
			for i in range(0,5):
				print minAVal
				self.grades.append(minAVal)
				minAVal = minAVal - scaleDiff
		if self.halfScale:
			for j in range(0,12):
				print self.minAVal
				self.grades.append(self.minAVal)
				self.minAVal = self.minAVal - self.scaleDiff
				
newScale = GradeScale()


class ScalesHandler(BaseHandler):
	@login_required
	def get(self):
		nScale = []
		hScale = []
		template_values = {
				"minAVal": newScale.minAVal,
				"scaleName": newScale.scaleName,
				"scaleDiff": newScale.scaleDiff,
				"nScale": newScale.normScale,
				"hScale": newScale.halfScale,
				'normalGrades': newScale.normal,
				'halfGrades': newScale.half,
				'grades': newScale.grades
			}
		template = JINJA_ENVIRONMENT.get_template("scalesEdit.html")
		self.response.out.write(template.render(template_values))
		
	@login_required
	def post(self):
		createScale = self.request.get('createScale')
		
		if createScale:
			newScale.scaleDiff = int(self.request.get("scaleDiff"))
			newScale.minAVal = int(self.request.get("minAVal"))
			newScale.scaleName = self.request.get("scaleName")
			scale = self.request.get("scale")
			#This decides which radio button was used
			if scale == "normScale":
				newScale.normScale = True
			elif scale == "halfScale":
				newScale.halfScale = True
				
			newScale.createNewScale()
		self.redirect("/editscales")