#!/usr/bin/python
# -*- coding: utf-8 -*-
#↑は途中までなんもなかったのになぜか急にエラー（例：SyntaxError: Non-UTF-8 code starting with '\x82' in file test.py on line 234, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details）出たから追記した。

from janome.tokenizer import Tokenizer
import collections
import pykakasi
import alkana
from alphabet2kana import a2k

from functions import judge

from bert_sentence_accuracy import bert

t = Tokenizer()
kks = pykakasi.kakasi()

def preprocessing(s):
    #品詞分解や単語の重複計算をする----------------------------------------------------------------------------------
    c = collections.Counter(t.tokenize(s, wakati=True))
    mc = c.most_common() #（単語、出現回数）のタプルが並んだリスト

    #mcリストの単語を名詞に絞る--------------------------------------------------------------------------------------
    noun_lst=[]
    for i in range(len(mc)):
        if mc[i][0]==" " or mc[i][0]=="　": #??????空白（記号,空白,*,*）があるとStopIterationエラーが出るから、そん時だけスキップする。全角も半角も??????
            continue
        token=t.tokenize(mc[i][0]).__next__()
        if token.part_of_speech.split(",")[0]=="名詞":
            noun_lst.append(mc[i])
    # print(noun_lst)

    #アラビア数字を漢数字に変換する関数------------------------------------------------------------------------------
    #??????????from kanjize import int2kanjiっていう関数があったけど、「0」だけ入力するとエラーになるのでやめた???????
    def int_to_kanint(num) :
        suji   = ["","一","二","三","四","五","六","七","八","九"]
        kugiri = ["","十","百","千"]
        tani   = ["","万","億","兆","京","垓","𥝱","穣","溝","澗","正","載","極","恒河沙","阿僧祇","那由他","不可思議","無量大数"]

        num  = list(map(int,list(str(num))))
        kansuji = []

        for k, v in zip(range(len(num)), reversed(num)) :
            keta = []
            keta.append(suji[0 if v<2 and k%4 else v])
            keta.append(kugiri[k%4 if v>0 else 0])
            keta.append((tani[0 if k%4 else int(k/4) if any(list(reversed(num))[k:(k+4 if len(num)>=(k+4) else len(num))]) else 0]))
            kansuji.append("".join(keta))
        kansuji = "".join(reversed(kansuji))
        return kansuji if kansuji else "零" #??????「零」を「ゼロ」と読むには???????
    # print(int_to_kanint(num))

    #アラビア数字を漢数字に変換する----------------------------------------------------------------------------------
    int_to_kanint_lst=[int_to_kanint(token.surface) if token.part_of_speech.split(",")[1]=="数" and token.reading=="*" else token.surface for token in t.tokenize(s)] #?????????if文の2つ目の条件は、例えば原文に「十」があった場合アラビア数字と同じように（名詞、数）となるから、int_to_kanint関数の変数numを生成するところでエラーになってしまうのを防ぐため?????????????
    s="".join(int_to_kanint_lst)
    # print(s)

    #英語をカタカナ読みにする----------------------------------------------------------------------------------------
    english_to_kana=[alkana.get_kana(token.surface.lower()) if alkana.get_kana(token.surface.lower()) else token.surface for token in t.tokenize(s)]
    s="".join(english_to_kana)
    # print(s)

    #英語をローマ字読みする（JR,SNSなど）----------------------------------------------------------------------------
    english_to_romaji=[a2k(token.surface) for token in t.tokenize(s)]
    s="".join(english_to_romaji)
    # print(s)

    #カナ文字に変換-------------------------------------------------------------------------------------------------
    tokenize_lst=list(t.tokenize(s))
    yomi_lst=[]
    #???????kakasiやと「経つ」を「ヘツ」と読んだりするから基本使わん。代わりにtokenizeの読みを取得する。逆に「剃って」はkakasiやと「ソッテ」と読んでくれるがtokenizeやと「スッテ」になる。どっちもどっち?????????
    for i,_ in enumerate(tokenize_lst):
        if tokenize_lst[i].reading=="ヲ": #??????????「ヲ」は「オ」と読む???????????
            yomi="オ"
        elif tokenize_lst[i].phonetic=="*": #????????「コーチ」や「ティーチャー」など、読みが「*」になるときがあるからそん時だけkakasi使う??????????
            result=kks.convert(tokenize_lst[i].surface) 
            yomi=result[0]["kana"]
            # print(yomi)
        else:
            yomi=tokenize_lst[i].phonetic #??????「十」の発音を取得すると「ジュー」になってしまうけど、読みを取得したら「ジュウ」になる???????
        yomi_lst.append(yomi) #??????????????????「菅」を「スガ」と読むには??????????????????????
    kana="".join(yomi_lst) #????????????????「100匹」を「ヒャッピキ」と読むには。「10個」を「ジュッコ」。「100円寿司」は「ヒャクエンスシ」と読まれちゃう?????????????????
    if "ヅ" in kana:
        kana=kana.replace("ヅ","ズ")

    # print(kana)

    #記号を削除-----------------------------------------------------------------------------------------------------
    no_symbol = ''.join(filter(str.isalnum,kana)) 
    # print(no_symbol)

    return no_symbol,noun_lst

