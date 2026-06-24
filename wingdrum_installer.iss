; ============================================================
; WingDrum Controller — Inno Setup スクリプト (Windows)
; Inno Setup: https://jrsoftware.org/isdl.php
; ============================================================

[Setup]
AppName=WingDrum Controller
AppVersion=1.0.0
AppPublisher=PhonicBloom / wingdrum-controller contributors
AppPublisherURL=https://www.phonicbloom.com
DefaultDirName={autopf}\WingDrumController
DefaultGroupName=WingDrum Controller
OutputDir=installer
OutputBaseFilename=WingDrumController_Setup
SetupIconFile=wingdrum.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
; PrivilegesRequired=lowest  ; 管理者権限なしでインストール可能にする場合はコメントを外す

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"

[Tasks]
Name: "desktopicon"; Description: "デスクトップにショートカットを作成"; GroupDescription: "追加タスク:"

[Files]
; PyInstallerがdist/WingDrumController/に出力したファイルを全て同梱
Source: "dist\WingDrumController\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\WingDrum Controller"; Filename: "{app}\WingDrumController.exe"; IconFilename: "{app}\WingDrumController.exe"
Name: "{group}\アンインストール"; Filename: "{uninstallexe}"
Name: "{commondesktop}\WingDrum Controller"; Filename: "{app}\WingDrumController.exe"; IconFilename: "{app}\WingDrumController.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\WingDrumController.exe"; Description: "WingDrum Controller を起動する"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
