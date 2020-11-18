import re
import sys
from ctypes import *
from time import sleep
from pykeyboard import PyKeyboard
from pymouse import PyMouse
import FindPic

k = PyKeyboard()
m = PyMouse()
isFirst = bool(int(sys.argv[1]))


def getColor(x, y):
    gdi32 = windll.gdi32
    user32 = windll.user32
    hdc = user32.GetDC(None)
    pixel = gdi32.GetPixel(hdc, x, y)
    return pixel


def answerExam(x):
    # 从文件中读取答案
    with open("answer.txt", "r", encoding="utf-8") as fp:
        answers = fp.read().split("\n")[x - 1].split()
    questionAmount = len(answers)
    # 开始填写每道题
    for i, answer in enumerate(answers):
        print(i + 1, answer)
        counter = 0
        while True:
            m.click(160, 560)
            k.tap_key(k.down_key, 1)
            sleep(0.5)
            questionPot = FindPic.findQuestion(i + 1)
            print("questionPot", questionPot)
            if questionPot is None or questionPot == 1:
                counter += 1
                if counter >= 5:
                    return 1
                continue

            # 开始填写一道题的每个答案
            for choice in answer:
                counter2 = 0
                while True:
                    sleep(0.25)
                    try:
                        choicePot = FindPic.findChoices(questionPot, choice, i + 1, questionAmount)
                    except TypeError:
                        return 2
                    
                    if choicePot is None or choicePot == 1:
                        counter2 += 1
                        if counter2 >= 5:
                            return 2
                        sleep(0.5)
                        m.click(160, 560)
                        k.tap_key(k.down_key, 1)
                        questionPot = FindPic.findQuestion(i + 1)
                        print("questionPot", questionPot)
                        continue
                    print("choicePot", choicePot)
                    m.click(int(((choicePot[0]) - 23) / 1.25), int(choicePot[1] / 1.25))
                    break
            break

    # 全部答案填写完后提交/保存答案
    print("开始提交...", end='')
    while True:
        sleep(0.5)
        submitPot = FindPic.findSubmit("notsubmit")
        print("submitPot", submitPot)
        if submitPot is None or submitPot == 1:
            m.click(160, 560)
            k.tap_key(k.down_key, 1)
            continue
        m.click(int(submitPot[0] / 1.25), int(submitPot[1] / 1.25))
        sleep(1)
        k.tap_key(k.enter_key)
        break


chapterURLPtn = re.compile("""<a href='/mycourse/studentstudy(.*)'""")
with open("html.txt", "r", encoding="utf-8") as fp:
    urls = list(
        map(lambda x: "http://mooc1.mooc.whu.edu.cn/mycourse/studentstudy" + x, chapterURLPtn.findall(fp.read())))

k.press_key(k.windows_l_key)
k.tap_key('r')
k.release_key(k.windows_l_key)
sleep(0.2)

k.type_string("C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
sleep(0.5)
k.tap_key(k.enter_key)
sleep(1)

k.press_key(k.control_l_key)
k.tap_key(k.space_key)
k.release_key(k.control_l_key)

print("开始...")

examOrder = 0
for i, url in enumerate(urls):
    sleep(0.5)
    k.tap_key(k.function_keys[4])
    sleep(0.2)
    k.type_string(url)
    sleep(0.2)
    k.tap_key(k.enter_key)
    sleep(5)
    if isFirst:
        if True:
            if getColor(350, 530) != 0x000000:
                examOrder += 1
                print(f"第{examOrder}章测试题已经完成，跳过！")
            elif getColor(350, 530) != 0xFFFFFF:
                m.click(608, 656)
                sleep(2)
                print(f"第{i + 1}个视频已经完成，跳过！")
            continue

    if getColor(350, 530) == 0x000000:
        m.click(608, 656)
        while getColor(350, 460) != 0x349B7B:
            print(f"视频放映中...{i + 1}/{len(urls)}")
            sleep(2)
    else:
        examOrder += 1
        print(f"正在做第{examOrder}章测试题...")
        sleep(10)
        isMistake = answerExam(examOrder)
        if isMistake == 1:
            print("将视频误判为测试题，已经为您跳过当前页面！")
            examOrder -= 1
            continue
        elif isMistake == 2:
            print("将已完成的测试题误判为未完成，已经为您跳过当前页面！")
            continue
        print(f"第{examOrder}章测试题已经提交！")
