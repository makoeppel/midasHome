# Setup MIDAS

# install
```bash
sudo apt-get install bluez bluez-hcidump tmux git cmake libcurl4-openssl-dev libcap-dev
pip install picamzero ruuvitag-sensor --break-system-packages
```

# find sensors
```python
"""
Find RuuviTags
"""

import os

os.environ["RUUVI_BLE_ADAPTER"] = "bluez"

import ruuvitag_sensor.log
from ruuvitag_sensor.ruuvi import RuuviTagSensor

ruuvitag_sensor.log.enable_console()

# This will print sensor's mac and state when new sensor is found
if __name__ == "__main__":
    RuuviTagSensor.find_ruuvitags()
```

# midas
```bash
git clone https://@bitbucket.org/tmidas/midas.git
cd midas
git submodule update --init --recursive
mkdir build
cd build
cmake ..
make -j4
make install
cd ../..
vim .bashrc
```

Add the following to the end:

```bash
export MIDASSYS=$HOME/midas
export MIDAS_EXPTAB=$HOME/midasHome/exptab
export MIDAS_EXPT_NAME=midasHome
export PATH=$PATH:$MIDASSYS/bin
export PYTHONPATH=$PYTHONPATH:$MIDASSYS/python
export RUUVI_BLE_ADAPTER="bluez"
```

```bash
source .bashrc
```

Setup extab file
```bash
`echo "midasHome /home/pi/midasHome eg" > /home/pi/midasHome/exptab`
```

Setup webserver
```bash
mhttpd
# kill it again
odbedit -c "set 'WebServer/Enable insecure port' 'y'"
odbedit -c "set 'WebServer/insecure port passwords' 'n'"
odbedit -c "set 'WebServer/insecure port host list' 'n'"
```

Setup systemd
```bash
sudo nano /etc/systemd/system/mhttpd.service
```

```bash
[Unit]
Description=MIDAS Web Server (mhttpd)
After=network.target

[Service]
Type=forking
User=pi
Group=pi
WorkingDirectory=/home/pi
ExecStart=/home/pi/midasHome/start-mhttpd.sh
PIDFile=/tmp/mhttpd.pid
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable mhttpd
sudo systemctl start mhttpd
sudo systemctl status mhttpd
```

Find tags
```bash
python find_tag.py
```
Add MAC to `ruuvi_fe.py`
