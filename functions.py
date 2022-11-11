import jaconv
from bs4 import BeautifulSoup
from urllib import request
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.support.ui import WebDriverWait


#ダジャレステーションからスクレイピングする関数-----------------------------------------------------------------------
# def scraping():
#     response = request.urlopen("https://dajare.jp/search/")
#     soup = BeautifulSoup(response)
#     aidhi = soup.find(id="PanelWorkRankingTotal")
#     dajare_lst=[]
#     for item in aidhi.find_all("td", "List ListWorkBody"):
#         dajare_lst.append(item.find("a").text)
#     return dajare_lst
# print(scraping())

#ダジャレステーションからスクレイピングする関数-----------------------------------------------------------------------
def scraping():
    options = Options()
    #下記2行は「ERROR:device_event_log_impl.cc(214)] [23:00:30.947] USB: usb_device_handle_win.cc:1048 Failed to read descriptor from node connection: システムに接続されたデバイスが機能していません。」というエラーをなくすため
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.use_chromium = True
    # options.headless = True

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # driver.implicitly_wait(10) #「selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element:」というエラーを避けるための暗黙的な待機。指定した時間を最大で待機し、要素が見つかったらその時点で待機するのを止めて処理を続ける。

    driver.get("https://dajare.jp/#Search")

    elem = driver.find_element(By.ID, "PanelSearchMenuHeaderButton") #find_elements_by_*系メソッドはseleniumのバージョン4.3.0で廃止された
    elem = elem.find_element(By.CLASS_NAME, "LabelDefault") 
    elem.click()

    select=driver.find_element(By.ID,"ViewOrder")
    select=Select(select)
    select.select_by_value('EvaluationNumberDescending')

    search=driver.find_element(By.CSS_SELECTOR,"#PanelSearchMenuBody .PanelFormButton.PanelFormButtonTop.PanelFormButtonBottom.PanelFade.PanelFadeIn a.LabelAnchor.LabelAnchorIcon.LabelAnchorIconSearch") #クラス名の空白は「.」に置き換える
    search.click()

    #上2行と同じ挙動を示す操作
    # element = driver.find_element(By.ID,'FormSearch')
    # element.submit()

    time.sleep(10)

    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    print(soup)

    # driver.quit()

    # chrome_service = fs.Service(executable_path='C:￥chromedriver_win32￥chromedriver.exe')
    # driver = webdriver.Chrome(service=chrome_service)
    # driver.get("https://dajare.jp/#Search")
    # elem_search_word = driver.find_element_by_class_name("LabelDefault")
    # print(elem_search_word)

# scraping()

#文字列の中に何文字のダジャレ（同じ読みの繰り返し）が何個あるかを数える関数--------------------------------------------
def count(i,output,function_name):
    lst=[output[j:j+i] for j in range(0,len(output)-i+1)]
    for k in range(len(lst)):
        num=lst.count(lst[k])
        if num>=2:
            # x=str(i)+"文字"
            # y=str(num)+"個"
            return lst[k],i,num,function_name

#最も文字数の多いダジャレ（同じ読みの繰り返し）を出力する関数------------------------------------------
# def judge(no_symbol):
#     n=len(no_symbol)//2
#     if n<2:
#         return "文字数が少ないのでダジャレじゃない可能性が高いです"
#     else:
#         for i in range(n,1,-1):
#             result=[]
#             output=no_symbol
#             result.append(count(i,output,"nothing"))
            
#             output=macron_to_vowel(no_symbol)
#             result.append(count(i,output,"macron_to_vowel"))
                    
#             output=macron_to_vowel_iu(no_symbol)
#             result.append(count(i,output,"macron_to_vowel_iu"))
            
#             output=delete_macron(no_symbol)
#             result.append(count(i,output,"delete_macron"))

#             output=delete_smalltu(no_symbol)
#             result.append(count(i,output,"delete_smalltu"))

#             output=delete_small(no_symbol)
#             result.append(count(i,output,"delete_small"))

#             output=small_to_capital(no_symbol)
#             result.append(count(i,output,"small_to_capital"))

#             output=delete_voiced_semivoiced_sound(no_symbol)
#             result.append(count(i,output,"delete_voiced_semivoiced_sound"))
            
#             print(result)
            # return "ダジャレではない可能性が高いです"

#最も文字数の多いダジャレ（同じ読みの繰り返し）を出力する関数------------------------------------------
def judge(no_symbol,s):
    n=len(no_symbol)//2
    a=1
    if n<2:
        return f"【{s}】は文字数が少ないのでダジャレではない可能性があります",a,no_symbol
    else:
        for i in range(n,1,-1):
            output=no_symbol
            result=count(i,output,"nothing")
            if result:
                return result
            elif True:
                output=macron_to_vowel(no_symbol)
                result=count(i,output,"macron_to_vowel")
                if result:
                    return result
                elif True:
                    output=macron_to_vowel_iu(no_symbol)
                    result=count(i,output,"macron_to_vowel_iu")
                    if result:
                        return result
                    elif True:
                        output=delete_macron(no_symbol)
                        result=count(i,output,"delete_macron")
                        if result:
                            return result
                        elif True:
                            output=delete_smalltu(no_symbol)
                            result=count(i,output,"delete_smalltu")
                            if result:
                                return result
                            elif True:
                                output=delete_small(no_symbol)
                                result=count(i,output,"delete_small")
                                if result:
                                    return result
                                elif True:
                                    output=small_to_capital(no_symbol)
                                    result=count(i,output,"small_to_capital")
                                    if result:
                                        return result
                                    elif True:
                                        output=delete_voiced_semivoiced_sound(no_symbol)
                                        result=count(i,output,"delete_voiced_semivoiced_sound")
                                        if result:
                                            return result
                                        elif i==2:
                                            return f"【{s}】はダジャレではない可能性があります",a,no_symbol

