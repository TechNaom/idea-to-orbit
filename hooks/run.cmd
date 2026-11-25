: ; exec bash "$(dirname "$0")/$1" #
@echo off
rem Idea to Orbit hook launcher.
rem This file is both a POSIX shell script and a Windows batch file. A shell runs line 1
rem and hands over to bash. cmd.exe reads line 1 as a label, skips it, and runs the lines
rem below, which find Git Bash and run the named hook with it. If no bash is found the
rem hook does nothing, so a session is never blocked.
setlocal
set "IO_HOOK=%~dp0%~1"
set "IO_BASH=%ProgramFiles%\Git\bin\bash.exe"
if exist "%IO_BASH%" goto run
set "IO_BASH=%LOCALAPPDATA%\Programs\Git\bin\bash.exe"
if exist "%IO_BASH%" goto run
set "IO_BASH="
for %%B in (bash.exe) do set "IO_BASH=%%~$PATH:B"
if not defined IO_BASH exit /b 0
rem The bash.exe in System32 is WSL, which cannot read this Windows path.
if /i "%IO_BASH%"=="%SystemRoot%\System32\bash.exe" exit /b 0
:run
"%IO_BASH%" "%IO_HOOK%"
exit /b %ERRORLEVEL%
