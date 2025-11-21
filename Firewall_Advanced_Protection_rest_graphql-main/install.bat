@echo off
echo Installing API Firewall Dependencies...
echo =====================================

pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo To start the firewall:
echo   python start.py
echo.
echo To test the firewall:
echo   python test_firewall.py
echo.
pause