#伸ばし棒を直前の文字の母音に置き換える----------------------------------------------------------------------------
def macron_to_vowel(no_symbol):
    lst=list(no_symbol)
    index=[i for i,w in enumerate(lst) if w=="ー"]
    for i in index:
        if lst[i-1] in ["ア","カ","サ","タ","ナ","ハ","マ","ヤ","ラ","ワ","ガ","ザ","ダ","バ","パ","ァ","ャ"]:
            lst[i]="ア"
        elif lst[i-1] in ["イ","キ","シ","チ","ニ","ヒ","ミ","リ","ギ","ジ","ヂ","ビ","ピ","ィ"]:
            lst[i]="イ"
        elif lst[i-1] in ["ウ","ク","ス","ツ","ヌ","フ","ム","ユ","ル","グ","ズ","ヅ","ブ","プ","ゥ","ュ"]:
            lst[i]="ウ"
        elif lst[i-1] in ["エ","ケ","セ","テ","ネ","ヘ","メ","レ","ゲ","ゼ","デ","ベ","ペ","ェ"]:
            lst[i]="エ"
        elif lst[i-1] in ["オ","コ","ソ","ト","ノ","ホ","モ","ヨ","ロ","ゴ","ゾ","ド","ボ","ポ","ォ","ョ"]:
            lst[i]="オ"
    macron_to_vowel="".join(lst)
    return macron_to_vowel
# print(macron_to_vowel())

#伸ばし棒の直前の文字の母音が「エ」「オ」の場合、伸ばし棒を「イ」「ウ」に置き換える----------------------------------
def macron_to_vowel_iu(no_symbol):
    lst=list(no_symbol)
    index=[i for i,w in enumerate(lst) if w=="ー"]
    for i in index:
        if lst[i-1] in ["ア","カ","サ","タ","ナ","ハ","マ","ヤ","ラ","ワ","ガ","ザ","ダ","バ","パ","ァ","ャ"]:
            lst[i]="ア"
        elif lst[i-1] in ["イ","キ","シ","チ","ニ","ヒ","ミ","リ","ギ","ジ","ヂ","ビ","ピ","ィ"]:
            lst[i]="イ"
        elif lst[i-1] in ["ウ","ク","ス","ツ","ヌ","フ","ム","ユ","ル","グ","ズ","ヅ","ブ","プ","ゥ","ュ"]:
            lst[i]="ウ"
        elif lst[i-1] in ["エ","ケ","セ","テ","ネ","ヘ","メ","レ","ゲ","ゼ","デ","ベ","ペ","ェ"]:
            lst[i]="イ"
        elif lst[i-1] in ["オ","コ","ソ","ト","ノ","ホ","モ","ヨ","ロ","ゴ","ゾ","ド","ボ","ポ","ォ","ョ"]:
            lst[i]="ウ"
    macron_to_vowel_iu="".join(lst)
    return macron_to_vowel_iu
# print(macron_to_vowel_iu())

#伸ばし棒を削除する-----------------------------------------------------------------------------------------------
def delete_macron(no_symbol):
    delete_macron=no_symbol.replace("ー","")
    return delete_macron
# print(delete_macron())

#小さい「ツ」を削除する--------------------------------------------------------------------------------------------
def delete_smalltu(no_symbol):
    delete_smalltu=no_symbol.replace("ッ","")
    return delete_smalltu
# print(delete_smalltu())

#小文字をすべて削除する----------------------------------------------------------------------------------------
def delete_small(no_symbol):
    moji = str.maketrans("","","ァィゥェォッャュョ")
    delete_small=no_symbol.translate(moji)
    return delete_small
# print(delete_small())

#小文字を大文字に変換する------------------------------------------------------------------------------------------
def small_to_capital(no_symbol):
    moji = str.maketrans("ァィゥェォッャュョ", "アイウエオツヤユヨ")
    small_to_capital=no_symbol.translate(moji)
    return small_to_capital
# print(small_to_capital())

#濁音、半濁音を削除する----------------------------------------------------------------------------------------------
def delete_voiced_semivoiced_sound(no_symbol):
    l=[]
    for c in no_symbol:
        c=jaconv.z2h(c)
        c=jaconv.h2z(c[0])
        l.append(c)
    delete_voiced_semivoiced_sound="".join(l)
    return delete_voiced_semivoiced_sound
# print(delete_voiced_semivoiced_sound())
