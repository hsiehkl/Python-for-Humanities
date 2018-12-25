import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import json

class Text_converter:
    
    # 初始化逐字稿處理物件
    def __init__(self, text_json):
        self.text_json = text_json

    def parse_text(self):
        text_1 = self.text_json["paragraphs"]

        newlist_1 = [] 

        par = ""
        flag = True
        time = ""

        for i in range(len(text_1)):
            ques_data = text_1[i]["cues"]
            for index in range(len(ques_data)):
                text = ques_data[index]["text"]
                if flag == True:
                    time = ques_data[index]["time"]
                    flag = False
                par += text + ' '
            
            par = par.replace('\n',' ')
            
            par_list = re.split(r'([.,:?!()\s])',par)
            par_list = [x for x in par_list if x != ' ']
            par_list = [x for x in par_list if x != '']
            # print(len(par_list))
            
            if len(par_list) > 130:

                dic = {}
                dic["time"] = time
                dic["text_list"] = par_list
                newlist_1.append(dic)
                par=''
                flag = True
            else:
                
                if i == (len(text_1) -1):
                    dic1 = {}
                    dic1["time"] = time
                    dic1["text_list"] = par_list

                    newlist_1.append(dic1)
                else:
                    continue
            
        #print(newlist_1)
        # print(newlist_1) 一個list裡包含n個dic 文字內容為list

        w = {}
        word_s1 = []
        words_2 = {}
        stop_words = ["Cheering", 'Laughter', 'Applause', "Higher"]
        for w in range(len(newlist_1)):
            words_1 = newlist_1[w]['text_list']#文字內容
            #print(words_1)

            for z in words_1:
                if len(z) > 5 and z not in stop_words :
                    word_s1.append(z)
            words_2[w]= word_s1
            word_s1 = []
        # print(words_2) 準備選來挖空的字們

        for w in range(len(newlist_1)):
            if words_2[w]==[]:
                del words_2[w]
            else:
                pass

        end_list = []
        time_1 = ""
        ques_words = []
        import numpy as np
        for k in range(len(words_2)): 
            choice_word = words_2[k]
            num_words = []
            for w in range(1,len(choice_word)+1):
                num_words.append(w) 
                num_med = round(np.percentile(num_words,40))
                num_per1 =round(np.percentile(num_words,15))
                num_per2 =round(np.percentile(num_words,65))
            num_med = int(num_med)
            num_per1 = int(num_per1)
            num_per2 = int(num_per2)
            ques_word_1 = choice_word[num_per1]

            try:
                ques_word_2 = choice_word[num_med]
            except:
                ques_word_2 = "not_valid"

            try:
                ques_word_3 = choice_word[num_per2]
            except:
                ques_word_3 = "not_valid"

            words_3 = newlist_1[k]['text_list']
            words_3 = ' '.join(words_3)
            ques_words.append(ques_word_1)
            ques_words.append(ques_word_2)
            ques_words.append(ques_word_3) 
            words_3 = words_3.replace(ques_word_1,'_____',1)
            words_3 = words_3.replace(ques_word_2,'_____',1)
            words_3 = words_3.replace(ques_word_3,'_____',1)
            dic_end = {}
            time_1 = newlist_1[k]['time']
            dic_end['time']=time_1
            dic_end['text']=words_3
            end_list.append(dic_end)

        last_time = text_1[-1]["cues"][0]["time"]
        dic_last = {}
        dic_last['time']=last_time
        dic_last['text']=""
        end_list.append(dic_last)

        return (end_list, ques_words)
        #print(end_list) #時間與挖空完的段落
        #print(ques_words) #所有挖空的單字





        




         



        
