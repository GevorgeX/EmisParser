import time
import requests
from bs4 import BeautifulSoup as bs


def main():
    ses = requests.Session()

    def autorization(siteUrl: str, logUrl: str, mail: str, password: str):
        authReq = ses.get(siteUrl) # autorizatiayi ej
        scrf = bs(authReq.content, 'lxml').select("input[name=csrf_token]")[0]["value"] # stanumenq scrf token

        info = {
            'csrf_token': scrf,
            'email': mail,
            'password': password
        }
        req = ses.post(logUrl, data=info) # logining

    autorization('https://e-diary.emis.am/auth', 'https://e-diary.emis.am/auth/SignIn', 'ellamartirosyan@mail.ru',
                 'garnik1960')

    authReq = ses.get('https://e-diary.emis.am/index.php/children') #gnumenq children ej
    soup = bs(authReq.content, 'lxml') #stanum ejy
    kojak = soup.findAll('div', class_='set-btn mt-3')  # stanumenq knopkeq (2 hat)
    gnahatakaniEj = ses.get(kojak[0].find('a').get('href'))  # gnumenq gnahatakanneri ej
    url = 'https://e-diary.emis.am/diary/getDiaryData'
    info = {
        'csrf_token': bs(authReq.content, 'lxml').select("input[name=csrf_token]")[0]["value"],
        'education_year': '2021-2022',
        'month': '1',
        'semester': '2',
        'diary_search': 'Հաստատել',
        'student_id': bs(gnahatakaniEj.content, 'lxml').select("input[name=student_id]")[0]["value"],
        'school_id': bs(gnahatakaniEj.content, 'lxml').select("input[name=school_id]")[0]["value"],
        'classroom_id': bs(gnahatakaniEj.content, 'lxml').select("input[name=classroom_id]")[0]["value"]

    }
    ses.post(f"https://e-diary.emis.am/diary/index/{info['student_id']}/{info['school_id']}/{info['classroom_id']}",
             data=info)  #gnum gnahatakani ejy
    info = {
        'csrf_token': bs(authReq.content, 'lxml').select("input[name=csrf_token]")[0]["value"],
        'weekday': '23',
        'student_id': bs(gnahatakaniEj.content, 'lxml').select("input[name=student_id]")[0]["value"],
        'school_id': bs(gnahatakaniEj.content, 'lxml').select("input[name=school_id]")[0]["value"],
        'classroom_id': bs(gnahatakaniEj.content, 'lxml').select("input[name=classroom_id]")[0]["value"]
    }
    req = ses.post('https://e-diary.emis.am/diary/getDiaryData', data=info).content
    req = bytes(str(req[9:-2]),encoding='utf8')
    a = bs(req,'lxml')
    print(a)


if __name__ == '__main__':
    main()