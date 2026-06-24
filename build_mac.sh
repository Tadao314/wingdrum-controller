#!/bin/bash
# ============================================================
# WingDrum Controller — macOS ビルドスクリプト
# 実行前に: pip3 install pyinstaller pywebview pyserial
# ============================================================

set -e

echo "[1/3] PyInstaller でビルド中..."
pyinstaller --clean wingdrum.spec

echo "[2/3] .dmg を作成中..."
# create-dmg がなければインストール（Homebrew必要）
if ! command -v create-dmg &> /dev/null; then
    echo "create-dmg をインストール中..."
    brew install create-dmg
fi

mkdir -p installer

create-dmg \
    --volname "WingDrum Controller" \
    --volicon "wd_bk.png" \
    --window-pos 200 120 \
    --window-size 600 400 \
    --icon-size 100 \
    --icon "WingDrumController.app" 150 190 \
    --hide-extension "WingDrumController.app" \
    --app-drop-link 450 190 \
    "installer/WingDrumController.dmg" \
    "dist/WingDrumController.app"

echo "[3/3] 完了！"
echo "出力: installer/WingDrumController.dmg"
