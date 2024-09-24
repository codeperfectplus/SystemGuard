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



# @app.route('/api/v2/influxdb/graphs_data', methods=['GET'])
# @login_required
# def graph_data_api_v2():
#     try:
#         current_time = datetime.now()
#         # Get the time filter from query parameters
#         time_filter = request.args.get('filter', default='1 day')

#         # Determine the start time based on the filter
#         time_deltas = {
#             '5 minutes': '-5m',
#             '15 minutes': '-15m',
#             '30 minutes': '-30m',
#             '1 hour': '-1h',
#             '3 hours': '-3h',
#             '6 hours': '-6h',
#             '12 hours': '-12h',
#             '1 day': '-1d',
#             '2 days': '-2d',
#             '3 days': '-3d',
#             '1 week': '-1w',
#             '1 month': '-30d',
#             '3 months': '-90d',
#         }

#         # Get the start time for the query
#         time_range = time_deltas.get(time_filter, '-1d')

#         # Build the InfluxDB query
#         flux_query = f"""
#         from(bucket: "{bucket}")
#         |> range(start: {time_range})
#         |> filter(fn: (r) => r._measurement == "system_info")
#         |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
#         """

#         # Execute the query
#         tables = query_api.query(flux_query)

#         # Initialize lists for the data
#         time_data = []
#         cpu_data = []
#         memory_data = []
#         battery_data = []
#         network_sent_data = []
#         network_received_data = []
#         dashboard_memory_usage = []
#         cpu_frequency = []
#         current_temp = []

#         # Parse the results
#         for table in tables:
#             for record in table.records:
#                 time_data.append(record.values.get("_time", None))
#                 # Extract each field by key (handle missing fields gracefully)
#                 cpu_data.append(record.values.get("cpu_percent", None))
#                 memory_data.append(record.values.get("memory_percent", None))
#                 battery_data.append(record.values.get("battery_percent", None))
#                 network_sent_data.append(record.values.get("network_sent", None))
#                 network_received_data.append(record.values.get("network_received", None))
#                 dashboard_memory_usage.append(record.values.get("dashboard_memory_usage", None))
#                 cpu_frequency.append(record.values.get("cpu_frequency", None))
#                 current_temp.append(record.values.get("current_temp", None))

#         # Return the data as JSON
#         response = jsonify({
#             "time": time_data,
#             "cpu": cpu_data,
#             "memory": memory_data,
#             "battery": battery_data,
#             "network_sent": network_sent_data,
#             "network_received": network_received_data,
#             "dashboard_memory_usage": dashboard_memory_usage,
#             "cpu_frequency": cpu_frequency,
#             "current_temp": current_temp,
#             "current_time": current_time
#         })

#         # Clean up large data structures
#         del tables
#         del time_data
#         del cpu_data
#         del memory_data
#         del battery_data
#         del network_sent_data
#         del network_received_data
#         del dashboard_memory_usage
#         del cpu_frequency
#         del current_temp

#         gc.collect()

#         return response, 200

#     except Exception as e:
#         # Handle and log the error for debugging purposes
#         return jsonify({'error': 'An error occurred while fetching the graph data', 'details': str(e)}), 500
