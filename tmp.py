import datetime
import os
import psutil
import GPUtil
from pprint import pprint

# cpu temp

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_info = [{'id': gpu.id, 'name': gpu.name, 'load': round(gpu.load * 100, 2),
                 'memoryTotal': gpu.memoryTotal, 'memoryUsed': gpu.memoryUsed,
                 'temperature': gpu.temperature} for gpu in gpus]
    return gpu_info

def get_load_average():
    load_avg = os.getloadavg()
    return load_avg

def get_top_processes(number=5):
    processes = [(p.info['name'], p.info['cpu_percent'], round(p.info['memory_percent'],2)) for p in sorted(psutil.process_iter(['name', 'cpu_percent', 'memory_percent']), key=lambda p: p.info['memory_percent'], reverse=True)[:number]]
    return processes

gpu_info = get_gpu_info()
load_avg = get_load_average()
top_processes = get_top_processes()

