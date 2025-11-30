Simple script to control relay based antenna switch 

Create file
```
sudo nano /etc/systemd/system/antennaSwitchControl.service
```

Edit and paste
```
[Unit]
Description=Antenna Switch Control Service
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/home/your_user/Project/antennaSwitchControl
ExecStart=/usr/bin/python3 /home/your_user/Project/antennaSwitchControl/antennaSwitchControl.py
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

Run
```
sudo systemctl daemon-reload
sudo systemctl enable antennaSwitchControl.service
sudo systemctl start antennaSwitchControl.service
```

done
