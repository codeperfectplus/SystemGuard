import time
import argparse
import sys

def allocate_memory(mb_to_allocate, duration):
    """
    Allocates memory in megabytes and holds it for the specified duration.
    
    :param mb_to_allocate: Amount of memory to allocate in MB.
    :param duration: How long (in seconds) to hold the memory allocation.
    """
    try:
        # Allocate memory (list of bytes, 1MB = 1024 * 1024 bytes)
        allocated_memory = bytearray(mb_to_allocate * 1024 * 1024)
        print(f"Allocated {mb_to_allocate} MB of memory.")

        # Keep the memory allocated for the specified duration
        time.sleep(duration)
        print(f"Held memory for {duration} seconds.")
    except MemoryError:
        print(f"Memory allocation failed for {mb_to_allocate} MB.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        del allocated_memory
        print(f"Memory released after {duration} seconds.")

def stress_test(total_mb, step_mb, duration):
    """
    Perform a memory stress test by allocating increasing amounts of memory.
    
    :param total_mb: The total amount of memory to allocate.
    :param step_mb: The step size in MB for each allocation.
    :param duration: Duration to hold each memory allocation.
    """
    for current_mb in range(step_mb, total_mb + 1, step_mb):
        print(f"Attempting to allocate {current_mb} MB...")
        allocate_memory(current_mb, duration)
        print(f"Completed {current_mb} MB allocation.\n")

if __name__ == "__main__":
    # Argument parser for command-line execution
    parser = argparse.ArgumentParser(description="Memory Stress Test Tool")
    parser.add_argument("-t", "--total", type=int, default=8024, help="Total memory to allocate in MB (default: 1024 MB)")
    parser.add_argument("-s", "--step", type=int, default=4000, help="Step size in MB for each allocation (default: 256 MB)")
    parser.add_argument("-d", "--duration", type=int, default=30, help="Duration to hold the memory allocation in seconds (default: 5 seconds)")
    
    args = parser.parse_args()

    print(f"Starting memory stress test. Total: {args.total} MB, Step: {args.step} MB, Duration: {args.duration} seconds.")
    stress_test(args.total, args.step, args.duration)
