import copy
class Course:
    def __init__(self, m_name, m_number, m_unit, m_description, m_type=''):
        self.name = m_name
        self.number = m_number
        self.unit = m_unit
        self.description = m_description
        self.ty = m_type
        self.children = []
        self.degree = 0

    def __eq__(self, other):
        return self.number == other.number

    def __str__(self):
        return "Course number: " + self.number + "\nCourse Title: " + self.name + "\nCourse units: " + self.unit + "\nCourse description: " + self.description + '\n'


    def addEdge(self, n):
        sefl.chidlren.append(n)


    def addRelation(self, cs):
        s = ''
        d = self.description.lower()
        if "requisites: " in d:
            s = d[d.index("requisites: ")+12: ]
            s = s[:s.index('.')]
        elif "requisite: " in d.lower():
            s = d[d.index("requisite: ")+11: ]
            s = s[:s.index('.')]
        s = s[s.index(' ')+1:]
        s = s.split(', ')
        for l in s:
            for c in cs:
                if l == c.number.lower():
                    self.children.append(c)
                    c.degree += 1


def parseCourses():
    f = open('data.txt', 'r')
    raw = [s for s in f.read().split('\n') if s!='']
    for i in range(len(raw)):
        if raw[i][0] == '(':
            raw[i] = raw[i][raw[i].index(')')+2:]



    courseData = []
    course = []
    for i in range(len(raw)):
        if(i%3 == 2):
            course.append(raw[i])
            courseData.append(course)
            course = []
        else:
            course.append(raw[i])

    courses = []
    for c in courseData:
        course = Course(c[0][c[0].index(' ')+1:],   c[0][:c[0].index('.')],   c[1][c[1].index(' ')+1:],c[2],)
        courses.append(course)

    return courses





courses = parseCourses()
graph = []
for c in courses:
    if "requisite: " in c.description.lower() or "requisites" in c.description.lower():
        graph.append(c)
for c in graph:
    c.addRelation(courses)


#for c in courses:
#    print(c.number + ": ")
#    for child in c.children:
#        print(child.number)




def dep_resolve(node, resolved):
   for edge in node.children:
       if edge not in resolved:
          dep_resolve(edge, resolved)
   resolved.append(node)



for i in range(len(courses)):
    print(courses[i].name + " "  + courses[i].number)
    resolved = []
    dep_resolve(courses[i], resolved)
    for node in resolved:
        print node.number
