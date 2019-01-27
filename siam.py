import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from get import get_data as get

session = requests.Session()

def login(username, pswd):
    try:
        parameters = {'username':username, 'password':pswd, 'login':'Masuk'}

        with session.post("https://siam.ub.ac.id", data=parameters) as r:
            if is_good_response(r):
                return (r.text)
            else:
                return None

    except RequestException as e:
        log_error("Error {}".format(str(e)))

def is_good_response(r):
    content_type = r.headers['Content-Type'].lower()
    return (r.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    print(e)

def get_bio(username, pswd):
    return get.biodata(BeautifulSoup(login(username, pswd), 'html.parser'))

def get_jadwal(username, pswd):
    try:
        with session.get("https://siam.ub.ac.id/class.php") as r:
            if is_good_response(r):
                return get.jadwal(BeautifulSoup(r.text, 'html.parser'))
            else:
                log_error("Not logged in or session expired!")
    except RequestException as e:
        log_error("Error {} as {}".format(str(e), username))

def get_all_data(username, pswd, split=True):
    if split:
        return get_bio(username, pswd), get_jadwal(username, pswd)
    else:
        retr = [[]]
        retr.append(get_bio(username, pswd))
        retr.append(get_jadwal(username, pswd))
        return retr
