import math
import pygame
from pygame.locals import *
import random
import time
import os
from PIL import Image, ImageSequence


# 返回图片文件夹中图片的总数量
def image_count(path):
    file = os.listdir(path)
    return len(file)


# 主角
class Leader:
    speed_x = 10
    speed_y = 10
    x_max = 0           # x轴最大值
    y_max = 0           # y轴最大值
    # 图片帧
    index = 1
    index_max = 0
    scene = None
    music_jump = None

    health = 100                        # 血量值
    health_color = (255, 0, 0)          # 显示血量字体的颜色
    health_msg = "血量:" + str(100)      # 血量信息

    score = 0   # 得分
    score_color = (0, 255, 0)  # 显示分数字体的颜色
    score_msg = "得分:" + str(score)  # 分数信息
    # 角色图片素材路径
    role_image_path = "./resources/images/character/leader/"
    # 创建音乐素材路径
    music_path = "./resources/audios/character/leader/"

    def __init__(self, x, y, scene):
        self.image = []
        # 主角动图总数
        self.index_max = image_count(self.role_image_path)
        # 添加角色图像
        for n in range(1, self.index_max + 1):
            self.image.append(pygame.image.load(self.role_image_path + f"{n}.png"))
        self.scene = scene
        # 添加角色动作音效
        self.music_jump = pygame.mixer.Sound(self.music_path+"jump.mp3")
        # 设置恐龙在窗口的初始位置
        self.rect = self.image[0].get_rect()
        self.rect.left = 0
        self.rect.bottom = y
        # 设置移动边界
        self.x_max = x
        self.y_max = y

    def move(self):
        # 鼠标控制
        # if self.rect.bottom + self.speed_y <= y:
        #     self.rect.y += self.speed_y
        # elif self.rect.top - self.speed_y >= y:
        #     self.rect.y -= self.speed_y
        # if self.rect.right + self.speed_x <= x:
        #     self.rect.x += self.speed_x
        # elif self.rect.left - self.speed_x >= x:
        #     self.rect.x -= self.speed_x
        # 键盘控制
        # 当角色目标Y轴坐标合法时，允许角色上下移动
        if self.speed_y != 0 and self.rect.bottom + self.speed_y in range(self.rect.height, self.y_max):
            self.rect.y += self.speed_y
        # 当角色目标X轴坐标合法时，允许角色左右移动
        if self.speed_x != 0 and self.rect.right + self.speed_x in range(self.rect.width, self.x_max):
            self.rect.x += self.speed_x

    def draw(self):
        # 每次更新血量值和得分
        self.health_msg = "血量:" + str(self.health)
        self.score_msg = "得分:" + str(self.score)
        # 当角色处于地面附近,图片帧数变化
        if self.rect.bottom >= self.y_max - 50:
            self.index += 0.2
            if self.index > self.index_max:
                self.index = 1
        image = self.image[math.floor(self.index) - 1]
        self.scene.blit(image, (self.rect.x, self.rect.y))


# 虫子
class Worm(pygame.sprite.Sprite):
    speed_x = 3
    x_max = 0           # x轴最大值
    index = 1
    index_max = 0
    # 角色图片素材路径
    image_path = "./resources/images/character/enemy/"
    # 创建音乐素材路径
    music_path = "./resources/audios/character/enemy/"

    def __init__(self, x, y):
        super().__init__()
        self.image_group = []
        self.image = None
        # 动图总数
        self.index_max = image_count(self.image_path)
        # 添加图像
        for n in range(1, self.index_max + 1):
            self.image_group.append(pygame.image.load(self.image_path + f"{n}.png"))
        # 设置在窗口的初始位置(窗口的右下角)
        self.rect = self.image_group[0].get_rect()
        self.rect.right = x
        self.rect.bottom = y
        # 设置移动边界
        self.x_max = x

    def update(self):
        self.rect.move_ip(-self.speed_x, 0)
        # 当右边界移动到窗口左边界，删除该对象
        if self.rect.right <= 0:
            self.kill()
        # 更新图片帧
        self.index += 0.2
        if self.index > self.index_max:
            self.index = 1
        self.image = self.image_group[math.floor(self.index) - 1]


# 小鸟
class Bird(pygame.sprite.Sprite):
    # 类中可以被修改的数据类型会随着第一次调用而被修改默认值（列表、字典、集合)
    # 而类中不可以被修改的数据类型的默认值不变（数字、字符串、元组)
    speed = 10
    # 小鸟图片当前帧
    index = 1
    # 小鸟图片数量
    index_max = 0
    # 图片路径
    path = "./resources/images/bird/"

    def __init__(self, x, y, image_kind):
        super().__init__()
        self.image = None
        self.image_group = []
        # 目标小鸟的图片素材路径(第image_kind种小鸟）
        self.path += f"{image_kind}/"
        self.index_max = image_count(self.path)
        # 添加小鸟图像到列表中
        for n in range(1, self.index_max+1):
            self.image_group.append(pygame.image.load(self.path+str(n)+".png"))
        # 设置鸟在背景的初始位置
        self.rect = self.image_group[0].get_rect()
        self.rect.left = x
        self.rect.top = y

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        # 当鸟的右边界移动到屏幕之外，删除该对象
        if self.rect.right <= 0:
            self.kill()
        # 更新图片帧
        self.index += 0.1
        if self.index > self.index_max:
            self.index = 1
        self.image = self.image_group[math.floor(self.index) - 1]


