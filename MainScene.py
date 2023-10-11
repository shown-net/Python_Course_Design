import pygame
import sys
from pygame.locals import *
import random
import time
import os
from PIL import Image, ImageSequence
import threading
import csv
from object import *
from role import *
from button import *

# 创建图片素材路径变量
image_path = "./resources/images/"
# 游戏运行标志
flag = True


def image_count(path):
    file = os.listdir(path)
    return len(file)


# gif转换成多个图片
def gif_image(path):
    pillow_image = Image.open(path)
    path = path.rstrip(".gif")
    index = 1
    # 缩小倍数
    x = 1
    for frame in ImageSequence.all_frames(pillow_image):
        width = frame.size[0]
        height = frame.size[1]
        frame = frame.resize((int(width/x), int(height/x)), Image.LANCZOS)
        frame.save(path+f"{index}.png")
        index += 1


# 地图
class GameBackGround(pygame.sprite.Sprite):
    # 地图滚动速度
    speed = 8

    # 初始化地图
    def __init__(self, x, y, kind):
        super().__init__()
        self.path = image_path+f"backGround/{kind}.jpg"
        # 加载图片资源
        self.image = pygame.image.load(self.path)
        # 设置背景的初始位置
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    # 计算地图图片以及绘制坐标
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        # 当背景图片的右边界移动到屏幕之外，删除该对象
        if self.rect.right <= 0:
            self.kill()


