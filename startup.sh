# Startup script. Will install needed modules and run the server
# origin clone and hard reset
echo "Cloning latest master"
# add git shell later

# pip packages
echo "Installing needed modules via pip..."
pip3 install -r requirements.txt

# server start
echo "Starting server in DEBUG mode"
python3 auth-module.py
