# 雷達數據處理

本專案透過 CAN 匯流排與雷達感測器連接，處理傳入的數據以偵測和追蹤物件，記錄相關資訊，並為雷達數據的可視化和網路傳輸提供框架。系統可透過 `radar.ini` 檔案進行配置。

## 主要功能

* **CAN 匯流排通訊:** 使用提供的 `libcontrolcan.so` (Linux) 函式庫，透過相容 USBCAN-II 的設備（或類似設備）與雷達感測器通訊。
* **雷達配置:** 從 `radar.ini` 讀取雷達操作參數和濾波器設定，並在啟動時相應地配置雷達。
* **物件偵測與解析:** 解析 CAN 訊息以提取雷達狀態和偵測到的物件詳細資訊，包括：
    * 物件 ID
    * 縱向和橫向距離
    * 相對縱向速度
    * 雷達截面積 (RCS)
    * 物件類型（例如：汽車、行人 - 基於雷達的分類）
    * 物件尺寸（長度、寬度 - 如果雷達提供）
* **物件管理:** 維護當前偵測到的物件列表。
* **地理座標計算:** 根據雷達自身配置的 GPS 位置和物件的相對位置，計算偵測到物件的估計緯度和經度。
* **數據記錄:**
    * 將處理後的物件數據記錄到 `logs/` 目錄下每小時輪替的日誌檔案中。
    * 日誌條目包含時間戳、偵測到的物件數量以及每個物件的詳細資訊（ID、地理座標、距離、類型、RCS、速度）。
* **可視化 (可選):** 包含 `movie_writer.py`，可使用 `matplotlib` 對偵測到的物件進行即時的 2D 散點圖可視化。此功能存在，但需要在 `radar.py` 中取消註解並可能進行調整。
* **UDP 數據傳輸 (可選):** 在 `radar.py` 中包含註解掉的程式碼，用於透過 UDP 將處理後的物件數據發送到指定的 IP 位址和連接埠。

## 環境需求

* **Python:** Python 3.8 (建議使用 64 位元版本，如程式碼註解所示)。
* **Python 函式庫:**
    * `matplotlib` (若您計劃使用可視化功能):
        ```bash
        pip install matplotlib
        ```
* **CAN 函式庫:**
    * Linux: `libcontrolcan.so`
    * Windows: `ControlCAN.dll`
    此函式庫檔案必須放置在與 `radar.py` 相同的目錄中，或系統可以找到的路徑（例如系統函式庫路徑）。腳本目前嘗試載入 `./libcontrolcan.so`。

## 安裝與設定

1.  **克隆儲存庫 (若適用) 或下載檔案:**
    確保所有專案檔案 (`radar.py`, `Can.py`, `utlis.py`, `log.py`, `movie_writer.py`, `radar.ini`) 位於同一目錄中。

2.  **安裝 Python 與依賴套件:**
    * 安裝 Python 3.8 (64 位元)。
    * 若需可視化功能，安裝 `matplotlib`:
        ```bash
        pip install matplotlib
        ```

3.  **放置 CAN 函式庫:**
    取得適用於您的 CAN 介面設備的 `libcontrolcan.so` (Linux) 或 `ControlCAN.dll` (Windows) 檔案。將此檔案放置在專案的根目錄（與 `radar.py` 同級）。

4.  **連接 CAN 設備:**
    將您的 CAN 介面設備連接到您的電腦，並連接到雷達的 CAN 匯流排。

## 設定檔案 (`radar.ini`)

`radar.ini` 檔案對於設定雷達感測器和應用程式至關重要。

* **`[DEFAULT]` 區段:**
    * **雷達參數:** `OutputType`, `MaxDistance_Valid`, `MaxDistance`, `Sensor_ID_Valid`, `Sensor_ID`, `RCS_Threshold_Valid`, `RCS_Threshold`, `SendExtInfo`, `SendQuality` 等。這些設定控制雷達的操作模式、偵測範圍以及輸出的數據類型，相關最大值請參閱ARS-408使用手冊。
    * **濾波器設定:** 前綴為Filter_的都為濾波器的參數。這些參數允許您在雷達上定義濾波器，以根據物件的屬性（例如距離、速度、RCS、存在機率）忽略某些物件，相關數值也請參閱ARS-408使用手冊
    * **請參考您的雷達感測器技術文件**以了解每個參數的含義和有效值。

