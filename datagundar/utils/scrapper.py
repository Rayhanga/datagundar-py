from bs4 import BeautifulSoup as bs
import mechanize

br = mechanize.Browser()
br.set_handle_robots(False)

def httpgetsoup(url, f_para, f_input):
    br.open(url+'?'+f_para+'='+f_input)
    return bs(br.response().read(), "html5lib") 

def scraptable(table, max_col, col):
    r = len(table)
    data = []
    for i in range(col, r, max_col):
        data.append(table[i].text)
    return data