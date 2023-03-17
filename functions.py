import jaconv

#文字列の中に何文字のダジャレ（同じ読みの繰り返し）が何個あるかを数える関数--------------------------------------------
def count(i,output,function_name):
    lst=[output[j:j+i] for j in range(0,len(output)-i+1)]
    for k in range(len(lst)):
        num=lst.count(lst[k])
        if num>=2:
            return lst[k],i,num,function_name

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
