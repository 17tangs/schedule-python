
class Subject:
    def __init__(self, m_name, m_id, m_courses=None):
        self.name = m_name
        self.id = m_id
        self.m_courses = m_courses


class Course:
    def __init__(self, m_name, m_id, m_unit, m_description, m_type=''):
        self.name = m_name
        self.id = m_id
        self.unit = m_unit
        self.description = m_description
        self.ty = m_type
        self.children = []

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return "Course number: " + self.id + "\nCourse Title: " + self.name + "\nCourse units: " + self.unit + "\nCourse description: " + self.description + '\n'


class Requisite:
    def __init__(self, m_name, m_number, m_courses=None):
        self.name = m_name
        self.number = m_number
        self.courses = m_courses if m_courses != None else []

    def __str__(self):
        if self.courses == []:
            return str(self.name);
        else:
            s = ""
            for i in self.courses:
                s += str(i) + ', '
        return "choose " + str(self.number) + " courses from " + s
