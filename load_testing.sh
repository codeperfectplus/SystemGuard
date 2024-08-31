    #!/bin/bash

    # Script to start Locust server

    # Define the path to your Locust file
    LOCUST_FILE="src/scripts/locustfile.py"
    # Define the host URL for Locust
    HOST_URL="http://localhost:5050"

    # Check if Locust is installed
    if ! command -v locust &> /dev/null
    then
        echo "Locust is not installed. Please install it first."
        exit 1
    fi

    # Start Locust server
    echo "Starting Locust server..."
    locust -f "$LOCUST_FILE" --host="$HOST_URL"

    # Optionally, you can pass additional Locust flags here if needed
    # For example, to run Locust in headless mode:
    # locust -f "$LOCUST_FILE" --host="$HOST_URL" --headless -u 10 -r 1 --run-time 1m
