#WebScraper class v2.0
import urllib
import re

class WebScraper():
    
    @staticmethod
    def scrapeLinksFromUrl(url):
        #returns list of links found at given url
        links = []
        if type(url) is str:
            try:
                page = urllib.urlopen(url)
                pageText = page.read()
                page.close()
                regex = '<\s*a(.+?)>'
                pattern = re.compile(regex)
                regex = 'href\s*=\s*\"(.+?)\"'
                urlPattern = re.compile(regex)
                atags = re.findall(pattern, pageText)

                for i in atags:
                    temp = re.findall(urlPattern, i)
                    for j in temp:
                        if len(j) > 0:
                            links.append(j)
            except:
                links = []
        
        return links

    @staticmethod
    def scrapeStringsOutisdeOfAllTagsFromUrl(url):
        #returns any string of the form "> ... <"
        #from given url. this will tend to be 
        #strings that are not within any tags
        outerStrings = []
        if type(url) is str:
            try:
                page = urllib.urlopen(url)
                pageText = page.read()
                page.close()
                outsideTagRegEx = '>(.+?)<'
                outsideTagRegExPattern = re.compile(outsideTagRegEx)
                insideTag = re.compile('<.*?>')
                outerStringsTemp = re.findall(outsideTagRegExPattern, pageText)
                for i in outerStringsTemp:
                    tempStr = i
                    tempStr = re.sub(insideTag, '', tempStr)
                    if len(tempStr) > 0:
                        outerStrings.append(tempStr)
                        
            except:
                outerStrings = []
        
        return outerStrings

    @staticmethod
    def scrapeStringsOutisdeOfTargetTagFromUrl(url, tag):
        #returns any string of the form "> ... <"
        #from given url. this will tend to be 
        #strings that are not within any tags
        outerStrings = []
        if (type(url) is str) and (type(tag) is str):
            try:
                page = urllib.urlopen(url)
                pageText = page.read()
                page.close()
                outsideTagRegEx = '>(.+?)<\s*/\s*'+tag
                outsideTagRegExPattern = re.compile(outsideTagRegEx)
                insideTag = re.compile('<.*?>')
                outerStringsTemp = re.findall(outsideTagRegExPattern, pageText)
                for i in outerStringsTemp:
                    tempStr = i
                    tempStr = re.sub(insideTag, '', tempStr)
                    if len(tempStr) > 0:
                        outerStrings.append(tempStr)
                        
            except:
                outerStrings = []
        
        return outerStrings

    @staticmethod
    def scrapeStringsBetweenTwoRegExsFromUrl(url, startRegEx, endRegEx):
        #returns all text occuring between instances of startRegEx 
        #and endRegEx from given url
        #print "please wait: retrieving data from " + url
        innerStrings = []
        if (type(url) is str) and (type(startRegEx) is str) and (type(endRegEx) is str):
            #try:
            page = urllib.urlopen(url)
            pageText = page.read()
            page.close()
            allWhiteSpace = re.compile('\s+')
            pageText = re.sub(allWhiteSpace, ' ', pageText)
            surroundingRegEx = startRegEx+"(.+?)"+endRegEx
            surroundingTagRegExPattern = re.compile(surroundingRegEx)
            innerStringsTemp = re.findall(surroundingTagRegExPattern, pageText)
            for i in innerStringsTemp:
                tempStr = i.strip(' ')
                innerStrings.append(tempStr)
                        
            #except:
            #    print "error occured"
            #    innerStrings = []
        
        return innerStrings
        
    @staticmethod
    def scrapeStringsBetweenTwoRegExsFromString(myString, startRegEx, endRegEx):
        #returns all text occuring between instances of startRegEx 
        #and endRegEx from given myString
        #print "please wait: retrieving data from " + myString
        innerStrings = []
        if (type(myString) is str) and (type(startRegEx) is str) and (type(endRegEx) is str):
            pageText = myString
            surroundingRegEx = startRegEx+"(.+?)"+endRegEx
            surroundingTagRegExPattern = re.compile(surroundingRegEx)
            innerStringsTemp = re.findall(surroundingTagRegExPattern, pageText)
            for i in innerStringsTemp:
                tempStr = i.strip(' ')
                innerStrings.append(tempStr)
        
        return innerStrings
        
    @staticmethod
    def scrapeStringsWithinTargetTagFromUrl(url, tag):
        if (type(url) is str) and (type(tag) is str):
            scrapedStrings = []
            try:
                page = urllib.urlopen(url)
                pageText = page.read()
                page.close()
                tagRegEx = '<\s*'+tag+'(.+?)>'
                tagRegExPattern = re.compile(tagRegEx)
                quoteRegEx = '\"(.+?)\"'
                quoteRegExPattern = re.compile(quoteRegEx)
                
                targetedTags = re.findall(tagRegExPattern, pageText)
                
                for i in targetedTags:
                    foundStrings = re.findall(quoteRegExPattern, i)
                    for j in foundStrings:
                        scrapedStrings.append(j)
                        
            except:
                scrapedStrings = []
                
        return scrapedStrings
        
    @staticmethod
    def scrapeTagHtml(url, tagString, tagType):
        #searches url for tags matching tag
        #returns all html within that tag
        #matching tags
        if (type(url) is str) and (type(tagString) is str) and (type(tagType) is str):
            scrapedHtml = []
            openTag = '<'+tagType
            closeTag = '</'+tagType+'>'

            page = urllib.urlopen(url)
            pageText = page.read()
            page.close()

            allWhiteSpace = re.compile('\s+')
            pageText = re.sub(allWhiteSpace, ' ', pageText)
            
            index = pageText.find(tagString)
            #print index
            while index > -1:
                endIndex = index+len(tagString)
                openTags = 0
                while (openTags > -1) and (endIndex < (len(pageText))):
                    lookAhead = ""
                    for i in range(0,len(closeTag)):
                        lookAhead = lookAhead + pageText[endIndex+i]
                    if lookAhead.find(openTag) > -1:
                        openTags = openTags + 1
                        endIndex = endIndex + len(lookAhead)-1
                    elif lookAhead.find(closeTag) > -1:
                        openTags = openTags -1
                        endIndex = endIndex + len(lookAhead)-1
                    endIndex = endIndex+1

                scrapedHtml.append(pageText[index:endIndex])
                pageText = pageText[:index]+ pageText[endIndex:]    
                index = pageText.find(tagString)
                #print index

                
        return scrapedHtml
        
    @staticmethod
    def scrapeCourseSections(term, year, courseName):
        #example:
        #>>WebScraper.scrapeCourseSections('Spring', 2016, 'MATH-231: Calculus and Analytic Geometry I (4 units; U ; NS,QLB)')
        # ['NS,QLB; None; 4; LEC 001; 48669; 8:00 AM-9:15 AM; MWF; 01/25-05/10; None; EMS E237; None;',
        # 'NS,QLB; None; 4; LEC 002; 48670; 9:30 AM-10:45 AM; MWF; 01/25-05/10; Hruska, Geoffrey; EMS E237; None;',
        # ...,
        # 'NS,QLB; None; 4; LEC 010; 49321; 5:00 PM-6:50 PM; TR; 01/25-05/10; Boyd, Suzanne; EMS E295; None;',
        # 'NS,QLB; None; 4; LEC 011; 54356; 11:00 AM-12:50 PM; MW; 01/25-05/10; Winarski, Rebecca; EMS E237; None;']
        subject = WebScraper.getCourseSubjectFromCourseName(courseName)
        courseNumber = WebScraper.getCourseNumberFromCourseName(courseName)
        
        allCourseNames = WebScraper.scrapeCourseNames(term, year, subject)
        determinedCourse = False
        determinedCourseIndex = 0
        index = 0
        for i in allCourseNames:
            if courseNumber in i:
                determinedCourse = True
                determinedCourseIndex = index
            index = index + 1
        
        htmlSection = ''
        url = WebScraper.buildTermYearSubjectUWMUrl(term, year, subject)
        sectionData = []
        sections = []
        if determinedCourse:
            htmlSections = WebScraper.scrapeTagHtml(url, '<div> <!-- **** start content **** -->', 'div')
            if len(htmlSections) >= (determinedCourseIndex+1):
                tdStr1 = '<td style=\"border-top:1px solid #CCCCCC;\">'
                tdStr2 = '<td style=\"\">'
                htmlSection = htmlSections[determinedCourseIndex]
                tempSectionData = WebScraper.scrapeStringsBetweenTwoRegExsFromString(htmlSection, '['+tdStr1+'|'+tdStr2+']', '</td>')
                if tempSectionData:
                    for i in tempSectionData:
                        tempStr = i
                        tempStr = re.sub(r'(.+?)>', '', tempStr)
                        tempStr = re.sub(r'<(.+?)', '', tempStr)
                        tempStr = re.sub(r'&nbsp;', 'None', tempStr)
                        if tempStr != '':
                            sectionData.append(tempStr.strip(' '))
                            
                    counter = 0
                    section = ''
                    for i in reversed(sectionData):
                        section = i + "; " + section
                        counter = counter + 1
                        if counter == 11:
                            sections.insert(0, section.strip(' '))
                            counter = 0
                            section = ''
               
        return sections
        
    @staticmethod
    def scrapeCourseNames(term, year, subject):
        #example:
        #>>WebScraper.scrapeCourseNames('UWinteriM', 2016, 'MATH')
        #['MATH 103(106): Contemporary Applications of Mathematics',
        #   'MATH-105: Intermediate Algebra',
        #   'MATH-116: College Algebra'
        #   'MATH-117: Trigonometry']
        courseTitles = []
        url = WebScraper.buildTermYearSubjectUWMUrl(term, year, subject)
        if url != '':
            startRegEx = '<span\s*class=\"subhead\">'
            endRegEx = '</span>'
            tempCourseTitles = WebScraper.scrapeStringsBetweenTwoRegExsFromUrl(url, startRegEx, endRegEx)
            for i in tempCourseTitles:
                tempStr = i
                tempStr = re.sub(r'%20', ' ', tempStr)
                tempStr = re.sub(r'%26', '&', tempStr)
                courseTitles.append(tempStr)
        else:
            print 'invalid url'

        return courseTitles

    @staticmethod
    def splitCourseSection(courseSection):
        #example:
        #>>WebScraper.splitCourseName('NS,QLB; None; 4; LEC 002; 48670; 9:30 AM-10:45 AM; MWF; 01/25-05/10; Hruska, Geoffrey; EMS E237; None;')
        #['NS,QLB',
        # 'None',
        # '4'
        # ...,
        # 'EMS E237', 
        # 'None']
        splitSection = []
        tempSplitSections = re.split(';', courseSection)
        for i in tempSplitSections:
            tempStr = i
            splitSection.append(tempStr.strip(' '))
            
        return splitSection
        
    @staticmethod
    def getGERFromCourseSection(courseSection):        
        #example:
        
        ret = ''
        splitSection = WebScraper.splitCourseSection(courseSection)
        if len(splitSection) > 0:
            ret = splitSection[0]
            
        return ret
        
    @staticmethod
    def getUnitsFromCourseSection(courseSection):        
        #example:
        #>>WebScraper.getUnitsFromCourseSection('NS,QLB; None; 4; LEC 002; 48670; 9:30 AM-10:45 AM; MWF; 01/25-05/10; Hruska, Geoffrey; EMS E237; None;')
        #'NS,QLB'        
        ret = ''
        splitSection = WebScraper.splitCourseSection(courseSection)
        if len(splitSection) > 2:
            ret = splitSection[2]
            
        return ret

    @staticmethod
    def getSectionFromCourseSection(courseSection):        
        #example:
        ret = ''
        splitSection = WebScraper.splitCourseSection(courseSection)
        if len(splitSection) > 3:
            ret = splitSection[3]
            
        return ret
        
    @staticmethod
    def getClassNumberFromCourseSection(courseSection):        
        #example:
        
        ret = ''
        splitSection = WebScraper.splitCourseSection(courseSection)
        if len(splitSection) > 4:
            ret = splitSection[4]
            
        return ret
        
    @staticmethod
    def getMeetTimeFromCourseSection(courseSection):        
        #example:
        
        ret = ''
        splitSection = WebScraper.splitCourseSection(courseSection)
        if len(splitSection) > 5:
            ret = splitSection[5]
            
        return ret
        
    @staticmethod
    def getMeetDaysFromCourseSection(courseSection):        
        #example:
        
        ret = ''
        splitSection = WebScraper.splitCourseSection(courseSection)
        if len(splitSection) > 6:
            ret = splitSection[6]
            
        return ret
        
    @staticmethod
    def getDatesFromCourseSection(courseSection):        
        #example:
        
        ret = ''
        splitSection = WebScraper.splitCourseSection(courseSection)
        if len(splitSection) > 7:
            ret = splitSection[7]
            
        return ret
        
    @staticmethod
    def getInstructorFromCourseSection(courseSection):        
        #example:
        
        ret = ''
        splitSection = WebScraper.splitCourseSection(courseSection)
        if len(splitSection) > 8:
            ret = splitSection[8]
            
        return ret

    @staticmethod
    def getRoomFromCourseSection(courseSection):        
        #example:
        
        ret = ''
        splitSection = WebScraper.splitCourseSection(courseSection)
        if len(splitSection) > 9:
            ret = splitSection[9]
            
        return ret
        
       
    @staticmethod
    def splitCourseName(courseName):
        #example:
        #>>WebScraper.splitCourseName('COMPSCI-361: Intro to software engineering')
        #['COMPSCI', '361', 'Intro to software engineering']
        courseName = re.sub(r':', ' ', courseName)
        courseName = re.sub(r'-', ' ', courseName)
        courseName = re.sub(r'\(.*?\)', ' ', courseName)
        deptAndNumberOrTitle = re.split('  ', courseName)
        number = re.findall(r'\d+', deptAndNumberOrTitle[0])
        deptAndNumberOrTitle[0] = re.sub(number[0], '', deptAndNumberOrTitle[0])
        splitCourseName = []
        splitCourseName.append(deptAndNumberOrTitle[0].strip(' '))
        splitCourseName.append(number[0].strip(' '))
        splitCourseName.append(deptAndNumberOrTitle[1].strip(' '))
        
        return splitCourseName

    @staticmethod
    def getCourseSubjectFromCourseName(courseName):
        #example:
        #>>WebScraper.getCourseDepartmentFromCourseName('COMPSCI-361: Intro to software engineering')
        #'COMPSCI'
        splitName = WebScraper.splitCourseName(courseName)
        retStr = ''
        if len(splitName) == 3:
            retStr = splitName[0]
            
        return retStr

    @staticmethod
    def getCourseNumberFromCourseName(courseName):
        #example:
        #>>WebScraper.getCourseNumberFromCourseName('COMPSCI-361: Intro to software engineering')
        #'361'
        splitName = WebScraper.splitCourseName(courseName)
        retStr = ''
        if len(splitName) == 3:
            retStr = splitName[1]

        return retStr

    @staticmethod
    def getCourseTitleFromCourseName(courseName):
        #example:
        #>>WebScraper.getCourseTitleFromCourseName('COMPSCI-361: Intro to software engineering')
        #'Intro to software engineering'
        splitName = WebScraper.splitCourseName(courseName)
        retStr = ''
        if len(splitName) == 3:
            retStr = splitName[2]

        return retStr
            

    @staticmethod
    def scrapeSubjectNames(term, year):
        #example:
        #>>WebScraper.scrapeSubjectNames('Spring', 2016)
        #['AOCMDSP', 'AD LDSP', 'AFRICOL', ..., 'WASHINGTONMDSP', 'WGS']
        deptNames = []
        url = WebScraper.buildTermYearUWMUrl(term, year)
        if url != '':
            startRegEx = "subject="
            endRegEx = "&strm="
            tempDeptNames = WebScraper.scrapeStringsBetweenTwoRegExsFromUrl(url, startRegEx, endRegEx)
            for i in tempDeptNames:
                tempStr = i
                tempStr = re.sub(r'%20', ' ', tempStr)
                tempStr = re.sub(r'%26', '&', tempStr)
                deptNames.append(tempStr)
        else:
            print 'invalid url'
            
        return deptNames
            
        
    @staticmethod    
    def buildTermYearUWMUrl(term, year):
    
        valid = True
        termCode = ''
        yearStr = str(year)
        if type(term) is str:
            if (term == 'Summer'):
                termCode = '6'
            elif (term == 'Fall'):
                termCode = '9'
            elif (term == 'UWinteriM'):
                termCode = '1'
            elif (term == 'Spring'):
                termCode = '2'
            else:
                valid = False
                
        if len(yearStr) == 4:
            yearStr = yearStr[0] + yearStr[2] + yearStr[3]
        else:
            valid = False
            
        strm = yearStr + termCode
        
        url = "http://www4.uwm.edu/schedule/index.cfm?a1=browse&strm="
        url = url + strm
        url = url + "&term_descr="
        url = url + term
        url = url + "%20"
        url = url + str(year)
        url = url + "&term_status=L"
        
        if valid == False:
            url = ''
            
        return url
        
    @staticmethod
    def buildTermYearSubjectUWMUrl(term, year, subject):

        valid = True
        termCode = ''
        yearStr = str(year)
        if type(term) is str:
            if (term == 'Summer'):
                termCode = '6'
            elif (term == 'Fall'):
                termCode = '9'
            elif (term == 'UWinteriM'):
                termCode = '1'
            elif (term == 'Spring'):
                termCode = '2'
            else:
                valid = False
                
        if len(yearStr) == 4:
            yearStr = yearStr[0] + yearStr[2] + yearStr[3]
        else:
            valid = False
            
        strm = yearStr + termCode
        
        subject = re.sub(r' ', '%20', subject)
        subject = re.sub(r'&', '%26', subject)

        url = "http://www4.uwm.edu/schedule/index.cfm?a1=subject_details&subject="
        url = url + subject
        url = url + "&strm="
        url = url + strm
        
        if valid == False:
            url = ''
            
        return url
        
#demo
print "WebScraper Demo:"
print "please wait..."
subjectNamesFall2015 = WebScraper.scrapeSubjectNames('Fall', 2015)
for i in subjectNamesFall2015:
    print "     " + i
print "retrieved with WebScraper.scrapeSubjectNames('Fall', 2015)"
print 
print "please wait..."
artClassesUWinteriM2016 = WebScraper.scrapeCourseNames('UWinteriM', 2016, 'ART')
for i in artClassesUWinteriM2016:
    print "     " + i
print "retrieved with WebScraper.scrapeCourseNames('UWinteriM', 2016, 'ART'))"
print
print "please wait..."    
sections = WebScraper.scrapeCourseSections('Spring', 2016, 'MATH-231: Calculus and Analytic Geometry I (4 units; U ; NS,QLB)')
for i in sections:
    print i
print "retrieved with WebScraper.scrapeCourseSections('Spring', 2016, 'MATH-231: Calculus and Analytic Geometry I (4 units; U ; NS,QLB)')"

