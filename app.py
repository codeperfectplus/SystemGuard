from src.config import app
from src import routes
from src.background_task import start_background_tasks

# Start the background tasks
start_background_tasks()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
