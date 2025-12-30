# Setup MIDAS

# install
sudo apt-get install bluez bluez-hcidump tmux git cmake libcurl4-openssl-dev, libcap-dev
pip install picamzero --break-system-packages

`bashrc`

```bash
export MIDASSYS=$HOME/midas
export MIDAS_EXPTAB=$HOME/midasHome/exptab
export MIDAS_EXPT_NAME=midasHome
export PATH=$PATH:$MIDASSYS/bin
export PYTHONPATH=$PYTHONPATH:$MIDASSYS/python
export RUUVI_BLE_ADAPTER="bluez"
```

`exptab`
`echo "midasHome /home/pi/midasHome eg" > /home/pi/midasHome/exptab`

`odbedit -c "set 'WebServer/Enable insecure port' 'y'"`
`odbedit -c "set 'WebServer/insecure port passwords' 'n'"`
`odbedit -c "set 'WebServer/insecure port host list' 'n'"`
