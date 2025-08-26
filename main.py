######################載入套件######################
import pygame
import sys


######################物件類別######################
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

    # TODO: 可以加入碰撞檢查方法 (例如: collide(ball))，現階段僅負責繪製


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
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

    def set_velocity(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def update(self):
        if self.launched:
            self.x += self.vx
            self.y += self.vy

    def move_with_paddle(self, paddle):
        # 將球置於底板上方中央（未發射時）
        self.x = paddle.x + paddle.width / 2
        self.y = paddle.y - self.radius - 1

    def check_wall_collision(self, width, height):
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
        # 簡單的 AABB 與圓形碰撞近似：檢查球中心點是否落入磚塊區域擴張 radius 的範圍
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
        # 簡單碰撞處理：若球從上方接觸到底板，則反轉 vy 並根據接觸位置調整 vx
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
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.launched = False


######################主程式######################
if __name__ == "__main__":
    while True:
        clock.tick(60)  # 每秒鐘最多執行60次迴圈

        # 偵測事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 如果按下[X]就退出
                sys.exit()  # 離開遊戲
            # 發射球：空白鍵或滑鼠左鍵
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and balls_to_launch == 0:
                    # 準備發射5顆球
                    balls_to_launch = min(5, len([b for b in balls if not b.launched]))
                    launch_timer = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and balls_to_launch == 0:
                    # 準備發射5顆球
                    balls_to_launch = min(5, len([b for b in balls if not b.launched]))
                    launch_timer = pygame.time.get_ticks()

        # 填充背景顏色
        screen.fill((0, 0, 0))  # 黑色背景
        # 繪製所有磚塊
        for b in bricks:
            b.draw(screen)

        # 每秒增加5顆球
        current_time = pygame.time.get_ticks()
        if current_time - last_add_time >= 1000:  # 每1000毫秒（1秒）
            for i in range(5):
                ball_radius = 8
                ball_color = (255, 255, 0)
                new_ball = Ball(
                    ball_radius,
                    ball_color,
                    paddle.x + paddle.width / 2,
                    paddle.y - ball_radius - 1,
                    launched=False,
                )
                balls.append(new_ball)
            total_balls += 5
            last_add_time = current_time

        # 處理連續發射球
        if balls_to_launch > 0:
            if current_time - launch_timer >= launch_delay:
                # 找到第一個未發射的球
                for ball in balls:
                    if not ball.launched:
                        ball.launched = True
                        # 添加一些隨機性讓球不會完全重疊
                        import random

                        ball.set_velocity(
                            ball_speed * 0.5 + random.uniform(-1, 1), -ball_speed
                        )
                        balls_to_launch -= 1
                        launch_timer = current_time
                        break

        # 繪製分數和球數於左上角
        score_surface = default_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))
        ball_count_surface = default_font.render(
            f"Balls: {len(balls)}", True, (255, 255, 255)
        )
        screen.blit(ball_count_surface, (10, 40))

        # 更新並繪製底板 (paddle)
        keys = pygame.key.get_pressed()
        paddle_speed = 8  # 每幀移動像素數，可調整以改變底板速度
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            paddle.x -= paddle_speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            paddle.x += paddle_speed
        else:
            # 使用滑鼠（以滑鼠 x 為中心）作為備援控制
            mouse_x, _ = pygame.mouse.get_pos()
            paddle.x = mouse_x - paddle.width // 2

        # 邊界限制，確保底板不會移出視窗
        if paddle.x < 0:
            paddle.x = 0
        if paddle.x + paddle.width > width:
            paddle.x = width - paddle.width

        # 繪製底板
        paddle.draw(screen)

        # 處理所有球的邏輯
        balls_to_remove = []
        for i, ball in enumerate(balls):
            if not ball.launched:
                # 未發射時球跟隨底板
                ball.move_with_paddle(paddle)
            else:
                ball.update()
                # 檢查與視窗牆壁碰撞
                ball.check_wall_collision(width, height)
                # 檢查與磚塊碰撞，若有命中則加分
                if ball.check_brick_collision(bricks):
                    score += 100
                # 檢查與底板碰撞
                ball.check_paddle_collision(paddle)

                # 檢查球是否已離開視窗
                if (
                    ball.x + ball.radius < 0
                    or ball.x - ball.radius > width
                    or ball.y - ball.radius > height
                    or ball.y + ball.radius < 0
                ):
                    balls_to_remove.append(i)

        # 移除離開視窗的球
        for i in reversed(balls_to_remove):
            balls.pop(i)

        # 檢查是否所有球都已離開且沒有未發射的球
        if len(balls) == 0:
            # 顯示遊戲結束畫面並等待玩家選擇
            def show_end_screen(message, final_score):
                font = pygame.font.SysFont(None, 48)
                small = pygame.font.SysFont(None, 28)
                while True:
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            sys.exit()
                        if ev.type == pygame.KEYDOWN:
                            if ev.key == pygame.K_r:
                                return "restart"
                            if ev.key == pygame.K_q:
                                sys.exit()
                        if ev.type == pygame.MOUSEBUTTONDOWN:
                            # 左鍵重開，右鍵離開
                            if ev.button == 1:
                                return "restart"
                            if ev.button == 3:
                                sys.exit()

                    # 半透明遮罩
                    overlay = pygame.Surface((width, height))
                    overlay.set_alpha(180)
                    overlay.fill((0, 0, 0))
                    screen.blit(overlay, (0, 0))
                    # 主要訊息
                    text = font.render(message, True, (255, 255, 255))
                    rect = text.get_rect(center=(width // 2, height // 2 - 60))
                    screen.blit(text, rect)
                    # 顯示分數
                    score_text = small.render(
                        f"Score: {final_score}", True, (255, 255, 255)
                    )
                    score_rect = score_text.get_rect(
                        center=(width // 2, height // 2 - 10)
                    )
                    screen.blit(score_text, score_rect)
                    # 次要指示
                    tip = small.render(
                        "Press R to restart, Q to quit (or click left/right)",
                        True,
                        (200, 200, 200),
                    )
                    tipr = tip.get_rect(center=(width // 2, height // 2 + 30))
                    screen.blit(tip, tipr)
                    pygame.display.update()

            choice = show_end_screen("Game Over", score)
            if choice == "restart":
                (
                    bricks,
                    paddle,
                    balls,
                    ball_speed,
                    score,
                    total_balls,
                    last_add_time,
                    balls_to_launch,
                    launch_timer,
                    launch_delay,
                ) = init_game()
                continue

        # 檢查是否已經清除所有磚塊 -> 贏
        if all(b.hit for b in bricks):
            choice = show_end_screen("You Win!", score)
            if choice == "restart":
                (
                    bricks,
                    paddle,
                    balls,
                    ball_speed,
                    score,
                    total_balls,
                    last_add_time,
                    balls_to_launch,
                    launch_timer,
                    launch_delay,
                ) = init_game()
                continue

        # 繪製所有球
        for ball in balls:
            ball.draw(screen)

        # 更新視窗
        pygame.display.update()
