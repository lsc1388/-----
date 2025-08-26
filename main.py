"""敲磚塊遊戲主檔案.

直接執行此檔案即可玩遊戲。
"""

from game_logic import BrickBreakerGame


if __name__ == "__main__":
    print("正在啟動敲磚塊遊戲...")
    game = BrickBreakerGame()
    game.run()
