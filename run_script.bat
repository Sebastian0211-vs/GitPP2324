@echo off

python RaspQuickLaunch.py %*

python WatchDogeSupercharged.py %*

start "" http://172.16.0.2:10000/app_dev_679be46fa230435f99b5f8f28716e48f#/chassis

pause