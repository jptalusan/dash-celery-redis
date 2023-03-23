# Setup
1. create virtual environment
2. activate venv
3. `celery -A celery_app.celery_app worker --loglevel=INFO`
* or `nohup celery -A celery_app.celery_app worker --loglevel=INFO > celery_logs.txt 2&1 &`
4. `docker run -p 6379:6379 redis`
5. `python celery_app.py`

# Execute
1. Click `Run Job!` will create a task (sleep 2), pass it to the worker.
2. A pop up will appear once the task is finish.
3. `Run longer Job2!` will create longer task (update figure), pass it to the worker.
4. It will generate a new plot after it finishes (no popup message)