# 路由與頁面設計文件 (Routes Design)

本文件根據產品需求文件 (PRD)、系統架構 (ARCHITECTURE) 與資料庫設計 (DB_DESIGN)，規劃「食譜收藏夾系統」的所有路由與頁面結構。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| **首頁與瀏覽** | | | | |
| 系統首頁 | GET | `/` | `main/index.html` | 顯示最新與推薦食譜 |
| 食譜搜尋 | GET | `/search` | `main/search.html` | 接收 `q` 或 `ingredients` 參數進行搜尋 |
| **使用者驗證 (Auth)** | | | | |
| 註冊頁面 | GET | `/register` | `auth/register.html` | 顯示註冊表單 |
| 執行註冊 | POST | `/register` | — | 接收註冊資料、建立 User、重導向至登入 |
| 登入頁面 | GET | `/login` | `auth/login.html` | 顯示登入表單 |
| 執行登入 | POST | `/login` | — | 驗證密碼，儲存 session，重導向至首頁 |
| 執行登出 | POST | `/logout` | — | 清除 session，重導向至首頁 |
| **食譜管理 (Recipe)** | | | | |
| 個人食譜面板 | GET | `/recipes` | `recipe/dashboard.html` | 顯示使用者收藏/建立的食譜列表 |
| 新增食譜頁面 | GET | `/recipes/new` | `recipe/new.html` | 顯示新增表單 |
| 建立食譜 | POST | `/recipes/new` | — | 建立 Recipe, Ingredient, 步驟，重導向至詳情 |
| 食譜詳情 | GET | `/recipes/<int:id>` | `recipe/detail.html` | 顯示食譜完整內容，包含份量動態換算邏輯 |
| 編輯食譜頁面 | GET | `/recipes/<int:id>/edit`| `recipe/edit.html` | 顯示編輯表單，帶入舊有資料 |
| 更新食譜 | POST | `/recipes/<int:id>/edit`| — | 更新 Recipe 資料，重導向至詳情頁 |
| 刪除食譜 | POST | `/recipes/<int:id>/delete`| — | 刪除指定 Recipe，重導向至個人面板 |
| **購買清單 (Shopping List)**| | | | |
| 購買清單面板 | GET | `/list` | `list/index.html` | 顯示使用者的購買清單 |
| 一鍵加入清單 | POST | `/list/add/<int:recipe_id>`| — | 將食譜食材加總存入 ShoppingListItem，重導 |
| 更新項目狀態 | POST | `/list/item/<int:item_id>`| — | 打勾/取消打勾 (is_bought)，可透過 AJAX 實作 |
| 移除項目 | POST | `/list/item/<int:item_id>/delete`| — | 刪除單一購買項目 |

## 2. 每個路由的詳細說明

### 2.1 首頁與搜尋 (main)
- **`GET /`**：
  - 輸入：無。
  - 邏輯：呼叫 `Recipe.get_all()` 或設計推薦邏輯抓取最新幾筆資料。
  - 輸出：渲染 `main/index.html`。
- **`GET /search`**：
  - 輸入：`?q=keyword` 或 `?ingredients=A,B`。
  - 邏輯：根據參數使用 LIKE 搜尋 Recipe 標題，或 JOIN Ingredient 比對。
  - 輸出：將結果清單傳入 `main/search.html` 渲染。未找到時顯示提示。

### 2.2 使用者驗證 (auth)
- 登入、註冊與登出處理。POST 操作成功後都會進行重導向 (Redirect)，失敗時利用 Flash message 與原表單模板顯示錯誤訊息。

### 2.3 食譜操作 (recipe)
- **`GET /recipes/new` & `POST /recipes/new`**：
  - 登入保護 (Login required)。
  - POST 時接收表單資料，呼叫 `Recipe.create()`、`Ingredient.create()` 等。
- **`GET /recipes/<id>`**：
  - 查無資料丟 404 錯誤。將食譜資料傳給前端 Jinja2。
- **編輯與刪除**：
  - 只有該食譜的 `user_id`（作者）才能存取。如非作者回傳 403。

### 2.4 購買清單 (shopping list)
- **`POST /list/add/<int:recipe_id>`**：
  - 取得該食譜所有 Ingredient，按比例換算後，為特定使用者建立 ShoppingListItem。

## 3. Jinja2 模板清單

所有的模板皆會繼承自共用的 `base.html`，以保持 Navbar 與 Footer 等全站一致性。

- `templates/base.html` (全站共用母片)
- `templates/main/index.html` (首頁)
- `templates/main/search.html` (搜尋結果)
- `templates/auth/login.html` (登入)
- `templates/auth/register.html` (註冊)
- `templates/recipe/dashboard.html` (個人食譜面板)
- `templates/recipe/new.html` (新增食譜)
- `templates/recipe/edit.html` (編輯食譜)
- `templates/recipe/detail.html` (食譜詳細內容)
- `templates/list/index.html` (購買清單)
