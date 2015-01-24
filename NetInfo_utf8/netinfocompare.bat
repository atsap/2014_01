cd /d %~dp
NetworkInterfacesView.exe
ping 127.0.0.1 > nul
fc netinfo.def netinfo.ctrl
if not errorlevel 1 (goto :eof) else (goto retry)

:retry
ping 127.0.0.1 -n 30 > nul
NetworkInterfacesView.exe
ping 127.0.0.1 > nul
fc netinfo.def netinfo.ctrl
if not errorlevel 1 (echo pass) else (echo netinfo compare fail. && pause)