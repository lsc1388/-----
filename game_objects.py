"""遊戲物件模組.

包含遊戲中的所有物件類別：Brick（磚塊）、Ball（球）和 Explosion（爆炸效果）。
"""

import math
import random

import pygame


class Brick:
    """簡單的磚塊物件.
    
    Attributes:
        width (int): 寬度
        height (int): 高度
        x (int): x 座標（左上角）
        y (int): y 座標（左上角）
        color (tuple): 顏色 tuple (R, G, B)
        hit (bool): 是否已被打到
    """

    def __init__(self, width, height, x, y, color, hit=False):
        """初始化磚塊.
        
        Args:
            width (int): 磚塊寬度
            height (int): 磚塊高度
            x (int): x 座標
            y (int): y 座標
            color (tuple): RGB 顏色值
            hit (bool, optional): 是否已被打到. Defaults to False.
        """
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.hit = hit

    def draw(self, surface, x=None, y=None):
        """在指定的 surface 上繪製磚塊.
        
        可選的 x, y 參數會暫時覆蓋磚塊本身的座標來繪製。
        只有當 self.hit == False 時才會繪製（被打到的磚塊不顯示）。
        
        Args:
            surface: pygame surface 物件
            x (int, optional): 暫時的 x 座標
            y (int, optional): 暫時的 y 座標
        """
        if self.hit:
            return

        draw_x = self.x if x is None else x
        draw_y = self.y if y is None else y
        rect = pygame.Rect(draw_x, draw_y, self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)


class Ball:
    """球物件.
    
    Attributes:
        radius (int): 半徑
        color (tuple): RGB 顏色值
        x (float): x 座標（中心）
        y (float): y 座標（中心）
        launched (bool): 是否已發射
        vx (float): x 方向速度
        vy (float): y 方向速度
    """

    def __init__(self, radius, color, x, y, launched=False):
        """初始化球物件.
        
        Args:
            radius (int): 球的半徑
            color (tuple): RGB 顏色值
            x (float): 初始 x 座標
            y (float): 初始 y 座標
            launched (bool, optional): 是否已發射. Defaults to False.
        """
        self.radius = radius
        self.color = color
        self.x = x
        self.y = y
        self.launched = launched
        self.vx = 0
        self.vy = 0

    def draw(self, surface):
        """繪製球."""
        pygame.draw.circle(
            surface, self.color, (int(self.x), int(self.y)), self.radius
        )

    def set_velocity(self, vx, vy):
        """設定球的速度.
        
        Args:
            vx (float): x 方向速度
            vy (float): y 方向速度
        """
        self.vx = vx
        self.vy = vy

    def update(self):
        """根據速度更新球的位置."""
        if self.launched:
            self.x += self.vx
            self.y += self.vy

    def move_with_paddle(self, paddle):
        """將球置於底板上方中央（未發射時）.
        
        Args:
            paddle: 底板物件
        """
        self.x = paddle.x + paddle.width / 2
        self.y = paddle.y - self.radius - 1

    def check_wall_collision(self, width, height):
        """檢查與視窗邊界的碰撞.
        
        Args:
            width (int): 視窗寬度
            height (int): 視窗高度
            
        Returns:
            bool: 是否發生碰撞
        """
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
        """檢查與磚塊的碰撞.
        
        簡單的 AABB 與圓形碰撞近似：檢查球中心點是否落入磚塊區域擴張 radius 的範圍。
        現在此方法會回傳一個被命中的磚塊清單（可能為空、1 或 2 個）。有 10% 機率
        同一次命中另外一個最近的未被擊中的磚塊。
        
        Args:
            bricks (list): 磚塊清單
            
        Returns:
            list: 被命中的磚塊清單
        """
        for brick in bricks:
            if brick.hit:
                continue
            # 磚塊矩形
            left = brick.x
            right = brick.x + brick.width
            top = brick.y
            bottom = brick.y + brick.height

            # 找到球到矩形的最近點
            nearest_x = max(left, min(self.x, right))
            nearest_y = max(top, min(self.y, bottom))
            dx = self.x - nearest_x
            dy = self.y - nearest_y
            if dx * dx + dy * dy <= self.radius * self.radius:
                hit_bricks = []
                # 標記第一個磚塊為已被打到
                brick.hit = True
                hit_bricks.append(brick)

                # 簡單反彈：根據接觸方向反轉 vx 或 vy
                if abs(dx) > abs(dy):
                    self.vx = -self.vx
                else:
                    self.vy = -self.vy

                # 10% 機率同時命中另一個最近的未被擊中磚塊
                try:
                    chance = random.random()
                except Exception:
                    chance = 1.0

                if chance < 0.1:
                    # 在所有未被擊中的磚塊中找到距離目前被擊中磚塊中心最近的一個
                    brick_center_x = brick.x + brick.width / 2
                    brick_center_y = brick.y + brick.height / 2
                    nearest_other = None
                    nearest_dist_sq = None
                    for other in bricks:
                        if other is brick or other.hit:
                            continue
                        other_x = other.x + other.width / 2
                        other_y = other.y + other.height / 2
                        dist_sq = ((other_x - brick_center_x) ** 2 + 
                                 (other_y - brick_center_y) ** 2)
                        if nearest_other is None or dist_sq < nearest_dist_sq:
                            nearest_other = other
                            nearest_dist_sq = dist_sq

                    if nearest_other is not None:
                        nearest_other.hit = True
                        hit_bricks.append(nearest_other)

                return hit_bricks
        return []

    def check_paddle_collision(self, paddle):
        """檢查與底板的碰撞.
        
        簡單碰撞處理：若球從上方接觸到底板，則反轉 vy 並根據接觸位置調整 vx。
        
        Args:
            paddle: 底板物件
            
        Returns:
            bool: 是否發生碰撞
        """
        # 檢查球是否在底板水平範圍內，且底部接觸到底板上方
        left = paddle.x
        right = paddle.x + paddle.width
        top = paddle.y
        if ((self.x + self.radius >= left) and 
            (self.x - self.radius <= right) and 
            (self.y + self.radius >= top) and 
            (self.y - self.radius <= top + paddle.height)):
            # 只在球向下移動時處理碰撞
            if self.vy > 0:
                self.y = top - self.radius - 1
                self.vy = -abs(self.vy)
                # 根據碰撞位置調整水平速度，讓玩家能控制反彈角度
                offset = ((self.x - (paddle.x + paddle.width / 2)) / 
                         (paddle.width / 2))
                self.vx += offset * 2  # 可調整的影響因子
                return True
        return False

    def reset(self, x, y):
        """重置球到指定位置並設為未發射.
        
        Args:
            x (float): 新的 x 座標
            y (float): 新的 y 座標
        """
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.launched = False


