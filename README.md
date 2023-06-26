# wts
1) clone repo onto the raspberry pi
2) set up the .env file
3) configure cron to pull repo and run script on reboot
  sudo crontab -e
  @reboot sleep 60 && git -C /path/to/repo/wts/ pull && python /path/to/repo/wts/run.py
  /etc/init.d/cron start
