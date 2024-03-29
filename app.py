from flask import Flask, render_template, request
import pandas as pd
import datetime
import os

from judge import score


app = Flask(__name__)
# app = Flask(__name__, static_folder='./static') #cssやimagesはstaticに入ってればいい。そのstaticを指定するのがstatic_folder。デフォルトではstaticはstaticディレクトリになる。

column_names = ["順位","ダジャレ","スコア","ダジャレの質","文法的な正しさ","読み","検出されたダジャレ","登録日"]
df = pd.read_csv('./csv/ranking.csv')
ranking = df.to_numpy().tolist()

def savecsv(array):
    ranking_df=pd.DataFrame(array, columns=column_names)
    ranking_df.to_csv("./csv/ranking.csv", index=False)

@app.route('/')
def layout():
        return render_template("home.html")

@app.route("/ranking")
def ranking_function(): 
    rank_in_dajare=request.args.get("rank_in_dajare") #layout.htmlから変数を受け取っている
    df = pd.read_csv('./csv/ranking.csv')
    ranking = df.to_numpy().tolist()
    return render_template("ranking.html", ranking=ranking, rank_in_dajare=rank_in_dajare)

@app.route('/judge', methods=["POST"])
def dajare():
    input_text=request.form["input_text"]
    result=score(input_text)
    if result[1]==1: #ダジャレと判定されなかった場合
        return render_template("result_false.html",message=result[0],input_text=input_text,preprocessing=result[2])
    else: #ダジャレと判定された場合
        total_score=result[2]+result[3]
        df = pd.read_csv('./csv/ranking.csv')
        ranking = df.to_numpy().tolist()
        if ranking==[]: #初登録の時だけランキングリストが空やから場合分けしてる
            rank=[1,input_text, total_score, result[2], result[3], result[1], result[4], datetime.datetime.now().date()]
            ranking.append(rank)
            savecsv(ranking)
        else:
            ranking_t=[list(x) for x in zip(*ranking)] #ランキングリストの行と列を入れ替えた転置リスト
            if input_text in ranking_t[1]: #ランキングに同じダジャレがあれば、登録日だけ更新する
                i=ranking_t[1].index(input_text)
                ranking[i][7]=datetime.datetime.now().date()
                savecsv(ranking)
            else:
                rank=[1,input_text, total_score, result[2], result[3], result[1], result[4], datetime.datetime.now().date()]
                ranking.append(rank)
                ranking=sorted(ranking, key=lambda x: x[2], reverse=True)
                for i,j in enumerate(ranking): #順位を割り振っていく
                    if i==0:
                        j[0]=1
                    elif j[2]==ranking[i-1][2]: #一個上のダジャレと同じスコアやったら同率にする
                        j[0]=ranking[i-1][0]
                    else:
                        j[0]=i+1
                    if j[0]>10: #順位が11位以下になったら削除する
                        ranking.pop(i)
                savecsv(ranking)

        ranking_t=[list(x) for x in zip(*ranking)]
        if input_text in ranking_t[1]: #ランクインした場合
            text="rank_in"
        else:
            text=""

        directory="static/images" #点数によって画像が変わる
        if total_score>=90:
            image_path=os.path.join(directory, "amazing.jpg")
        elif total_score>=80:
            image_path=os.path.join(directory, "excellent.jpg")
        elif total_score>=70:
            image_path=os.path.join(directory, "wonderfull.jpg")
        elif total_score>=60:
            image_path=os.path.join(directory, "wow.jpg")
        elif total_score>=50:
            image_path=os.path.join(directory, "very_good.jpg")
        else:
            image_path=os.path.join(directory, "good.jpg")

        return render_template("result_true.html", input_text=input_text, preprocessing=result[1], quality_score=result[2], grammar_score=result[3], total_score=total_score, dajare=result[4], letter_number=result[5], repeat_count=result[6], image_path=image_path, text=text)

@app.route('/detail')
def detail():
    return render_template("detail.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True) #hostとportをこのように設定することで、同じWi-Fiに繋いだ機器からもサイトが開けるURLが生成される。
