"""
遊戲邏輯模組
包含主要的遊戲循環和邏輯處理
"""

import pygame
import sys
import random
from game_objects import Ball, Explosion
from config import *
from utils import *


class BrickBreakerGame:
    """敲磚塊遊戲主要類別"""

    def __init__(self):
        """初始化遊戲"""
        # 初始化 pygame
        pygame.init()

        # 在建立視窗前嘗試將視窗置中
        import os

        os.environ.setdefault("SDL_VIDEO_CENTERED", SDL_VIDEO_CENTERED)

        # 建立遊戲視窗和時鐘
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        # 建立字型
        self.default_font = pygame.font.SysFont(None, FONT_SIZE)

        # 初始化遊戲狀態
        self.reset_game()

    def reset_game(self):
        """重置遊戲狀態"""
        (
            self.bricks,
            self.paddle,
            self.balls,
            self.score,
            self.total_balls,
            self.last_add_time,
            self.balls_to_launch,
            self.launch_timer,
        ) = init_game()

        # 初始化爆炸效果列表
        self.explosions = []

    def handle_events(self):
        """處理遊戲事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # 發射球：空白鍵或滑鼠左鍵
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.balls_to_launch == 0:
                    self._prepare_launch()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.balls_to_launch == 0:
                    self._prepare_launch()

    def _prepare_launch(self):
        """準備發射球"""
        unlaunched_balls = [b for b in self.balls if not b.launched]
        self.balls_to_launch = min(5, len(unlaunched_balls))
        self.launch_timer = pygame.time.get_ticks()

    def update_game_logic(self):
        """更新遊戲邏輯"""
        current_time = pygame.time.get_ticks()

        # 每秒增加5顆球
        if current_time - self.last_add_time >= BALLS_ADD_INTERVAL:
            for i in range(BALLS_ADD_COUNT):
                new_ball = Ball(
                    BALL_RADIUS,
                    BALL_COLOR,
                    self.paddle.x + self.paddle.width / 2,
                    self.paddle.y - BALL_RADIUS - 1,
                    launched=False,
                )
                self.balls.append(new_ball)
            self.total_balls += BALLS_ADD_COUNT
            self.last_add_time = current_time

        # 處理連續發射球
        if self.balls_to_launch > 0:
            if current_time - self.launch_timer >= LAUNCH_DELAY:
                self._launch_next_ball(current_time)

        # 更新底板位置
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        update_paddle_position(self.paddle, keys, mouse_pos)

        # 處理所有球的邏輯
        self._update_balls()

        # 更新爆炸效果
        self._update_explosions()

    def _launch_next_ball(self, current_time):
        """發射下一顆球"""
        for ball in self.balls:
            if not ball.launched:
                ball.launched = True
                # 添加一些隨機性讓球不會完全重疊
                ball.set_velocity(BALL_SPEED * 0.5 + random.uniform(-1, 1), -BALL_SPEED)
                self.balls_to_launch -= 1
                self.launch_timer = current_time
                break

    def _update_balls(self):
        """更新所有球的狀態"""
        balls_to_remove = []

        for i, ball in enumerate(self.balls):
            if not ball.launched:
                # 未發射時球跟隨底板
                ball.move_with_paddle(self.paddle)
            else:
                ball.update()
                # 檢查與視窗牆壁碰撞
                ball.check_wall_collision(WINDOW_WIDTH, WINDOW_HEIGHT)
                # 檢查與磚塊碰撞，若有命中則加分並創建爆炸效果
                hit_brick = ball.check_brick_collision(self.bricks)
                if hit_brick:
                    self.score += SCORE_PER_BRICK
                    # 創建爆炸效果在磚塊中心位置
                    explosion_x = hit_brick.x + hit_brick.width / 2
                    explosion_y = hit_brick.y + hit_brick.height / 2
                    explosion = Explosion(explosion_x, explosion_y, hit_brick.color)
                    self.explosions.append(explosion)
                # 檢查與底板碰撞
                ball.check_paddle_collision(self.paddle)

                # 檢查球是否已離開視窗
                if self._is_ball_out_of_bounds(ball):
                    balls_to_remove.append(i)

        # 移除離開視窗的球
        for i in reversed(balls_to_remove):
            self.balls.pop(i)

    def _update_explosions(self):
        """更新爆炸效果"""
        explosions_to_remove = []

        for i, explosion in enumerate(self.explosions):
            explosion.update()
            if explosion.is_finished():
                explosions_to_remove.append(i)

        # 移除已結束的爆炸效果
        for i in reversed(explosions_to_remove):
            self.explosions.pop(i)

    def _is_ball_out_of_bounds(self, ball):
        """檢查球是否離開視窗範圍"""
        return (
            ball.x + ball.radius < 0
            or ball.x - ball.radius > WINDOW_WIDTH
            or ball.y - ball.radius > WINDOW_HEIGHT
            or ball.y + ball.radius < 0
        )

    def check_game_state(self):
        """檢查遊戲狀態（勝利或失敗）"""
        # 檢查是否所有球都已離開且沒有未發射的球
        if len(self.balls) == 0:
            choice = show_end_screen(self.screen, "Game Over", self.score)
            if choice == "restart":
                self.reset_game()
            else:
                sys.exit()

        # 檢查是否已經清除所有磚塊 -> 贏
        if all(b.hit for b in self.bricks):
            choice = show_end_screen(self.screen, "You Win!", self.score)
            if choice == "restart":
                self.reset_game()
            else:
                sys.exit()

    def render(self):
        """渲染遊戲畫面"""
        # 填充背景顏色
        self.screen.fill(BLACK)

        # 繪製所有磚塊
        for brick in self.bricks:
            brick.draw(self.screen)

        # 繪製底板
        self.paddle.draw(self.screen)

        # 繪製所有球
        for ball in self.balls:
            ball.draw(self.screen)

        # 繪製爆炸效果
        for explosion in self.explosions:
            explosion.draw(self.screen)

        # 繪製分數和球數於左上角
        score_surface = self.default_font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_surface, (10, 10))

        ball_count_surface = self.default_font.render(
            f"Balls: {len(self.balls)}", True, WHITE
        )
        self.screen.blit(ball_count_surface, (10, 40))

        # 更新顯示
        pygame.display.update()

    def run(self):
        """運行主遊戲循環"""
        while True:
            self.clock.tick(FPS)  # 控制幀率

            self.handle_events()
            self.update_game_logic()
            self.check_game_state()
            self.render()
