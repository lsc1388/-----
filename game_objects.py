"""
遊戲物件模組
包含遊戲中的所有物件類別：Brick（磚塊）和 Ball（球）
"""

import pygame
import random


class Brick:
    """簡單的磚塊物件

    屬性:
        width, height: 寬與高
        x, y: 位置（左上角）
        color: 顏色 tuple (R,G,B)，由使用者提供
        hit: 是否已被打到（預設 False）
    """

    def __init__(self, width, height, x, y, color, hit=False):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.hit = hit

    def draw(self, surface, x=None, y=None):
        """在指定的 surface 上繪製磚塊。

        可選的 x, y 參數會暫時覆蓋磚塊本身的座標來繪製。
        只有當 self.hit == False 時才會繪製（被打到的磚塊不顯示）。
        """
        if self.hit:
            return

        draw_x = self.x if x is None else x
        draw_y = self.y if y is None else y
        rect = pygame.Rect(draw_x, draw_y, self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)


class Ball:
    """球物件

    屬性:
        radius: 半徑
        color: (R,G,B)
        x, y: 中心座標
        launched: 是否已發射 (bool)
        vx, vy: 速度 (像素/frame)

    方法:
        draw(surface): 繪製球
        update(): 根據速度移動
        set_velocity(vx, vy): 設定速度
        move_with_paddle(paddle): 在未發射時跟隨底板位置
        check_wall_collision(width, height): 與視窗邊界碰撞處理
        check_brick_collision(bricks): 與磚塊碰撞（標記磚塊為 hit，並反彈）
        check_paddle_collision(paddle): 與底板碰撞
        reset(x, y): 重置到指定位置並設為未發射
    """

    def __init__(self, radius, color, x, y, launched=False):
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y
        self.launched = launched
        self.vx = 0
        self.vy = 0

    def draw(self, surface):
        """繪製球"""
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def set_velocity(self, vx, vy):
        """設定球的速度"""
        self.vx = vx
        self.vy = vy

    def update(self):
        """根據速度更新球的位置"""
        if self.launched:
            self.x += self.vx
            self.y += self.vy

    def move_with_paddle(self, paddle):
        """將球置於底板上方中央（未發射時）"""
        self.x = paddle.x + paddle.width / 2
        self.y = paddle.y - self.radius - 1

    def check_wall_collision(self, width, height):
        """檢查與視窗邊界的碰撞"""
        collided = False
        # 左右牆
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = -self.vx
            collided = True
        elif self.x + self.radius >= width:
            self.x = width - self.radius
            self.vx = -self.vx
            collided = True
        # 上牆
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy = -self.vy
            collided = True
        return collided

    def check_brick_collision(self, bricks):
        """檢查與磚塊的碰撞

        簡單的 AABB 與圓形碰撞近似：檢查球中心點是否落入磚塊區域擴張 radius 的範圍
        """
        for b in bricks:
            if b.hit:
                continue
            # 磚塊矩形
            left = b.x
            right = b.x + b.width
            top = b.y
            bottom = b.y + b.height

            # 找到球到矩形的最近點
            nearest_x = max(left, min(self.x, right))
            nearest_y = max(top, min(self.y, bottom))
            dx = self.x - nearest_x
            dy = self.y - nearest_y
            if dx * dx + dy * dy <= self.radius * self.radius:
                # 標記磚塊為已被打到
                b.hit = True
                # 簡單反彈：根據接觸方向反轉 vx 或 vy
                # 判斷從哪個方向撞擊（水平或垂直分量較大）
                if abs(dx) > abs(dy):
                    self.vx = -self.vx
                else:
                    self.vy = -self.vy
                return True
        return False

    def check_paddle_collision(self, paddle):
        """檢查與底板的碰撞

        簡單碰撞處理：若球從上方接觸到底板，則反轉 vy 並根據接觸位置調整 vx
        """
        # 檢查球是否在底板水平範圍內，且底部接觸到底板上方
        left = paddle.x
        right = paddle.x + paddle.width
        top = paddle.y
        if (
            (self.x + self.radius >= left)
            and (self.x - self.radius <= right)
            and (self.y + self.radius >= top)
            and (self.y - self.radius <= top + paddle.height)
        ):
            # 只在球向下移動時處理碰撞
            if self.vy > 0:
                self.y = top - self.radius - 1
                self.vy = -abs(self.vy)
                # 根據碰撞位置調整水平速度，讓玩家能控制反彈角度
                offset = (self.x - (paddle.x + paddle.width / 2)) / (paddle.width / 2)
                self.vx += offset * 2  # 可調整的影響因子
                return True
        return False

    def reset(self, x, y):
        """重置球到指定位置並設為未發射"""
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.launched = False
