# WingDrum Controller

A PC companion app for the [PhonicBloom WingDrum](https://www.phonicbloom.com) — a handpan-style electronic instrument.

Control scales, tuning, micro-tuning, and presets from your computer over USB, with a visual drum diagram that mirrors the instrument's layout.

![WingDrum Controller](wd_wh.png)

---

## Features

### Connection
- Auto-detects WingDrum on startup (FTDI VID matching)
- Manual COM port selection from dropdown
- Connection status indicator (live dot + label)
- Dry-run mode when disconnected — all controls remain usable for preview

### Patch Selection
- Switch between all built-in timbres instantly:
  - Metal 1–11
  - Wood 1–5
  - Polyphonic Reverb
- Patch changes are sent immediately on click (no Apply needed)

### Scale Selection
- Full built-in scale library, organized by group:
  - **Minor**: Minor, Minor Harmonic
  - **Major**: Major, Major Pentatonic, Major Flat
  - **Modes**: Lydian, Phrygian, Ionian
  - **World**: Kurd Minor, Celtic Minor, Akebono Pentatonic, Annaziska, Pygmy, Deep Sea, Cloud, Celtic 2, Daze, Hijaz, Kurd 2, Voice, Shade
  - **World (Microtonal)**: Rast, Bayati, Saba, Hicaz, Bhairav, Todi, Darbari Kanada, Slendro, Pelog, Bali Pelog
  - **User**: your saved custom scales
- Microtonal world scales include per-pad cent offsets (auto-applied on selection)
- **Transpose**: shift the entire scale ±6 semitones
- **Rotation**: rotate pad assignments 0–7 steps clockwise
- **Flip L/R**: mirror pad assignments left-to-right

### Preset Slots
- 8 preset slot buttons displayed on the drum diagram outer ring
- Click a slot to select it as the write target
- When connected, clicking fetches the current slot data from the device
- Factory reset per patch (with confirmation dialog)

### Drum Diagram
- Visual SVG diagram matching the WingDrum's physical layout
- Note names displayed on each pad in real time
- **Drag & drop pad reordering**: grab any note label and drop it onto another pad to reorder
- Click any pad label to open the micro-tuning popup

### Per-Pad Micro-Tuning
- Click any pad label to open a popup
- Adjust pitch offset ±50 cents per pad
- Cent values shown visually on the diagram (background circle expands when offset is active)
- Micro-tuning is included when saving user scales

### Global Tuning
- Reference pitch slider: 400–480 Hz
- Fine tune slider: ±0.99 Hz, with a one-click reset-to-zero button
- Octave shift: ±3 octaves

### User Scale Registration
- Register the current pad layout (including micro-tuning) as a named custom scale
- Saved scales appear in the User group of the scale dropdown
- Delete individual user scales with the × button
- **User scales persist across sessions** (saved to `%APPDATA%\WingDrumController\` on Windows, `~/Library/Application Support/WingDrumController/` on macOS)

### Apply Button
- Sends all pending changes to the device in one operation:
  - `SET_SCALE_NOTES` for scale changes
  - `SET_TUNING` for tuning changes
  - `SET_PAD_TUNING` for per-pad micro-tuning
- Button turns red when there are unsent changes, green when in sync

### UI
- Dark / light theme toggle
- Responsive layout — resizes with the window, no scrollbar
- Log area showing all serial communication in real time

---

## Requirements

### Hardware
- PhonicBloom WingDrum (any unit)
- USB cable (USB-A to the WingDrum's port)

### Firmware
The app requires the **experimental serial control firmware v1.01**, which adds USB serial command support. This is not the factory firmware — it was developed in collaboration with Mario at PhonicBloom.

**Download:**
http://phonicbloom.com/updates/wingdrum/wingdrum_fw-1.01-experimental.bin

**Before flashing — back up your original firmware:**
```bash
python -m esptool --port COM4 --baud 115200 read_flash 0x30000 0x60000 wingdrum_backup_original.bin
```

**Flash the experimental firmware:**
```bash
# Enter boot mode: hold Power + Metal buttons, then connect USB
# Release Metal once esptool connects; keep Power held until complete
python -m esptool --port COM4 --baud 115200 write_flash 0x30000 wingdrum_fw-1.01-experimental.bin
```

> Replace `COM4` with your actual port. On macOS/Linux use `/dev/tty.usbserial-XXXX` or similar.

> **Note:** The firmware outputs debug data to serial on startup and on button presses. This is normal — the app ignores it automatically.

### FTDI Driver (Windows)
On some Windows systems, the FTDI USB serial driver may need to be installed manually:
https://ftdichip.com/drivers/vcp-drivers/

---

## Installation

### Windows
1. Download `WingDrumController_Setup.exe` from [Releases](../../releases)
2. Double-click to install
3. Launch from the desktop shortcut or Start Menu

### macOS
1. Download `WingDrumController.dmg` from [Releases](../../releases)
2. Open the DMG and drag `WingDrumController.app` to Applications
3. On first launch, right-click → Open to bypass Gatekeeper

---

## Serial Command Reference

For developers. All commands verified on firmware v1.01-experimental.

| Command | Response | Notes |
|---|---|---|
| `GET_TUNING` | `OK:440.00` | Current reference pitch in Hz |
| `SET_TUNING:<hz>` | `OK` | e.g. `SET_TUNING:432.50` |
| `GET_PATCH` | `OK:metal,0` | Current timbre and patch index |
| `SET_PATCH:metal,<0-10>` | `OK` | Wait 700ms after sending |
| `SET_PATCH:wood,<0-4>` | `OK` | Wait 700ms after sending |
| `SET_PATCH:reverb` | `OK` | Polyphonic Reverb mode |
| `GET_SCALE` | `OK:60,62,...` | 9 MIDI note numbers (active slot) |
| `SET_SCALE:<name>` | `OK` | Writes to slot 7 |
| `SET_SCALE_DEF:<slot>,<name>` | `OK` | Register named scale to slot 0–7 |
| `SET_SCALE_NOTES:<slot>,<n0>,...,<n8>` | `OK` | Write 9 MIDI notes to slot |
| `GET_PAD_TUNING:<pad>` | `OK:15.00` | Per-pad offset in cents |
| `SET_PAD_TUNING:<pad>,<cents>` | `OK` | Micro-tuning ±50 cents |

**Important:** Always set `dtr=False` and `rts=False` before opening the serial port, or the WingDrum will reset on connect.

```python
ser = serial.Serial()
ser.port = 'COM4'
ser.baudrate = 115200
ser.dtr = False
ser.rts = False
ser.open()
```

---

## Building from Source

```bash
pip install pywebview pyserial
python main.py
```

To build a standalone installer, see [BUILD_README.md](BUILD_README.md).

---

## License

GPL v3. See [LICENSE](LICENSE).

This project is developed independently by a WingDrum owner, with the kind support of Mario at PhonicBloom.
