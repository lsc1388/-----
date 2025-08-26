## AI Coding Agent: 敲磚塊遊戲 — 精簡快速上手指南

目的：讓 AI 編碼代理能快速定位修改點、了解架構與常用模式，並能安全地修改與測試遊戲。

主要架構（一眼看懂）

- `start_game.py` — 程式進入點（執行/測試用），會建立 `BrickBreakerGame` 並啟動主迴圈。
- `main.py` — 備援進入點，包含較舊的單檔案實作，但 `start_game.py` 為首選。
- `game_logic.py` — 控制器：`BrickBreakerGame` 負責事件、狀態更新、碰撞處理與繪製流程。
- `game_objects.py` — 實體類別：`Ball`, `Brick`, `Explosion` 等；每個物件實作自己的 `update()`、`draw()` 與碰撞檢查方法。
- `utils.py` — Factory 函式（一致性來源）：請用 `create_paddle()`, `create_initial_balls(paddle)`, `create_bricks()` 等，不要直接 new 類別。
- `config.py` — 所有魔數、顏色與遊戲參數（調整玩法請先改這裡）。

關鍵模式（可直接動手修改）

- **Factory pattern**：建立物件必須走 `utils.py` 的工廠
  ```python
  paddle = create_paddle()
  balls = create_initial_balls(paddle)
  bricks = create_bricks()
  ```
- **事件與流程**：`BrickBreakerGame.handle_events()` 處理按鍵與滑鼠（Space 發射、方向鍵/滑鼠移動、R 重置、Q 離開）
- **碰撞系統**：`Ball` 有 `check_wall_collision`, `check_brick_collision(bricks)`, `check_paddle_collision(paddle)`；`check_brick_collision` 若命中會回傳被擊中的 `Brick` 清單，呼叫方會建立 `Explosion(...)`
- **特殊機制**：球有 10% 機率同時擊中鄰近磚塊；每秒自動增加 5 顆新球；爆炸粒子效果持續 800ms
- **雙控制方式**：鍵盤（左右方向鍵/A/D）+ 滑鼠移動，滑鼠為備援

開發與測試流程（具體指令）

- **安裝**：`pip install -r requirements.txt` （需要 Pygame 2.5.2+）
- **執行**：`python start_game.py` （首選進入點，`main.py` 為備援）
- **小改測試**：調整 `config.py` 常數，或在 `game_logic.py:update_game_logic()` 加 debug print，然後重新執行
- **操作驗證**：Space/滑鼠左鍵發射、方向鍵/A/D/滑鼠移動底板、R 重開、Q 離開

專案慣例（不要違反）

- **常數集中化**：所有魔數放 `config.py`（例如 WINDOW_WIDTH、BALL_SPEED、PADDLE_Y）；不要在其他模組寫魔數
- **命名規範**：變數/函數用 snake_case，類別用 PascalCase，常數用 UPPER_CASE
- **註解風格**：區塊分隔用 `######################`、文檔字串用三引號、內容使用繁體中文
- **Factory 強制**：切勿直接用類別建構子建立遊戲物件，改用 `utils` 中的工廠函式

重要整合點與風險區域

- **assets/**: 圖片或音效改動會影響載入路徑，請確認相對路徑
- **Explosion 與 Brick 的生命週期**：刪除磚塊時要同時建立 `Explosion`（位置以 brick 的中心為準）
- **多球系統**：`balls` 是 list，新增/移除需妥善在主迴圈處理以避免 concurrent modification
- **碰撞回傳值**：`check_brick_collision()` 回傳被擊中磚塊清單（可能為空、1 或多個）

快速檢查清單（PR reviewer 用）

- **是否使用 factory** 建立物件？
- **config 的魔數** 是否新增而非散佈於程式中？
- **是否維持中文註解風格**？
- **碰撞邏輯變更** 是否同時建立/清理 Explosion？
- **多球處理** 是否正確處理清單修改？

如有不清楚的地方請回覆想要擴充的段落（例如：示範一個 PR 修改範例或加入 unit-test 模板）。
