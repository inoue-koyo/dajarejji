import numpy as np
import pandas as pd
import pprint

# a=np.array([["猫が寝ころんだ","60","50","10","ネコガネコロンダ","ネコ","2022/11/09"],["猫が寝ころんだ","60","50","10","ネコガネコロンダ","ネコ","2022/11/09"]])

# df=pd.DataFrame(a, columns=["ダジャレ","スコア","ダジャレの質","文法的な正しさ","読み","検出されたダジャレ","登録日"])
# df.to_csv("./csv/ranking.csv", index=False)

df = pd.read_csv('./csv/ranking.csv')
ranking = df.to_numpy().tolist()
# print(ranking[0])
# ranking_t=[list(x) for x in zip(*ranking)]
# print(ranking_t[1])

new=sorted(ranking, key=lambda x: x[2], reverse=True)
for i,j in enumerate(new):
    print(j)
# column_names = ["順位","ダジャレ","スコア","ダジャレの質","文法的な正しさ","読み","検出されたダジャレ","登録日"]
# ranking_df=pd.DataFrame(ranking, columns=column_names)
# ranking_df_sort=ranking_df.sort_values("スコア", ascending=False)
# ranking_df_sort=ranking_df_sort.reset_index(drop=True)
# for i,v in enumerate(ranking_df_sort):
#     print(v)

# print(ranking_df_sort.drop([1,3]))
# ranking_df_sort.to_csv("./csv/ranking.csv",index=False)