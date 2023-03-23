# Setup
1. Install Docker.
2. `docker build -t sample_dash .`
3. `docker run --rm -v ABSOLUTE_PATH_TO_LOCAL_OUTPUT_FOLDER/data:/usr/src/app/logs -p 8050:8050 sample_dash`

# Execute
1. Click `Run Job!` will create a task (sleep 2), pass it to the worker.
2. A pop up will appear once the task is finish.
3. `Run longer Job2!` will create longer task (update figure), pass it to the worker.
4. It will generate a new plot after it finishes (no popup message)