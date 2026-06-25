# WingDrum Controller

[PhonicBloom WingDrum](https://www.phonicbloom.com)（ハンドパン型電子楽器）用のPC companion アプリです。

USBケーブル1本でスケール・チューニング・微分音設定・プリセットをPCから操作できます。画面上のドラム図は実機のパッドレイアウトをそのまま再現しています。

![WingDrum Controller](wd_wh.png)

---

## 機能一覧

### 接続
- 起動時にWingDrumを自動検出（FTDI VID照合）
- COMポートの手動選択も可能
- 接続状態をドット＋テキストでリアルタイム表示
- **未接続時もドライランモード**で全操作をプレビュー可能

### 音色（パッチ）切り替え
- 全内蔵音色をワンクリックで即切り替え：
  - Metal 1〜11
  - Wood 1〜5
  - Polyphonic Reverb *（内蔵マイクを使用。誤操作防止のロックボタンつき。スピーカー使用時はフィードバックに注意）*
- パッチ変更はクリック即時送信（Applyボタン不要）

### スケール選択
- 全内蔵スケールをグループ別に表示。グループ名クリックで開閉：
  - **Minor**：Minor、Minor Harmonic、Minor Sharp (G#)、Melodic Minor
  - **Major**：Major、Major Pentatonic、Major Flat
  - **Modes**：Lydian、Phrygian、Phrygian Alt、Ionian、Greek Mixolydian、Altered、Diminished
  - **World**：Kurd Minor、Celtic Minor、Akebono Pentatonic、Annaziska、Pygmy、Deep Sea、Cloud、Celtic 2、Daze、Hijaz、Kurd 2、Voice、Shade
  - **World (Microtonal)**：Rast、Bayati、Saba、Hicaz、Bhairav、Todi、Darbari Kanada、Slendro、Pelog、Bali Pelog
  - **Linear**：Major、Major Flat、Minor、Melodic Minor、Whole Tone、Diminished (H-W)、Altered、Chromatic — すべてD3スタートで音階を時計回りに配置（鍵盤をドラムの周りに並べたイメージ）
  - **User**：自分で登録したカスタムスケール
- Microtonalスケールは選択時に各パッドのセントオフセットを自動適用
- **Transpose**：スケール全体を±6半音シフト
- **Rotation**：パッド割り当てを0〜7ステップ時計回りにずらす
- **Flip L/R**：パッド割り当てを左右ミラー反転

### プリセットスロット
- ドラム図の外周に8つのスロットボタンを表示
- クリックで書き込み先スロットを選択
- 接続時はクリックで実機から現在のスロットデータを取得
- パッチごとにファクトリーリセット可能（確認ダイアログあり）

### ドラム図
- WingDrumの物理パッドレイアウトを再現したSVG図
- 各パッドに音名をリアルタイム表示
- **ドラッグ&ドロップでパッド並び替え**：音名ラベルをつかんで別のパッドにドロップ
- パッドラベルをクリックで微分音ポップアップを表示

### パッド別微分音設定
- パッドラベルをクリックでポップアップ表示
- パッドごとに±50セントのピッチ調整
- セント値はドラム図上にリアルタイム反映（オフセットがある場合は背景円が大きくなる）
- 微分音設定はユーザースケール保存時に一緒に保存される

### グローバルチューニング
- 基準ピッチスライダー：400〜480 Hz
- Fine Tuneスライダー：±0.99 Hz（0.00Hzに戻すリセットボタンつき）
- オクターブシフト：±3オクターブ

### ユーザースケール登録
- 現在のパッドレイアウト（微分音設定を含む）に名前をつけてカスタムスケールとして登録
- 登録したスケールはドロップダウンのUserグループに表示
- ×ボタンで個別に削除可能
- **ユーザースケールはアプリを閉じても保持される**
  - Windows：`%APPDATA%\WingDrumController\`
  - macOS：`~/Library/Application Support/WingDrumController/`

### Applyボタン
- 未送信の変更をまとめて実機に送信：
  - スケール変更 → `SET_SCALE_NOTES`
  - チューニング変更 → `SET_TUNING`
  - パッド微分音変更 → `SET_PAD_TUNING`
- 未送信の変更があるときは赤、実機と同期済みのときは緑で表示

### UI
- ダーク／ライトモード切り替え
- ウィンドウサイズに追従するレスポンシブレイアウト（スクロールバーなし）
- シリアル通信をリアルタイム表示するログエリア

---

## 動作要件

### ハードウェア
- PhonicBloom WingDrum（全シリアルナンバー対応）
- USBケーブル

### ファームウェア
本アプリはUSBシリアルコマンドに対応した **experimental firmware v1.01** が必要です。工場出荷時のファームウェアとは異なります。PhonicBloom Marioとの協力のもと開発されました。

**ダウンロード：**
http://phonicbloom.com/updates/wingdrum/wingdrum_fw-1.01-experimental.bin

**フラッシュ前に元のファームウェアをバックアップ：**
```bash
python -m esptool --port COM4 --baud 115200 read_flash 0x30000 0x60000 wingdrum_backup_original.bin
```

**実験的ファームウェアをフラッシュ：**
```bash
# ブートモード：Power + Metalボタンを押しながらUSB接続
# esptoolが接続したらMetalボタンを離す。Powerは完了まで押し続ける
python -m esptool --port COM4 --baud 115200 write_flash 0x30000 wingdrum_fw-1.01-experimental.bin
```

> `COM4` は実際のポート番号に置き換えてください。macOS/Linuxでは `/dev/tty.usbserial-XXXX` などになります。

> **補足：** ファームウェアは起動時やボタン操作時にデバッグ出力をシリアルに送信します。これは正常な動作です。アプリは自動的に無視します。

### FTDIドライバ（Windowsのみ）
環境によってはFTDI USBシリアルドライバの手動インストールが必要な場合があります：
https://ftdichip.com/drivers/vcp-drivers/

---

## インストール

### Windows
1. [Releases](../../releases) から `WingDrumController_Setup.exe` をダウンロード
2. ダブルクリックしてインストール
3. デスクトップのショートカットまたはスタートメニューから起動

### macOS
1. [Releases](../../releases) から `WingDrumController.dmg` をダウンロード
2. DMGを開いて `WingDrumController.app` をApplicationsフォルダにドラッグ
3. 初回起動時は右クリック→「開く」でGatekeeperを通過

---

## シリアルコマンドリファレンス

開発者向け。firmware v1.01-experimental で動作確認済み。

| コマンド | レスポンス | 備考 |
|---|---|---|
| `GET_TUNING` | `OK:440.00` | 現在の基準ピッチ（Hz） |
| `SET_TUNING:<hz>` | `OK` | 例：`SET_TUNING:432.50` |
| `GET_PATCH` | `OK:metal,0` | 現在の音色とパッチ番号 |
| `SET_PATCH:metal,<0-10>` | `OK` | 送信後700ms待つこと |
| `SET_PATCH:wood,<0-4>` | `OK` | 送信後700ms待つこと |
| `SET_PATCH:reverb` | `OK` | Polyphonic Reverbモード |
| `GET_SCALE` | `OK:60,62,...` | MIDIノート番号9個（現在スロット） |
| `SET_SCALE:<name>` | `OK` | スロット7に書き込む |
| `SET_SCALE_DEF:<slot>,<name>` | `OK` | スロット0〜7に名前つきスケールを登録 |
| `SET_SCALE_NOTES:<slot>,<n0>,...,<n8>` | `OK` | スロットにMIDIノートを直接書き込む |
| `GET_PAD_TUNING:<pad>` | `OK:15.00` | パッドのセントオフセット |
| `SET_PAD_TUNING:<pad>,<cents>` | `OK` | パッド別微分音 ±50セント |

**重要：** シリアルポートを開く前に必ず `dtr=False`、`rts=False` を設定してください。設定しないとWingDrumが接続時にリセットされます。

```python
ser = serial.Serial()
ser.port = 'COM4'
ser.baudrate = 115200
ser.dtr = False
ser.rts = False
ser.open()
```

---

## ソースからビルドする

```bash
pip install pywebview pyserial
python main.py
```

スタンドアロンインストーラーのビルド手順は [BUILD_README.md](BUILD_README.md) を参照してください。

---

## ライセンス

GPL v3。詳細は [LICENSE](LICENSE) を参照。

本プロジェクトはWingDrumオーナーが個人で開発しています。PhonicBloom Marioの協力に感謝します。
