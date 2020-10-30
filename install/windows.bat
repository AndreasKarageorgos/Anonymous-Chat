@ECHO OFF

IF EXIST C:\Users\%username%\AppData\Local\Programs\Python\Python3? (
powershell C:\Users\%username%\AppData\Local\Programs\Python\Python3?\python.exe -m pip install pysocks
powershell C:\Users\%username%\AppData\Local\Programs\Python\Python3?\python.exe -m pip install requests
powershell C:\Users\%username%\AppData\Local\Programs\Python\Python3?\python.exe -m pip install pycryptodome
echo.
echo.
echo Done !
echo Do not forget to download Tor "Windows Expert Bundle".
echo Press any key to exit.
pause >> nul
exit
)
echo Python3 is not installed to your system.
pause >> null

