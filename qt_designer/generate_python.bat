pyuic5 imcc.ui -o ..\src\ui\imcc.py
pyuic5 variables.ui -o ..\src\ui\variables.py
pyuic5 graphics.ui -o ..\src\ui\graphics.py
pyuic5 console.ui -o ..\src\ui\console.py
pyuic5 stm32flash.ui -o ..\src\ui\stm32flash.py
pyuic5 digital_servos.ui -o ..\src\ui\digital_servos.py

pyrcc5 imcc.qrc -o ..\src\ui\imcc_rc.py

pause
