[Setup]
AppName=Barangay Request System
AppVersion=1.0
DefaultDirName={pf}\BarangayRequestApp
DefaultGroupName=Barangay Request App
UninstallDisplayIcon={app}\BarangayRequestApp.exe
OutputBaseFilename=BarangayRequestAppInstaller
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes

[Files]
Source: "dist\BarangayRequestApp.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Barangay Request App"; Filename: "{app}\BarangayRequestApp.exe"
Name: "{commondesktop}\Barangay Request App"; Filename: "{app}\BarangayRequestApp.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"
