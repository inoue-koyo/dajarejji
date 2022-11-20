from transformers import BertJapaneseTokenizer, BertForMaskedLM, pipeline, BertConfig
import torch #Bertを使うのに必要
import re
import numpy as np

# import GPUtil

@torch.no_grad()
def bert(input):
    # input='「イワシ・タイ・ナマズ」って言わしたいな、まず。'
    # input2='給料は玉ねぎのことです。'
    
    # GPUtil.showUtilization()
    
    torch.cuda.empty_cache()

    pretrained = 'cl-tohoku/bert-base-japanese-whole-word-masking'#事前学習済みモデルの選択
    tokenizer = BertJapaneseTokenizer.from_pretrained(pretrained) #分析器の事前学習モデルの選択
    model = BertForMaskedLM.from_pretrained(pretrained) #事前学習モデルのロード
    config=BertConfig.from_pretrained(pretrained) # 事前学習済みモデルの設定
    MLM=pipeline('fill-mask',model=model,tokenizer=tokenizer,config=config) # pepeline関数でモデルを利用できるようにする

    # GPUtil.showUtilization()

    score=0
    tokenized_text1=tokenizer.tokenize(input) # 文章を形態素解析
    for i in range(len(tokenized_text1)):
        provisional=tokenized_text1[i] # マスクする部分を一時的に保持する変数
        tokenized_text1[i]='[MASK]' # 一単語をマスクする
        text=''.join(tokenized_text1) # リストになっているので、連結して一つの文にする
        score=re.findall(r'\d+\.\d+',str(MLM(text)[0])) # 解析結果の中から小数を抜き出す
        score=+np.log(float(score[0])/len(tokenized_text1)) #生起確率を足し合わせる
        tokenized_text1[i]=provisional # マスクした単語を元に戻す

    # 文章と文法的な正しさの度合を表示
    return score 
# print(bert())

    # score2=0
    # tokenized_text2=tokenizer.tokenize(input2)
    # for i in range(len(tokenized_text2)):
    #     provisional=tokenized_text2[i]
    #     tokenized_text2[i]='[MASK]'
    #     text=''.join(tokenized_text2)
    #     score=re.findall(r'\d+\.\d+',str(MLM(text)[0]))
    #     score2=+np.log(float(score[0])/len(tokenized_text2))
    #     tokenized_text2[i]=provisional

    # print(input2)
    # print(str(score2))