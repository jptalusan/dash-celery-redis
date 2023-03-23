#!/bin/bash
nohup redis-server 2>&1 &
nohup celery -A celery_app.celery_app worker --loglevel=INFO > logs/celery_logs.txt 2>&1 &
python celery_app.py