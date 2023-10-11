import pygame


class Button:
    status = False              # False 为按钮未选中，True为被选中
    scene = None
    image = None
    x = 0
    y = 0
    weight = 0
    height = 0
    image_path = "./resources/images/button/"

    def __init__(self, scene, x, y, button_kind):
        self.scene = scene
        self.x = x
        self.y = y
        self.image_path += button_kind
        self.image = pygame.image.load(self.image_path)
        self.weight = self.image.get_width()
        self.height = self.image.get_height()

    def draw(self):
        self.scene.blit(self.image, (self.x, self.y))

    # 检测鼠标是否按下按钮界面
    def coli(self, x, y):
        if self.status is False and (self.x <= x <= self.x + self.weight or self.y <= y <= self.y + self.height):
            self.status = True

