import Ted_Crawler
import Player
import time
import signal
from time import sleep

# welcome info
print("")
print("=====歡迎來到 Ted__?__，填入你的英語未來！=====")

# 取得演講類別
print("=====請選擇演講類別=====")
topics = Ted_Crawler.Topics.getTopics()
for i in range(len(topics)):
    print(i, topics[i].name)

# 用戶輸入演講類別
topic_selected = input("種類編號(0~6): ")

# 取得演講清單
crawler = Ted_Crawler.TedCrawler()
lists = crawler.playlists_request(topics[int(topic_selected)].value)
talk_names = list(lists.keys())

# 選擇演講，若選中的演講沒有音檔來源，則請用戶重新輸入
def select_talk():
    print("=====請選擇任一演講=====")
    for i in range(len(lists)):
        print(i, talk_names[i])

    talk_selected = input("演講編號(0~35): ")

    print("=====取得資料中=====")
    talk_name = talk_names[int(talk_selected)]
    info = crawler.vedio_page_request(lists[talk_name])
    download_successful = info[0]
    if not download_successful:
        print("您選的演講並沒有資訊源，請選擇其他演講")
        select_talk()
    else:
        return info

# data from crawler
info = select_talk()
talk_id = info[1]
correct_answers = info[3]
text = info[2]

# index for paragraph
index = 0
# collected answers
all_answers = []

print("=====資料取得完畢=====")
print("=====開啟播放器=====")
player = Player.Talk_player()
player.play_talk(talk_id)

def interrupted(signum, frame):
    # called when read times out
    raise ValueError('oops!')
signal.signal(signal.SIGALRM, interrupted)

def input_with_timeout(timeout):
    # set alarm
    signal.alarm(timeout)
    answers = input_fun()

    # disable the alarm after success
    signal.alarm(0)
    print('\nYou typed', answers)
    return answers


def input_fun():
    first = ""
    second = ""
    third = ""
    try:
        first = input("first:" )
        second = input("second:" )
        third = input("third:" )

        # user entered all blanks but we have to stay here until getting signal
        while True:
            time.sleep(10)
        # will nerver excute
        return [first, second, third]
    except:
        # get signal to go to next paragraph, return user's answes of this paragraph
        return [first, second, third]

# wait for Ted official statement before speaker starts
time.sleep(18)

# iterate each paragraph
for i in range(len(text)):

    if index <= (len(text) - 2):

        # print transcript
        print(text[index]["text"])

        # calculate duration of this paragraph
        skip_timeout = (text[(index+1)]["time"] - text[index]["time"]) / 1000

        # set signal alert time
        answers = input_with_timeout(int(skip_timeout))

        # add answers in this paragraph into all_answers list
        all_answers = all_answers + answers
        index += 1

# wait for audio end playing
time.sleep(5)
print("=====成績計算中=====")
time.sleep(5)

# varify the answers
total_questions = 0
correct_num = 0

print("Your answers / Correct answers")
print("------------------------------")
for i in range(len(correct_answers)):

    correct_ans = correct_answers[i]
    if correct_ans == "not_valid":
        continue
    else:
        print(all_answers[i]," / ", correct_ans)
        total_questions += 1
        if all_answers[i] == correct_ans:
            correct_num += 1

correct_rate = (correct_num/total_questions)*100
print("Correct Rate:", str(correct_rate), "%")

# delete audio files
player.remove_audios(talk_id)