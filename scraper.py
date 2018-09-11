from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

total = 0
def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def get_links():
    url = "https://www.registrar.ucla.edu/Academics/Course-Descriptions#A"
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        links = []
        for li in html.select('td a'):#'#lower, #upper'):
            l = li.get('href')
            links.append('https://www.registrar.ucla.edu'+l)
        return links

    raise Exception('Error retrieving contents at {}'.format(url))

def hasNumbers(inputString):
     return any(char.isdigit() for char in inputString)

def joinMajor(char, l):
    i = 0
    while i < len(l)-1:
        if i>len(l)-1:
            break
        words = [c for c in l[i].split(' ') if c != '']
        if words[len(words)-1][0].isupper() and not hasNumbers(words[len(words)-1]):
            l[i] = char.join([l[i], l[i+1]])
            l.remove(l[i+1])
            i -= 1
        i += 1
    return l

def delParen(s):
    while '(' in s.lower():
        s = s[:s.index('(')] + s[s.index(')')+1:]
    return s

def replaceExceptions(s):
    if "attendance" in s:
        s = ''
    if 'with grade' in s.lower():
        a = s.index('with grade')-1
        b = a + s[a:].index('better')+6 #index of first comma after the 'with grade'
        s = s[:a]+s[b:]
    s = s.replace("at least", "")
    s = s.replace("satisfaction of Entry-Level Writing requirement", "")
    s = s.replace("satisfaction of English as a Second Language requirement", "")
    s = s.replace("proficiency demonstrated on Analytical Writing Placement Examination", "")
    s = s.replace("associated undergraduate lecture course in life sciences", "")
    s = s.replace("successful completion of Mathematics Diagnostic Test", "")
    s = s.replace("two courses in Field III", "")
    s = s.replace(" taken within past three years", "")
    s = s.replace("one statistics Management", "")
    s = s.replace("satisfaction of Writing II requirement", "")
    s = s.replce("with grades of A", "")
    return s

def addSubject(c):
    for i in range(len(c)):
        c[i] = c[i].replace('courses', subject).replace('course', subject)
    wordlist = []
    for i in range(len(c)):
        words = [s for s in c[i].split(' ') if s!='']
        wordlist.append(words)
    if wordlist != [] and len(wordlist[0]) == 1:
        c[0] = subject + ' ' + wordlist[0][0]
    for i in range(len(wordlist)):
        if len(wordlist[i]) == 1:
            j = i - 1
            while len(wordlist[j]) == 1:
                j -= 1
            subj = ' '.join(wordlist[j][:-1])
            c[i] = subj + ' ' + wordlist[i][0]
    return c;


f = open('courses.txt', 'w')

def parse_req(s, subject):
    s = replaceExceptions(s)
    s = delParen(s)

    if "and" not in s and "or" not in s:
        c = [si.strip() for si in s.split(",") if si.strip() != ""]
        c = joinMajor(', ', c)
        for i in range(len(c)):
            if 'from' in c[i]:
                t = c[i].split("from")
        c = addSubject(c)
        print(c)
        f.write(str(c) + '\n')




def parse_des(s,subject):
    ss = [t.strip() for t in s.split('. ') if 'requisite:' in t.lower() or 'requisites:' in t.lower()]
    req = ""
    en = ""
    co = ""
    rec = ""
    for r in ss:
        ty = r[:r.index(":")].lower()
        content = r[r.index(":")+1:]
        parse_req(content, subject)
        if ty == "enforced requisite" or ty == "enforced requisites":
            en = content
        elif ty == "requisite" or ty == "requisites":
            req = content
        elif ty == "recommended requisite" or ty == "recommended requisites":
            rec = content


def get_courses(url):
    response = simple_get(url)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        courses = []
        subject = delParen(html.select('.page-header h1')[1].get_text().strip())
        for div in html.select('#lower, #upper'):
            for d2 in div.select('.media-body'):
                name = d2.find('h3').get_text()
                p = d2.find_all('p')
                units = p[0].get_text()
                description = p[1].get_text()
                parse_des(description,subject)
                courses.append(name)



links = get_links();
#get_courses("https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?SA=MUSC&funsel=3")
# get_courses("https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?SA=CHEM&funsel=3")
for i in range(len(links)):
    get_courses(links[i])