#確認用-------------------------------------------------------------------------------------------------------------
def score(s):
    # s="時たま悟空溶き卵食う"
    # preprocessing(s)
    no_symbol=preprocessing(s)[0]
    noun_lst=preprocessing(s)[1]
    for j in range(len(noun_lst)):
        if noun_lst[j][1]>=2: #同じ名詞を使っていないか確認
            if t.tokenize(noun_lst[j][0]).__next__().phonetic=="*":
                result=kks.convert(t.tokenize(noun_lst[j][0]).__next__().surface) 
                yomi=result[0]["kana"]
            else:
                yomi = t.tokenize(noun_lst[j][0]).__next__().phonetic

            if no_symbol.count(yomi)<=noun_lst[j][1]:
                a=1
                return f"【{s}】は同じ名詞を複数回用いているのでダジャレではない可能性があります",a,no_symbol
    if judge(no_symbol,s)[1]==1: #ダジャレじゃないパターン
        return judge(no_symbol,s)
    else: #ダジャレと判定されたパターン
        quality_score=0 #ダジャレの質を示すスコア
        quality_score+=judge(no_symbol,s)[1]*4 #40点、grammar_scoreを含める場合は30点
        quality_score+=judge(no_symbol,s)[2]*8 #24点、grammar_scoreを含める場合は20点
        if judge(no_symbol,s)[3]=="nothing": #36点、grammar_scoreを含める場合は30点
            quality_score+=36
        elif judge(no_symbol,s)[3]=="macron_to_vowel" or judge(no_symbol,s)[3]=="macron_to_vowel_iu":
            quality_score+=30
        elif judge(no_symbol,s)[3]=="delete_macron":
            quality_score+=29
        elif judge(no_symbol,s)[3]=="delete_smalltu":
            quality_score+=28
        elif judge(no_symbol,s)[3]=="delete_small":
            quality_score+=27
        elif judge(no_symbol,s)[3]=="small_to_capital":
            quality_score+=26
        elif judge(no_symbol,s)[3]=="delete_voiced_semivoiced_sound":
            quality_score+=25
        
        # grammar_score=round(-50/bert(s),1) #20点、ダジャレの文法的な正しさを示すスコア、Bertが-2.5のときに20点満点
        grammar_score=0

        return s, no_symbol, quality_score, grammar_score, judge(no_symbol,s)[0], judge(no_symbol,s)[1], judge(no_symbol,s)[2]

        #入力、前処理後、スコア（ダジャレの質）、スコア（文法的な正しさ）、トータルスコア、検出されたダジャレ、ダジャレの文字数、ダジャレの反復回数
# print(score("佐賀市に有るか無いか？捜しに歩かないか？"))
