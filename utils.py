"""工具函式模組.

包含遊戲初始化和輔助函式。
"""

import pygame

from config import *
from game_objects import Ball, Brick


def create_bricks():
    """建立並回傳磚塊清單.

    Returns:
        list: 磚塊物件清單
    """
    total_bricks_width = BRICK_COLS * BRICK_WIDTH + (BRICK_COLS - 1) * BRICK_PADDING
    brick_offset_x = (WINDOW_WIDTH - total_bricks_width) // 2
    bricks = []

    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = brick_offset_x + col * (BRICK_WIDTH + BRICK_PADDING)
            y = BRICK_OFFSET_Y + row * (BRICK_HEIGHT + BRICK_PADDING)
            # 根據行列位置生成不同顏色
            color = (
                200 - row * 20 if 200 - row * 20 >= 0 else 0,
                50 + row * 30 if 50 + row * 30 <= 255 else 255,
                50 + col * 10 if 50 + col * 10 <= 255 else 255,
            )
            bricks.append(Brick(BRICK_WIDTH, BRICK_HEIGHT, x, y, color))

    return bricks


def create_paddle():
    """建立並回傳底板物件.

    Returns:
        Brick: 底板物件
    """
    paddle_x = (WINDOW_WIDTH - PADDLE_WIDTH) // 2  # 初始 x 座標置中
    return Brick(PADDLE_WIDTH, PADDLE_HEIGHT, paddle_x, PADDLE_Y, PADDLE_COLOR)


def create_initial_balls(paddle):
    """建立初始球群.

    Args:
        paddle: 底板物件

    Returns:
        list: 初始球物件清單
    """
    balls = []
    for i in range(INITIAL_BALL_COUNT):
        ball = Ball(
            BALL_RADIUS,
            BALL_COLOR,
            paddle.x + paddle.width / 2,
            paddle.y - BALL_RADIUS - 1,
            launched=False,
        )
        balls.append(ball)
    return balls


def init_game():
    """初始化或重置遊戲物件，回傳所有遊戲狀態.

    Returns:
        tuple: 包含所有遊戲狀態的元組
            (bricks, paddle, balls, score, total_balls,
             last_add_time, balls_to_launch, launch_timer)
    """
    paddle = create_paddle()
    balls = create_initial_balls(paddle)
    bricks = create_bricks()

    # 遊戲狀態變數
    score = 0
    total_balls = INITIAL_BALL_COUNT
    last_add_time = pygame.time.get_ticks()
    balls_to_launch = 0
    launch_timer = 0

    return (
        bricks,
        paddle,
        balls,
        score,
        total_balls,
        last_add_time,
        balls_to_launch,
        launch_timer,
    )


def show_end_screen(screen, message, final_score):
    """顯示遊戲結束畫面.

    Args:
        screen: pygame 畫面物件
        message (str): 結束訊息
        final_score (int): 最終分數

    Returns:
        str: 使用者選擇 ('restart' 或 'quit')
    """
    font = pygame.font.SysFont(None, LARGE_FONT_SIZE)
    small_font = pygame.font.SysFont(None, FONT_SIZE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 左鍵重開，右鍵離開
                if event.button == 1:
                    return "restart"
                if event.button == 3:
                    return "quit"

        # 半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # 主要訊息
        text = font.render(message, True, WHITE)
        rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60))
        screen.blit(text, rect)

        # 顯示分數
        score_text = small_font.render(f"Score: {final_score}", True, WHITE)
        score_rect = score_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 10)
        )
        screen.blit(score_text, score_rect)

        # 次要指示
        tip = small_font.render(
            "Press R to restart, Q to quit (or click left/right)",
            True,
            GRAY,
        )
        tip_rect = tip.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        screen.blit(tip, tip_rect)

        pygame.display.update()


def update_paddle_position(paddle, keys, mouse_pos):
    """更新底板位置.

    支援鍵盤左右控制（左右方向鍵或 A/D），若有按鍵則以鍵盤為主；
    否則以滑鼠為備援。

    Args:
        paddle: 底板物件
        keys: pygame 按鍵狀態
        mouse_pos (tuple): 滑鼠位置 (x, y)
    """
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        paddle.x -= PADDLE_SPEED
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        paddle.x += PADDLE_SPEED
    else:
        # 使用滑鼠（以滑鼠 x 為中心）作為備援控制
        mouse_x, _ = mouse_pos
        paddle.x = mouse_x - paddle.width // 2

    # 邊界限制，確保底板不會移出視窗
    if paddle.x < 0:
        paddle.x = 0
    if paddle.x + paddle.width > WINDOW_WIDTH:
        paddle.x = WINDOW_WIDTH - paddle.width
