import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from get import get_data as get
from getpass import getpass

session = requests.Session()
siam_home = "https://siam.ub.ac.id/"

def login(username=None, pswd = None, raw=True):
    username = input("Username: ") if username == None else username # implement CLI login
    pswd = getpass(prompt="Password: ") if pswd == None else pswd # input will not be visible
    try:
        parameters = {'username':username, 'password':pswd, 'login':'Masuk'}

        with session.post(siam_home, data=parameters) as r:
            if is_good_response(r):
                if success_login(r):
                    if raw:
                        passreturn (r.text)
                    else:
                        return 0
                else:
                    log_error("Wrong username or password!\nError while trying to login as username: {}".format(username))
            else:
                return None

    except RequestException as e:
        log_error("Error {}".format(str(e)))

def success_login(r):
    html = BeautifulSoup(r.text, 'html.parser')
    return (html.find("input", class_="button") == None)

def is_good_response(r):
    content_type = r.headers['Content-Type'].lower()
    return (r.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    print(e)

def get_bio(username=None):
    return get.biodata(BeautifulSoup(login(username), 'html.parser'))

def get_jadwal(username=None):
    try:
        with session.get(siam_home+"class.php") as r:
            if is_good_response(r):
                return get.jadwal(BeautifulSoup(r.text, 'html.parser'))
            else:
                log_error("Not logged in or session expired!")
    except RequestException as e:
        log_error("Error {} as {}".format(str(e), username))

def get_all_data(username=None, split=True):
    if split:
        return get_bio(username), get_jadwal(username)
    else:
        retr = [[]]
        retr.append(get_bio(username))
        retr.append(get_jadwal(username))
        return retr
