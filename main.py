"""
WingDrum Controller — main.py
PyWebView + pyserial バックエンド
"""

import threading
import os
import sys
import time
import webview
import serial
import serial.tools.list_ports


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)


def user_data_path() -> str:
    """
    ユーザーデータ保存先を返す（ユーザーの目に触れない標準パス）。
    Windows: APPDATA/WingDrumController/
    macOS  : ~/Library/Application Support/WingDrumController/
    Linux  : ~/.config/WingDrumController/
    """
    if sys.platform == 'win32':
        base = os.environ.get('APPDATA', os.path.expanduser('~'))
    elif sys.platform == 'darwin':
        base = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support')
    else:
        base = os.path.join(os.path.expanduser('~'), '.config')
    path = os.path.join(base, 'WingDrumController')
    os.makedirs(path, exist_ok=True)
    return path


WINGDRUM_VID = 0x0403
WINGDRUM_NAME_HINTS = ['wingdrum', 'ftdi', 'usb serial']


def _is_wingdrum(port_info) -> bool:
    if port_info.vid == WINGDRUM_VID:
        return True
    desc = (port_info.description or '').lower()
    mfr  = (port_info.manufacturer or '').lower()
    return any(h in desc or h in mfr for h in WINGDRUM_NAME_HINTS)


class WingDrumAPI:

    def __init__(self):
        self._ser: serial.Serial | None = None
        self._lock = threading.Lock()
        self._window = None

    def set_window(self, window):
        self._window = window

    def _js(self, expr: str):
        if self._window:
            self._window.evaluate_js(expr)

    def _log(self, msg: str, level: str = 'info'):
        safe = msg.replace('\\', '\\\\').replace("'", "\\'")
        self._js(f"window.pyLog('{safe}', '{level}')")

    def scan_ports(self) -> list[dict]:
        ports = serial.tools.list_ports.comports()
        result = []
        for p in sorted(ports, key=lambda x: x.device):
            result.append({
                "port":     p.device,
                "desc":     p.description or p.device,
                "wingdrum": _is_wingdrum(p),
            })
        return result

    def connect(self, port: str) -> dict:
        with self._lock:
            if self._ser and self._ser.is_open:
                self._ser.close()
            try:
                ser = serial.Serial()
                ser.port     = port
                ser.baudrate = 115200
                ser.dtr      = False
                ser.rts      = False
                ser.timeout  = 1
                ser.open()
                self._ser = ser
            except Exception as e:
                self._log(f'Connect failed: {e}', 'error')
                return {"ok": False, "error": str(e)}

        threading.Thread(target=self._drain_boot_log, daemon=True).start()
        self._log(f'Connected to {port}')
        return {"ok": True}

    def _drain_boot_log(self):
        deadline = time.time() + 5.0
        while time.time() < deadline:
            with self._lock:
                if not (self._ser and self._ser.is_open):
                    break
                if self._ser.in_waiting:
                    line = self._ser.readline().decode(errors='replace').strip()
                    if line.startswith('OK') or line.startswith('ERR'):
                        self._log(f'← {line}')
                else:
                    time.sleep(0.05)

    def disconnect(self) -> dict:
        with self._lock:
            if self._ser and self._ser.is_open:
                self._ser.close()
        self._log('Disconnected')
        return {"ok": True}

    def send_command(self, cmd: str) -> dict:
        with self._lock:
            if not (self._ser and self._ser.is_open):
                return {"ok": False, "error": "Not connected"}
            try:
                self._ser.write((cmd + '\n').encode())
                time.sleep(0.3)
                responses = []
                deadline = time.time() + 1.0
                while time.time() < deadline:
                    if self._ser.in_waiting:
                        line = self._ser.readline().decode(errors='replace').strip()
                        if line.startswith('OK') or line.startswith('ERR'):
                            responses.append(line)
                    else:
                        if responses:
                            break
                        time.sleep(0.02)
            except Exception as e:
                return {"ok": False, "error": str(e)}

        # レスポンスが空 = タイムアウト = 失敗扱い
        if not responses:
            return {"ok": False, "error": "No response"}

        resp = '\n'.join(responses)
        self._log(f'→ {cmd}')
        self._log(f'← {responses[0]}', 'ok' if responses[0].startswith('OK') else 'error')
        return {"ok": resp.startswith('OK'), "response": resp}

    def get_initial_state(self) -> dict:
        results = {}
        for cmd in ['GET_TUNING', 'GET_PATCH', 'GET_SCALE']:
            r = self.send_command(cmd)
            results[cmd] = r.get('response', '')
        return results

    def is_connected(self) -> bool:
        return bool(self._ser and self._ser.is_open)

    # ── API: ユーザースケール 保存／読み込み ─────────────────────
    def save_user_scales(self, data: dict) -> dict:
        """
        JS から userScales オブジェクトを受け取り JSON ファイルに保存する。
        保存先: APPDATA/WingDrumController/user_scales.json (Windows)
        """
        import json
        try:
            path = os.path.join(user_data_path(), 'user_scales.json')
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def load_user_scales(self) -> dict:
        """
        保存済みの userScales を読み込んで返す。
        ファイルがなければ空の dict を返す。
        """
        import json
        try:
            path = os.path.join(user_data_path(), 'user_scales.json')
            if not os.path.exists(path):
                return {}
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}


def main():
    api = WingDrumAPI()

    window = webview.create_window(
        title     = 'WingDrum Controller',
        url       = resource_path('index.html'),
        js_api    = api,
        width     = 780,
        height    = 960,
        resizable = True,
        min_size  = (400, 500),
    )

    api.set_window(window)

    def on_loaded():
        import json
        ports = api.scan_ports()
        window.evaluate_js(f'window.pyOnPortsScanned({json.dumps(ports)})')

        # 保存済みユーザースケールを復元
        user_scales = api.load_user_scales()
        if user_scales:
            window.evaluate_js(f'window.pyRestoreUserScales({json.dumps(user_scales)})')

        wingdrum_ports = [p for p in ports if p['wingdrum']]
        if wingdrum_ports:
            auto_port = wingdrum_ports[0]['port']
            api._log(f'Auto-connecting to {auto_port} ...')
            result = api.connect(auto_port)
            if result['ok']:
                window.evaluate_js(f"window.pyOnConnected('{auto_port}')")
                time.sleep(0.5)
                state = api.get_initial_state()
                window.evaluate_js(f'window.pyOnInitialState({json.dumps(state)})')
            else:
                window.evaluate_js("window.pyOnDisconnected()")
        else:
            # WingDrum未検出 → 明示的にDisconnected状態にする
            api._log('No WingDrum found. Select COM port manually.', 'error')
            window.evaluate_js("window.pyOnDisconnected()")

    window.events.loaded += on_loaded
    webview.start(debug=False)


if __name__ == '__main__':
    main()
