import re

with open("answerhtml.txt", 'r', encoding='utf-8') as fp:
    answerPtn = re.compile("<span>正确答案： ([ABCDE]+) </span>")
    answers = answerPtn.findall(fp.read())

if len(answers) != 10 and len(answers) != 20:
    print("题目数量异常，可能出现错误！")
else:
    with open("answer.txt", 'a', encoding='utf-8') as fp:
        fp.write(" ".join(answers) + "\n")
    print("答案已写入文件！")