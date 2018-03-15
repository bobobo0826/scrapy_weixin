#encoding=utf-8
#简单的验证码识别，可能识别效果不理想
import pytesseract
from PIL import Image


def main():
    image = Image.open("D:\scrapy_test\scrapy_weixin\scrapy_weixin\pic.png")
    im = image.convert('L').save("a.png")  # 图片转换为灰色图像
    im = im.convert('RGBA').save("b.png")  # 图片转换成RGBA模式
    # image.show() #打开图片1.jpg
    # text = pytesseract.image_to_string(image)  # 使用简体中文解析图片
    # print(text)
    # with open("output.txt", "w") as f:  # 将识别出来的文字存到本地
    #     print(text)
    #     f.write(str(text))


if __name__ == '__main__':
    main()
