import pygame
from pygame.locals import *
import random
import time
import os
import math
from PIL import Image, ImageDraw, ImageFont
import numpy


def image_count(path):
    file = os.listdir(path)
    return len(file)


# 仙人掌
class Cactus(pygame.sprite.Sprite):
    speed = 8
    image = None
    scene = None

    def __init__(self, x, y, image, scene):
        super().__init__()
        self.scene = scene
        self.image = image
        self.rect = image.get_rict()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        # 当障碍物的右边界移动到屏幕之外，删除该对象
        if self.rect.right <= 0:
            # 对象删除自身不会影响到存放它的group组集合
            self.kill()


# 金币
class Gold(pygame.sprite.Sprite):
    speed = 5

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        # 设置金币在背景的初始位置
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.bottom = y

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        # 当金币的右边界移动到屏幕之外，删除该对象
        if self.rect.right <= 0:
            self.kill()


class Font:
    msg = "hello world"
    # 字体图片
    image = Image.new('RGB', (1000, 400), color=(0, 0, 0))
    d = ImageDraw.Draw(image)
    # 右边界
    right_range = 0

    def __init__(self, x, y, scene):
        self.x = x
        self.y = y
        # 窗口字体
        self.fnt = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', 200)
        self.d.text((0, 0), self.msg, font=self.fnt, fill=(255, 255, 255))
        # 金币图片
        self.gold_surface = pygame.image.load("./resources/images/Gold/24.png")
        # 金币集合
        self.gold_group = pygame.sprite.Group()
        self.scene = scene
        # 转化成金币图像
        self.paste()

    # 用金币图像覆盖字体画
    def paste(self):
        # 转化为灰度图像
        self.image = self.image.convert(mode='L')
        block_size = 24
        # 字符画初始坐标范围
        y_range = random.randint(0, self.y - self.image.size[1])
        x_range = random.randint(self.x, self.x + self.image.size[0])
        # 右边界
        self.right_range = x_range + self.image.size[0]
        for y in range(0, self.image.height, block_size):
            for x in range(0, self.image.width, block_size):
                # 选取block_size*block_size大小的图片，转化为矩阵
                area = numpy.array(self.image.crop([x, y, x + block_size, y + block_size]))
                # 计算灰度平均值
                val = numpy.mean(area)
                # 根据val值大小，选择是否添加金币对象
                if val > 100:
                    self.gold_group.add(Gold(x_range + x, y_range + y, self.gold_surface))

    def draw(self):
        self.gold_group.draw(self.scene)

    def update(self):
        # 整体右边界更新坐标
        self.right_range -= Gold.speed
        self.gold_group.update()


# 血瓶（恢复生命）
class Potion(pygame.sprite.Sprite):
    speed = 5
    path = "./resources/images/potion/"

    def __init__(self, x, y):
        super().__init__()
        # 添加血瓶图像(静态）
        self.image = pygame.image.load(self.path + f"{1}.png")
        # 设置血瓶在背景的初始位置
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(x, x + x)
        self.rect.bottom = random.randint(self.rect.height, y)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        # 当血瓶的右边界移动到屏幕之外，删除该对象
        if self.rect.right <= 0:
            self.kill()



