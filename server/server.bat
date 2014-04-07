# Shellscript for runnning the server for windows users

setlocal
set PYTHONPATH=%cd%;%PYTHONPATH%
cd server

#change the python file arguments if you wish to change some configuration
python server.py
endlocal