class Explosion:
    """爆炸效果類別.
    
    當磚塊被打中時創建的粒子爆炸效果。
    """

    def __init__(self, x, y, color, particle_count=15):
        """初始化爆炸效果.
        
        Args:
            x (float): 爆炸中心 x 座標
            y (float): 爆炸中心 y 座標
            color (tuple): 爆炸顏色（基於磚塊顏色）
            particle_count (int, optional): 粒子數量. Defaults to 15.
        """
        self.x = x
        self.y = y
        self.particles = []
        self.creation_time = pygame.time.get_ticks()
        self.duration = 800  # 爆炸持續時間（毫秒）

        # 創建粒子
        for _ in range(particle_count):
            # 隨機角度和速度
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)

            particle = {
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "size": random.uniform(2, 6),
                "color": self._vary_color(color),
                "life": 1.0,  # 生命值從1.0開始，逐漸減少到0
            }
            self.particles.append(particle)

    def _vary_color(self, base_color):
        """基於基礎顏色創建變化顏色.
        
        Args:
            base_color (tuple): 基礎 RGB 顏色值
            
        Returns:
            tuple: 變化後的 RGB 顏色值
        """
        r, g, b = base_color
        # 添加一些隨機變化，但保持在有效範圍內
        r = max(0, min(255, r + random.randint(-50, 50)))
        g = max(0, min(255, g + random.randint(-50, 50)))
        b = max(0, min(255, b + random.randint(-50, 50)))
        return (r, g, b)

    def update(self):
        """更新爆炸效果."""
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.creation_time

        # 計算生命值比例
        life_ratio = max(0, 1 - elapsed / self.duration)

        # 更新每個粒子
        for particle in self.particles:
            # 更新位置
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]

            # 添加重力效果
            particle["vy"] += 0.2

            # 更新生命值
            particle["life"] = life_ratio

            # 添加阻力
            particle["vx"] *= 0.98
            particle["vy"] *= 0.98

    def draw(self, surface):
        """繪製爆炸效果.
        
        Args:
            surface: pygame surface 物件
        """
        for particle in self.particles:
            if particle["life"] > 0:
                # 根據生命值調整透明度和大小
                alpha = int(particle["life"] * 255)
                size = int(particle["size"] * particle["life"])

                if size > 0:
                    # 創建帶透明度的surface
                    particle_surface = pygame.Surface(
                        (size * 2, size * 2), pygame.SRCALPHA
                    )
                    color_with_alpha = (*particle["color"], alpha)
                    pygame.draw.circle(
                        particle_surface, color_with_alpha, (size, size), size
                    )

                    # 繪製到主surface
                    surface.blit(
                        particle_surface, 
                        (particle["x"] - size, particle["y"] - size)
                    )

    def is_finished(self):
        """檢查爆炸是否已結束.
        
        Returns:
            bool: 爆炸是否已結束
        """
        current_time = pygame.time.get_ticks()
        return current_time - self.creation_time >= self.duration
