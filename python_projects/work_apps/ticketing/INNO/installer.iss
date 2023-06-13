[Setup]
AppName=Ticketing
AppVersion=1.5
WizardStyle=modern
DefaultDirName={autopf}\ticketing
DefaultGroupName=Ticketing
UninstallDisplayIcon={app}\ticketing.exe
Compression=lzma2
SolidCompression=yes
OutputDir=userdocs:Inno Setup Examples Output
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "ticketing.exe"; DestDir: "{app}"
Source: "MyProg.chm"; DestDir: "{app}"
Source: "Readme.txt"; DestDir: "{app}"; Flags: isreadme
Source: "bg1.png"; DestDir: "{app}" 
Source: "tickets.pkl"; DestDir: "{app}" 

[Icons]
Name: "{group}\Ticketing"; Filename: "{app}\ticketing.exe"