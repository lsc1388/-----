"""
遊戲配置模組
包含所有遊戲相關的常數和設定
"""

# 視窗設定
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "敲磚塊遊戲"

# 顏色定義 (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# 磚塊設定
BRICK_COLS = 10  # 列數 (x 方向)
BRICK_ROWS = 5  # 行數 (y 方向)
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
BRICK_PADDING = 5  # 磚塊間隔
BRICK_OFFSET_Y = 60  # 上方邊距

# 底板設定
PADDLE_WIDTH = BRICK_WIDTH * 2  # 底板寬度
PADDLE_HEIGHT = 16
PADDLE_Y = WINDOW_HEIGHT - 60  # 底板 Y 座標
PADDLE_COLOR = GRAY
PADDLE_SPEED = 8  # 底板移動速度

# 球設定
BALL_RADIUS = 8
BALL_COLOR = YELLOW
BALL_SPEED = 10  # 球的基本速度
INITIAL_BALL_COUNT = 5  # 初始球數量
BALLS_ADD_INTERVAL = 1000  # 每秒增加球的間隔 (毫秒)
BALLS_ADD_COUNT = 5  # 每次增加的球數量

# 發射設定
LAUNCH_DELAY = 300  # 每顆球間隔發射時間 (毫秒)

# 遊戲設定
FPS = 60  # 每秒畫面數
SCORE_PER_BRICK = 100  # 每個磚塊的分數

# 字型設定
FONT_SIZE = 28
LARGE_FONT_SIZE = 48

# SDL 視窗位置設定
SDL_VIDEO_CENTERED = "1"