# 主场景
class MainScene:
    size = None
    scene = None

    button = None
    # 窗口字体
    font = None
    # 字体
    font_gold = None
    # 金币音效播放对象
    gold_channel = None
    # 背景
    background_group = pygame.sprite.Group()
    # 血瓶
    potion = None
    # 血瓶的集合
    potion_group = pygame.sprite.Group()
    # 血瓶音效播放对象
    potion_channel = None
    # 鸟
    # 鸟的集合
    bird_group = pygame.sprite.Group()
    # 主角
    leader = None
    leader_speed_x = 0
    health_image = None
    score_image = None
    # 虫子
    worm = None
    # 敌人的集合
    enemy_group = pygame.sprite.Group()
    # 碰撞列表(除主角之外的物体对象)
    bomb_list = []
    # 死亡对象动画字典（key为图像，value=（坐标x,坐标y,开始死亡时间t)
    dict = {}
    # 死亡动画执行时间
    death_second = 0.6
    # 鼠标光标位置
    mouse_pos = []
    # 游戏暂停画面
    gamepause_image = pygame.image.load(image_path+"gamepause.png")
    gamepause_image_x = 0
    gamepause_image_y = 0
    button_game_continue = None
    # 游戏结束画面
    gameover_image = pygame.image.load(image_path+"gameover.png")
    gameover_image_x = 0
    gameover_image_y = 0

    # 初始化主场景
    def __init__(self):
        # 初始化pygame,使用自定义字体必须用到
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        # 窗口字体
        self.font = pygame.font.SysFont("KaiTi", 30)
        # 场景尺寸
        self.size = (800, 600)
        # 场景对象
        self.scene = pygame.display.set_mode([self.size[0], self.size[1]], pygame.RESIZABLE)
        # 设置游戏标题
        pygame.display.set_caption("恐龙快跑")
        # 设置游戏暂停画面位置和按钮
        self.gamepause_image_x = (self.size[0] - self.gamepause_image.get_width())/2
        self.gamepause_image_y = (self.size[1] - self.gamepause_image.get_height())/2
        self.button_game_continue = Button(self.scene, self.gamepause_image_x, self.gamepause_image_y + 100, "continue.png")
        # 设置游戏结束画面位置
        self.gameover_image_x = (self.size[0] - self.gameover_image.get_width()) / 2
        self.gameover_image_y = (self.size[1] - self.gameover_image.get_height()) / 2
        # 创建clock对象控制帧数
        self.timer = pygame.time.Clock()
        # 创建地图对象
        self.background_group.add(GameBackGround(0, 0, 1))
        self.background_group.add(GameBackGround(self.size[0], 0, 2))
        # 创建字体画
        self.font_gold = Font(self.size[0], self.size[1], self.scene)
        # 创建金币播放音效
        self.gold_channel = pygame.mixer.Sound("./resources/audios/object/gold.mp3")
        # 创建血瓶
        self.potion = Potion(self.size[0], self.size[1])
        self.potion_channel = pygame.mixer.Sound("./resources/audios/object/potion.mp3")
        self.potion_group.add(self.potion)
        # 创建仙人掌
        # for n in range(7):
        # self.item_images.append(pygame.image.load.())
        # 创建鸟(2个）
        self.bird_group.add(Bird(self.size[0], 100, 1))
        self.bird_group.add(Bird(self.size[0] + 100, 100, 2))
        # 创建主角
        self.leader = Leader(self.size[0], self.size[1], self.scene)
        self.leader_speed_x = self.leader.speed_x
        # 创建虫子(1个）
        self.worm = Worm(self.size[0], self.size[1])
        self.enemy_group.add(self.worm)

    # 绘制
    def draw_elements(self):
        self.scene.fill([255, 255, 255])
        # 绘制背景
        self.background_group.draw(self.scene)
        # 绘制主角
        self.leader.draw()
        # 显示血量
        self.health_image = self.font.render(self.leader.health_msg, True, self.leader.health_color)
        self.scene.blit(self.health_image, (0, 0))
        # 显示得分
        self.score_image = self.font.render(self.leader.score_msg, True, self.leader.score_color)
        self.scene.blit(self.score_image, (self.size[1] - 100, 0))
        # 绘制敌人
        self.enemy_group.draw(self.scene)
        # 绘制敌人死亡动画
        for key, value in self.dict.items():
            self.scene.blit(key, (value[0], value[1]))
        # 绘制鸟
        self.bird_group.draw(self.scene)
        # 绘制字体画
        self.font_gold.draw()
        # 绘制血瓶
        self.potion_group.draw(self.scene)

    # 计算元素坐标及生成元素
    def action_elements(self):
        # 先添加元素到精灵组中，再对每个精灵update
        # 地图
        if len(self.background_group) <= 2:
            self.background_group.add(GameBackGround(self.size[0], 0, random.randint(1, 2)))
        self.background_group.update()
        # 仙人掌

        # 字体画
        if self.font_gold.right_range <= 0:
            self.font_gold = Font(self.size[0], self.size[1], self.scene)
        self.font_gold.update()

        # 血瓶
        if len(self.potion_group) == 0:
            self.potion_group.add(Potion(self.size[0], self.size[1]))
        self.potion_group.update()

        # 鸟
        if len(self.bird_group) == 0:
            self.bird_group.add(Bird(self.size[0], 100, 1))
            self.bird_group.add(Bird(self.size[0] + 100, 100, 2))
        self.bird_group.update()

        # 主角移动
        self.leader.move()
        # 敌人移动
        if len(self.enemy_group) == 0:
            self.worm = Worm(self.size[0], self.size[1])
            self.enemy_group.add(self.worm)
        self.enemy_group.update()

        # 敌人死亡动画透明度的计算
        for key, value in list(self.dict.items()):
            val = (time.time() - value[2]) / self.death_second
            # set_alpha()函数会直接影响到窗口背景
            # 删除图片后，子窗口必须还原到100%不透明度:(255)为100%不透明度
            # 目前有一个问题：当图片未消失完全时，同类型物体经过仍然会被透明化
            # 透明化程度大于100%，直接删除该键值对
            if val > 1:
                key.set_alpha(255)
                del self.dict[key]
            else:
                key.set_alpha(int(255*(1-val)))

    # 处理事件
    def handle_event(self):
        global flag
        for event in pygame.event.get():
            # 检测用户按下窗口关闭按钮事件
            if event.type == pygame.QUIT:
                self.gameover_quit()
                pygame.quit()
        # 角色血量归0
        if self.leader.health <= 0:
            # self.gameover_quit()
            flag = False

    # 碰撞检测
    def detect_collision(self):
        # 主角和鸟
        self.bomb_list = pygame.sprite.spritecollide(self.leader, self.bird_group, True)
        for sprite in self.bomb_list:
            self.dict.update({sprite.image: [sprite.rect.x, sprite.rect.y, time.time()]})
            self.leader.health -= 1
        # 主角和敌人
        self.bomb_list = pygame.sprite.spritecollide(self.leader, self.enemy_group, True)
        for sprite in self.bomb_list:
            self.dict.update({sprite.image: [sprite.rect.x, sprite.rect.y, time.time()]})
            self.leader.health -= 1
        # 主角和金币
        self.bomb_list = pygame.sprite.spritecollide(self.leader, self.font_gold.gold_group, True)
        for sprite in self.bomb_list:
            # 播放获得金币音效，得分增加
            self.gold_channel.play()
            self.leader.score += 1
        # 主角和血瓶
        self.bomb_list = pygame.sprite.spritecollide(self.leader, self.potion_group, True)
        for sprite in self.bomb_list:
            # 播放获得血瓶音效，生命增加
            self.potion_channel.play()
            self.leader.health += 1
            self.dict.update({sprite.image: [sprite.rect.x, sprite.rect.y, time.time()]})

    # 按键处理
    def key_press(self):
        # 获取按下按键信息
        key_pressed = pygame.key.get_pressed()
        # 当按下方向右键时，角色向右移动
        if key_pressed[K_RIGHT]:
            self.leader.speed_x = self.leader_speed_x
        # 当按下方向左键时，角色向左移动
        if key_pressed[K_LEFT]:
            self.leader.speed_x = -self.leader_speed_x
        # 角色不左右移动
        elif key_pressed[K_RIGHT] is False and key_pressed[K_LEFT] is False:
            self.leader.speed_x = 0
        # 当按下空格键时，角色向上飞
        if key_pressed[K_SPACE] is True:
            self.leader.speed_y = - abs(self.leader.speed_y)
        # 没有按下空格键时，角色向下落
        else:
            self.leader.speed_y = abs(self.leader.speed_y)
        # 当按下esc键时，游戏暂停
        if key_pressed[K_ESCAPE]:
            global flag
            flag = False
        # 当按下ESCAPE键时，游戏结束
        # if key_pressed[K_ESCAPE]:
        #     self.gameover_quit()

    # 处理帧数
    def set_fps(self):
        # 刷新显示
        pygame.display.update()
        # 设置帧率
        self.timer.tick(60)

    # 主循环，主要处理各种事件
    def run_scene(self):
        global flag
        while True:
            while flag:
                # 计算元素坐标及生成元素
                self.action_elements()
                # 绘制元素图片
                self.draw_elements()
                # 处理事件
                self.handle_event()
                # 碰撞检测
                self.detect_collision()
                # 按键处理
                self.key_press()
                # 更新画布设置，fps
                self.set_fps()
            # 游戏暂停,绘制暂停界面
            self.gameover_pause()
            # 等待鼠标点击按钮事件
            while not flag:
                for event in pygame.event.get():
                    # 检测到鼠标点击事件
                    if event.type == MOUSEBUTTONDOWN:
                        self.mouse_pos = pygame.mouse.get_pos()
                        self.button_game_continue.coli(self.mouse_pos[0], self.mouse_pos[1])
                    # 检测到Enter键被点击
                    if event.type == KEYDOWN and event.key == K_RETURN:
                        self.button_game_continue.status = True
                    # 确定鼠标点击了按钮，跳出flag循环，继续游戏
                    if self.button_game_continue.status is True:
                        flag = True
                        self.button_game_continue.status = False
                        self.leader.health = 100

    # 记录分数和结束时间数据
    def save_record(self):
        # 结束时间
        end_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        # 分数
        score = self.leader.score
        # 排名
        rank = 1
        # 记录表
        data = [[score, end_time]]
        with open(r'data.csv', mode='r', encoding='utf-8') as fp:
            # 创建一个csv的写对象
            reader = csv.reader(fp)
            # 录入信息到表中
            for row in reader:
                data.append(row)
                rank += 1
                # 只记录前十名分数
                if rank > 10:
                    break
        # 将每个记录的分数转换为int类型
        for i in range(len(data)):
            data[i][0] = int(data[i][0])
        # 降序排序（根据每个元素的第一个值）
        data.sort(key=lambda x: x[0], reverse=True)
        # 删除最后一个元素(保留十个记录）
        if len(data) > 10:
            del data[-1]
        # 向文件写入排序后的记录表
        with open(r'data.csv', mode='w', encoding='utf-8',newline='') as fp:
            # 创建一个csv的写对象
            writer = csv.writer(fp)
            for item in data:
                writer.writerow(item)
    # 游戏暂停
    def gameover_pause(self):
        # 游戏暂停只在窗口绘制一次画面，并更新
        # 游戏暂停画面
        self.scene.blit(self.gamepause_image, (self.gamepause_image_x, self.gamepause_image_y))
        # 游戏继续开始按钮界面
        self.button_game_continue.draw()
        pygame.display.update()

    # 游戏结束
    def gameover_quit(self):
        # 窗口绘制游戏结束画面，并更新
        self.scene.blit(self.gameover_image, (self.gameover_image_x, self.gameover_image_y))
        pygame.display.update()
        self.save_record()
        # time.sleep(5)


# 创建主场景
mainScene = MainScene()
# 开始游戏
mainScene.run_scene()
