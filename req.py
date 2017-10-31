# -*- coding: utf-8 -*-  
import requests
from bs4 import BeautifulSoup  
from checkCode import getCheckCode

url  = "http://server1.cdce.cn/student/default.aspx"
stu_url = "http://server1.cdce.cn/Student/StuUpSignInfo.aspx"
file = open('result.txt','a')
session = requests.session()
res = session.post(url=url)
soup = BeautifulSoup(  
    res.text,                   
    'html.parser',              
    from_encoding = 'utf-8'     
)
__VIEWSTATE_value = soup.find_all(id = "__VIEWSTATE")[0]["value"]
__VIEWSTATEGENERATOR_value = soup.find_all(id = "__VIEWSTATEGENERATOR")[0]["value"]
__EVENTVALIDATION_value = soup.find_all(id = "__EVENTVALIDATION")[0]["value"]

check_code_url = "http://server1.cdce.cn/student/" + soup.find_all(id = "imgCodeCtrl")[0]["src"]
check_code_req = session.get(check_code_url)

if check_code_req.status_code == 200:
    open('checkcode.gif', 'wb').write(check_code_req.content)
    check_code = getCheckCode('checkcode.gif')
    post_data = {
        "__VIEWSTATE" : __VIEWSTATE_value,
        "__VIEWSTATEGENERATOR" : __VIEWSTATEGENERATOR_value,
        "__EVENTVALIDATION" : __EVENTVALIDATION_value,
        "txtEmail" : "W518713220029",
        "txtPWD" : "kangyi558",
        "txtCheck" : check_code,
        "btnLogin.x":9,
        "btnLogin.y":15,
        "hid1":"",
    }
    login = session.post(url=url,data = post_data)
    if login.status_code == 200:
        login.encoding = 'gbk'
        soup = BeautifulSoup(  
            login.text,                   
            'html.parser',              
            from_encoding = 'utf-8'     
        )
        frames_len = len(soup.find_all("frame"))
        if (frames_len == 0):
            print "bad"
        else:
            stu_info = session.get(url=stu_url)           
            stu = BeautifulSoup(  
                stu_info.text,                   
                'html.parser',              
                from_encoding = 'utf-8'     
            )
            stu_name = str(stu.find_all(id="lblStuName")[0].text.encode("gbk","ignore"))
            stu_number = str(stu.find_all(id="lblStuNumber")[0].text.encode("gbk","ignore"))                     
            table = stu.find_all(id="ComputerSubjectGridView")[0]
            trs = table.find_all("tr")
            if len(trs) > 1:
                for i,tr in enumerate(trs):
                    if i != 0:
                        tds = tr.find_all("td")
                        td0 = str(tds[0].text.encode("gbk","ignore"))
                        td1 = str(tds[1].text.encode("gbk","ignore"))
                        td5 = str(tds[5].text.encode("gbk","ignore"))
                        td6 = str(tds[6].text.encode("gbk","ignore"))
                        result_text = stu_name +"   "+ stu_number +"    "+ td0 + "    " +td1 + "    " +td5 + "    " +td6 + '\n'                      
                        file.write(result_text)                      
            
        
        
#print soup.find_all('input')[0]['value']
