import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

numbers = ''.join(map(str, range(10)))
chars = ''.join((numbers))
import platform


def create_validate_code(size=(80, 30),
                         chars=chars,
                         mode="RGB",
                         bg_color=(255, 250, 250),
                         font_size=18,
                         font_type="",
                         length=4,
                         draw_points=True,
                         point_chance=2):
    def getRandomColor():
        return (
            random.randint(
                0, 250), random.randint(
                0, 250), random.randint(
                0, 250))

    fg_color = getRandomColor()  # 获取一个随机颜色
    width, height = size
    img = Image.new(mode, size, bg_color)  # 创建图形
    draw = ImageDraw.Draw(img)  # 创建画笔
    PLATFORM = platform.system().lower()  # 设置linux 下字体路径
    # if PLATFORM == 'linux':
    #     font_type = "/usr/share/fonts/simsun.ttc"
    path_of_this_file = os.path.abspath(os.path.dirname(__file__))
    font_type = os.path.abspath(
        os.path.join(
            path_of_this_file,
            '..',
            '..',
            '..',
            '..',
            'data/simsun.ttc'))

    def get_chars():
        '''''生成给定长度的字符串，返回列表格式'''
        return random.sample(chars, length)

    def create_points():
        '''''绘制干扰点'''
        chance = min(50, max(0, int(point_chance)))  # 大小限制在[0, 50]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 50)
                if tmp > 50 - chance:
                    draw.point((w, h), fill=getRandomColor())

    def create_strs():
        '''''绘制验证码字符'''
        c_chars = get_chars()
        strs = '%s' % ''.join(c_chars)

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 4),
                  strs, font=font, fill=fg_color)

        return strs

    def create_lines():
        '''绘制干扰线'''
        line_num = random.randint(*(1, 3))  # 干扰线条数

        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    if draw_points:
        create_points()
        create_lines()
    strs = create_strs()

    params = [1 - float(random.randint(1, 2)) / 100,
              0.005,
              0.002,
              0.003,
              1 - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

    return img, strs


if __name__ == '__main__':
    print(create_validate_code())
