# WingDrum Controller — ビルド手順

## ファイル構成

```
wingdrum/
├── main.py                  ← Pythonバックエンド
├── index.html               ← GUI本体
├── wd_bk.png                ← ダークモード画像
├── wd_wh.png                ← ライトモード画像
├── wingdrum.spec            ← PyInstaller設定（Win/Mac共通）
├── build_windows.bat        ← Windowsビルド用バッチ
├── wingdrum_installer.iss   ← Inno Setup スクリプト（Windows）
└── build_mac.sh             ← macOSビルド用スクリプト
```

---

## Windows でのビルド手順

### 1. 必要なものをインストール

```bat
pip install pyinstaller pywebview pyserial
```

Inno Setup（インストーラー作成ツール）:  
→ https://jrsoftware.org/isdl.php からダウンロードしてインストール

### 2. ビルド実行

```bat
build_windows.bat をダブルクリック
```

### 3. 出力

```
installer\WingDrumController_Setup.exe
```

これを配布すればOK。受け取った人はダブルクリックでインストールできる。

---

## macOS でのビルド手順

### 1. 必要なものをインストール

```bash
pip3 install pyinstaller pywebview pyserial
brew install create-dmg   # Homebrew必要
```

### 2. ビルド実行

```bash
./build_mac.sh
```

### 3. 出力

```
installer/WingDrumController.dmg
```

これを配布すればOK。受け取った人はdmgをダブルクリック→アプリをApplicationsにドラッグ。

---

## トラブルシューティング

**「WingDrumが認識されない」**  
→ FTDIドライバが必要な場合あり:  
Windows: https://ftdichip.com/drivers/vcp-drivers/  
macOS: 最近のmacOSは標準内蔵のため不要なことが多い

**「WindowsがSmartScreenで警告を出す」**  
→ コードサイニング証明書がないため。「詳細情報」→「実行」で通過できる。  
（オープンソースプロジェクトなのでこれは許容範囲）

**「macOSで"開発元が未確認"と言われる」**  
→ 右クリック→「開く」で初回だけ許可できる。  
または System Settings → Privacy & Security から許可。
