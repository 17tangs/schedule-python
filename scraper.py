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


def joinMajor(char, l):
    i = 0
    while i < len(l)-1:
        if i>len(l)-1:
            break
        words = [c for c in l[i].split(' ') if c != '']
        if words[len(words)-1][0].isupper():
            l[i] = char.join([l[i], l[i+1]])
            l.remove(l[i+1])
            i -= 1
        i += 1
    return l




def parse_req(s):
    f = open('exceptions.txt', 'a');
    f2 = open('more.txt','a');
    #get rid of grade requirement, which messes up 'and' parsing
    if 'with grades of a' in s.lower():
        a = s.index('with grade')-1
        s = s[:a] + s[a+16:]
    elif 'with grade' in s.lower():
        a = s.index('with grade')-1
        b = a + s[a:].index('better')+6 #index of first comma after the 'with grade'
        s = s[:a]+s[b:]
    #get rid of parentheses which also mess up 'and' parsing
    while '(' in s.lower():
        s = s[:s.index('(')] + s[s.index(')')+1:]

    if "and" not in s and "or" not in s:
        c = [si.strip() for si in s.split(",")]
        c = joinMajor(', ', c)
        print(c)

    #parse 'and'
    if "and" in s or "or" in s:
        l = s.split("and")
        i = 0
        while i < len(l)-1:
            if i>len(l)-1:
                break
            words = [c for c in l[i].split(' ') if c != '']
            if words[len(words)-1][0].isupper():
                l[i] = 'and'.join([l[i], l[i+1]])
                l.remove(l[i+1])
                i -= 1
            i += 1



def parse_des(s):
    ss = [t.strip() for t in s.split('. ') if 'requisite:' in t.lower() or 'requisites:' in t.lower()]
    req = ""
    en = ""
    co = ""
    rec = ""
    for r in ss:
        ty = r[:r.index(":")].lower()
        content = r[r.index(":")+1:]
        parse_req(content)
        if ty == "enforced requisite" or ty == "enforced requisites":
            en = content
        elif ty == "requisite" or ty == "requisites":
            req = content
        elif ty == "recommended requisite" or ty == "recommended requisites":
            rec = content
    # print("requisites:   " + req)
    # print("enforced:     " + en)
    # print("recommended:    " + rec + '\n')


def get_courses(url):
    response = simple_get(url)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        courses = []
        print(html.select('.page-header h1')[1].get_text())
        for div in html.select('#lower, #upper'):
            for d2 in div.select('.media-body'):
                name = d2.find('h3').get_text()
                p = d2.find_all('p')
                units = p[0].get_text()
                description = p[1].get_text()
                parse_des(description)
                courses.append(name)



links = get_links();
#get_courses("https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?SA=MUSC&funsel=3")
# get_courses("https://www.registrar.ucla.edu/Academics/Course-Descriptions/Course-Details?SA=CHEM&funsel=3")
for i in range(len(links)):
    get_courses(links[i])
