@echo off
cd /d "c:\Users\ASUS\Desktop\敲磚塊遊戲"
echo Adding files to git...
git add .
echo Files added. Committing...
git commit -m "重構專案：實現模組化架構和完整功能

- 新增模組化檔案結構
- config.py: 遊戲設定和常數管理
- game_objects.py: Brick 和 Ball 類別
- game_logic.py: BrickBreakerGame 主要遊戲邏輯
- utils.py: 輔助函式和初始化功能
- start_game.py: 簡潔的遊戲啟動檔案
- requirements.txt: 專案依賴管理
- 更新 README.md: 完整的專案說明文檔
- 重構 main.py: 修正多球邏輯和遊戲流程

功能改進:
- 多球同時發射系統
- 每秒自動增加新球
- 完整的碰撞檢測和物理反彈
- 遊戲狀態管理（勝利/失敗）
- 模組化設計便於維護和擴展"
echo Commit completed. Pushing to GitHub...
git push origin master
echo Upload completed!
pause