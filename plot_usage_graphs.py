import matplotlib.pyplot as plt
import csv
import json
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python script.py <benchmark_language>")
    sys.exit(1)

folder_name = sys.argv[1]

with open('test-report.json', 'r') as json_file:
    data = json.load(json_file)

latency_data = data['aggregate']['histograms']['http.response_time']

latency_percentiles = {
    'p50': latency_data['p50'],
    'p90': latency_data['p90'],
    'p95': latency_data['p95'],
    'p99': latency_data['p99'],
}

timestamps = []
cpu_usage = []
ram_usage = []

with open('output.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        timestamps.append(int(row[0])) 
        cpu_usage.append(float(row[1]))
        ram_usage.append(float(row[2]))


if not os.path.exists(folder_name+"_figures"):
    os.mkdir(folder_name+"_figures")


plt.figure(figsize=(10, 6))
plt.plot(timestamps, cpu_usage, label='CPU Usage')
plt.title('CPU Usage Over Time')
plt.xlabel('Time in seconds')
plt.ylabel('CPU Usage (%)')

plt.savefig(folder_name + '_figures/cpu_usage.png')
plt.close()

plt.plot(timestamps, ram_usage, label='RAM Usage')
plt.title('RAM Usage Over Time')
plt.xlabel('Time in seconds')
plt.ylabel('RAM Usage (%)')

plt.savefig(folder_name + '_figures/ram_usage.png')
plt.close()

percentiles = list(latency_percentiles.keys())
latency_values = [latency_percentiles[p] for p in percentiles]

plt.figure(figsize=(10, 6))
plt.bar(percentiles, latency_values, color='blue')
plt.xlabel('Latency Percentile')
plt.ylabel('Latency (ms)')
plt.title('Latency Metrics')
plt.ylim(0, max(latency_values) + 10) 
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.savefig(folder_name + '_figures/latency.png')
plt.close()
