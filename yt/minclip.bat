@echo off
setlocal

:: Check the number of arguments
if "%~2"=="" (
    echo Usage: %0 input_file start_time
    echo Example: %0 video.mp4 00:00:05
    exit /b 1
)

:: Parameters
set "INPUT_FILE=%~1"
set "START_TIME=%~2"
set "LENGTH=00:01:00"
set "FPS=30"
set "CRF=20"
set "CODEC=libx264"
set "OUTPUT_FILE=%~n1_output%~x1.mp4"

:: Command
:: sample ffmpeg -ss 00:00:06 -t 00:01:00 -r 30 -vf "fps=30" -i .\bd.mp4 -c:v libx264 -crf 20 bd1.mp4
ffmpeg -ss %START_TIME% -t %LENGTH% -r %FPS%  -i "%INPUT_FILE%" -c:v %CODEC% -crf %CRF% "%OUTPUT_FILE%" -vf "fps=%FPS%"

echo Done processing %OUTPUT_FILE%
endlocal