# Breath_Shield

## 項目概述

本項目旨在創建一個基於Flask的AI服務，該服務使用攝像頭實時獲取視頻流，並進行圖像處理和預測。通過ASP.NET控制器接收並轉發攝像頭IP地址，確保攝像頭和AI服務之間的通信順暢。

## 系統架構

1. **Flask應用**：處理攝像頭視頻流並進行AI預測。
2. **ASP.NET應用**：接收前端用戶輸入的攝像頭IP地址並將其轉發給Flask應用。
3. **前端頁面**：允許用戶輸入攝像頭和Flask服務器的IP地址，並動態顯示預測結果。

## 文件結構

```
.
├── .gitignore
├── Breath_Shield/
│   ├── Controllers/
│   │   └── CameraController.cs
│   ├── css/
│   │   └── Camera.css
│   ├── index.html
│   ├── js/
│   │   └── Camera.js
├── keras_model.h5
├── labels.txt
├── main.py
└── README.md
```

## 設置步驟

### 1. 安裝依賴

首先，確保你安裝了所有必需的依賴項：

- 對於Flask應用，安裝以下Python庫：
  ```bash
  pip install flask opencv-python-headless numpy tensorflow
  ```

- 對於ASP.NET應用，確保你的項目中安裝了必要的包，包括HttpClient等。

### 2. 配置Flask應用

在Flask應用中：

- 加載模型和標籤文件。
- 初始化攝像頭變量。
- 創建一個端點，用於接收和設置攝像頭的IP地址。
- 創建另一個端點，用於獲取AI預測結果。

### 3. 配置ASP.NET應用

在ASP.NET應用中：

- 創建一個控制器，用於接收前端發送的攝像頭IP地址。
- 使用HttpClient將攝像頭IP地址POST給Flask應用。
- 創建另一個端點，用於從Flask應用獲取預測結果。

### 4. 創建前端頁面

在前端頁面中：

- 創建輸入框，允許用戶輸入攝像頭和Flask服務器的IP地址。
- 創建一個按鈕，用於提交這些IP地址。
- 使用JavaScript將IP地址發送到ASP.NET應用，並更新頁面上的視頻流和預測結果。

## 使用步驟

1. **啟動Flask服務**：
   - 確保Flask應用和攝像頭可用。
   - 運行Flask應用，監聽指定的端口。

2. **啟動ASP.NET服務**：
   - 確保ASP.NET應用已正確配置並能夠與Flask應用通信。
   - 運行ASP.NET應用，監聽指定的端口。

3. **使用前端頁面**：
   - 在瀏覽器中打開前端頁面。
   - 輸入攝像頭IP地址和Flask服務器IP地址。
   - 點擊“更新IP”按鈕。
   - 頁面將顯示來自攝像頭的視頻流，並不斷更新預測結果。

## 常見問題

1. **無法連接攝像頭**：
   - 檢查攝像頭的IP地址是否正確。
   - 確保攝像頭服務器正在運行並且可以訪問。

2. **Flask應用未返回預測結果**：
   - 檢查Flask應用的日誌，確認是否正確接收到攝像頭IP地址。
   - 確保模型文件和標籤文件已正確加載。

3. **前端頁面未更新**：
   - 檢查瀏覽器控制台是否有錯誤信息。
   - 確認ASP.NET應用是否正確接收並轉發了IP地址。

通過上述步驟，你可以成功設置和運行基於Flask和ASP.NET的實時視頻流AI預測系統。如有任何疑問或需要進一步的幫助，請參考相關文檔或聯繫項目維護者。

---
## 支援

- 如果遇到任何問題，請聯絡 [Roger] (hiaconde@gmail.com)。
- 詳細資料 (https://hackmd.io/@NnknBWhxTNGvs1jO3I8-bQ/ByOtKFP4A)
