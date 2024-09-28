import threading
import time
import multiprocessing

# Function to consume CPU
def cpu_stress(duration):
    # Get the start time
    end_time = time.time() + duration
    while time.time() < end_time:
        # Simulate some CPU-heavy operation
        x = 0
        for _ in range(1000000):
            x += 1

def start_cpu_stress(duration, num_threads=None):
    if num_threads is None:
        # Default to the number of CPU cores if num_threads is not provided
        num_threads = multiprocessing.cpu_count()

    print(f"Starting CPU stress test with {num_threads} threads for {duration} seconds...")

    # Create and start threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=cpu_stress, args=(duration,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("CPU stress test completed.")

if __name__ == "__main__":
    # Set duration and number of threads (CPU cores) for the stress test
    duration = 30  # Duration in seconds
    num_threads = multiprocessing.cpu_count()  # Number of threads equal to CPU cores

    # Start the CPU stress test
    start_cpu_stress(duration, num_threads)
