import aircv as ac
from PIL import ImageGrab
from PIL import Image


def findQuestion(question):
    prtsc = ImageGrab.grab((300, 130, 800, 830))
    prtsc.save(r".\screen\prtsc1.png")

    imsrc = ac.imread(r".\screen\prtsc1.png")
    imsch = ac.imread(rf".\source\{question}.png")
    result = ac.find_template(imsrc, imsch)
    print("开始查找当前题目。")

    try:
        if result['confidence'] > 0.95:
            return result['rectangle'][0]
    except:
        print("未找到题目！")
        return 1


def findChoices(pot, choice, question, questionAmount):
    choice = choice.upper()
    pot = list(pot)
    pot[0] += 300
    pot[1] += 130
    prtsc = ImageGrab.grab((pot[0] - 50, pot[1], pot[0] + 100, pot[1] + 600 if pot[1] < 410 else 1010))
    prtsc.save(r".\screen\prtsc2.png")

    imsrc = ac.imread(r".\screen\prtsc2.png")
    if question < questionAmount:
        imsch = ac.imread(rf".\source\{question + 1}.png")
        result2 = ac.find_template(imsrc, imsch)
        try:
            if result2['confidence'] > 0.95:
                print("图片中找到了下一题。开始裁剪图片...", end='')
                img = Image.open(r".\screen\prtsc2.png")
                cropped = img.crop((0, 0, img.size[0], result2['result'][1]))
                cropped.save(r".\screen\prtsc4.png")
                print("裁剪图片完成。")
            else:
                Image.open(r".\screen\prtsc2.png").save(r".\screen\prtsc4.png")
                print("图片中没有找到下一题。")
        except:
            Image.open(r".\screen\prtsc2.png").save(r".\screen\prtsc4.png")
            print("图片中没有找到下一题。")
    else:
        Image.open(r".\screen\prtsc2.png").save(r".\screen\prtsc4.png")
        print("最后一题无需检查下一题。")
    imsrc = ac.imread(r".\screen\prtsc4.png")
    imsch = ac.imread(rf".\source\{choice}.png")
    result = ac.find_template(imsrc, imsch)

    print(f"开始查找选项{choice}。")
    try:
        if result['confidence'] > 0.95:
            choicePot = list(result['result'])
            choicePot[0] += (pot[0] - 50)
            choicePot[1] += pot[1]
            return choicePot
    except:
        print(f"未找到选项{choice}！")
        return 1


def findSubmit(submit):
    prtsc = ImageGrab.grab((600, 130, 900, 1030))
    prtsc.save(r".\screen\prtsc3.png")

    imsrc = ac.imread(r".\screen\prtsc3.png")
    imsch = ac.imread(rf".\source\{submit}.png")
    result = ac.find_template(imsrc, imsch)
    
    try:
        if result['confidence'] > 0.95:
            submitPot = list(result['result'])
            submitPot[0] += 600
            submitPot[1] += 130
            return submitPot
    except:
        print(f"未找到提交按钮！")
        return 1