* **`[LOCATION]` 區段:**
    * `Lat`: 雷達實際安裝位置的緯度 (十進制度)。
    * `Lon`: 雷達實際安裝位置的經度 (十進制度)。
    這些值用於計算偵測到物件的絕對地理座標。

## 如何使用

1.  **確認硬體連接:** 確保 CAN 設備已正確連接到 PC 和雷達。
2.  **配置 `radar.ini`:** 編輯 `radar.ini` 以符合您的雷達規格、所需的濾波器以及雷達的實際地理位置。
3.  **執行腳本:**
    打開終端機或命令提示字元，導航到專案目錄，然後執行：
    ```bash
    sudo python3 radar.py
    ```

    腳本將嘗試：
    * 開啟 CAN 設備。
    * 初始化 CAN 通道。
    * 將從 `radar.ini` 產生的設定訊息發送到雷達。
    * 在單獨的執行緒中開始接收和處理雷達數據。
    * 啟動一個執行緒以每小時輪替日誌檔案。

## 輸出結果

* **主控台輸出:**
    * 初始化期間的狀態訊息 (例如 "調用 VCI_OpenDevice成功")。
    * 雷達配置傳輸的確認訊息。
    * 每個掃描週期的偵測物件摘要，包括總數和每個物件的詳細格式化字串（ID、緯度、經度、距離、類型、RCS、速度）。
* **日誌檔案:**
    * 位於 `logs/` 目錄下 (若不存在則會自動建立)。
    * 日誌檔案根據其建立的小時命名，例如 `YYYY-MM-DD HH.log`。
    * 每個日誌條目都帶有時間戳，並包含與列印到主控台相同的偵測物件詳細資訊。

## 檔案結構

* `radar.py`: 主要應用程式腳本。處理 CAN 設備初始化、雷達配置、數據接收、處理、記錄和多執行緒。
* `Can.py`: 定義了與 `ControlCAN` 函式庫互動的 `ctypes` 結構 (`VCI_INIT_CONFIG`, `VCI_CAN_OBJ` 等)。
* `utlis.py`: 包含工具類別與函式：
    * `Radar_Config`, `Filters`, `FilterCfg`: 用於解析 `radar.ini` 並建立 CAN 配置訊息。
    * `Radar_State`, `FilterStatus`: 用於解析雷達的狀態訊息。
    * `Object`: 代表一個偵測到的雷達物件，包含從 CAN 訊息解析數據和計算座標的方法。
    * `Object_list`: 管理偵測到的 `Object` 實例集合。
    * 座標轉換函式。
* `log.py`: 實作了 `DynamicFileHandler` 以每小時建立和輪替日誌檔案。
* `movie_writer.py`: 提供了 `AnimatedPoint` 類別，用於基於 `matplotlib` 的即時雷達目標可視化 (可選，需在 `radar.py` 中取消註解)。
* `radar.ini`: 雷達參數、濾波器與位置的設定檔。
* `libcontrolcan.so` / `ControlCAN.dll`: (使用者提供) 用於 CAN 通訊的外部函式庫。


##雷達相關文件
* 雲端連結:https://drive.google.com/drive/u/0/folders/1YFao-appYF70aJp7UgTYSt7rUsumYX9t
## 疑難排解與注意事項

* **CAN 函式庫不匹配:** 請確保 `libcontrolcan.so` 或 `ControlCAN.dll` 與您的作業系統 (32位元/64位元) 和您的特定 CAN 介面硬體相容。腳本嘗試載入 `./libcontrolcan.so`，如有必要，請在 `radar.py` 中調整路徑或檔名。
* **未偵測到 CAN 設備:** 確認您的 CAN 設備驅動程式已正確安裝，並且設備已被系統識別。
* **雷達配置錯誤:** 如果雷達行為不如預期，請仔細核對 `radar.ini` 中的參數與您的雷達文件。
* **Python 版本:** 程式碼包含類似 "python3.8.0 64位" 的註解，表明偏好此版本和架構。
* **可視化/UDP:** 可視化和 UDP 傳輸功能存在於 `radar.py` 中，但目前已被註解。您需要取消註解並可能調整這些部分才能使用它們。

---

希望這份中文版的 README 能幫助到您！您可以根據您的具體雷達型號或特定設定添加更多詳細資訊。
