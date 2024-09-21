# from influxdb_client import InfluxDBClient, Point, WritePrecision
# from influxdb_client.client.write_api import SYNCHRONOUS
# import os
# from src.logger import logger


# # influx db configuration
# org = "systemguard"
# url = "http://localhost:8086"
# bucket="system_metrics"
# INFLUXDB_TOKEN=os.getenv('INFLUXDB_TOKEN')
# print("INFLUXDB_TOKEN: ", INFLUXDB_TOKEN)

# try:
#     influx_client = InfluxDBClient(url=url, token=INFLUXDB_TOKEN, org=org)
#     bucket = "system_metrics"
#     write_api = influx_client.write_api(write_options=SYNCHRONOUS)
#     query_api = influx_client.query_api()
#     logger.info("Connected to InfluxDB successfully")
# except Exception as e:
#     logger.error(f"Failed to connect to InfluxDB: {e}")
#     raiseclient = InfluxDBClient(url=url, token=INFLUXDB_TOKEN, org=org)
