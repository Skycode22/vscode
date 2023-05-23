# Import user32.dll and define SetForegroundWindow function
Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class User32 {
        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetForegroundWindow(IntPtr hWnd);
    }
"@

# Start programs
$proc1 = Start-Process "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Ticketing\Ticketing.lnk" -PassThru
$proc2 = Start-Process "C:\Program Files (x86)\Microsoft Office\root\Office16\ONENOTE.EXE" -PassThru
$proc3 = Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "https://calendar.google.com" -PassThru

# Wait for the applications to start
Start-Sleep -Seconds 5

# Arrange windows
[User32]::SetForegroundWindow($proc1.MainWindowHandle) # Activate the first window
Start-Sleep -Seconds 1
[User32]::SetForegroundWindow($proc2.MainWindowHandle) # Activate the second window
Start-Sleep -Seconds 1
[User32]::SetForegroundWindow($proc3.MainWindowHandle) # Activate the third window
