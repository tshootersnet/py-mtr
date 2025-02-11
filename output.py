# output.py
import logging
from datetime import datetime
import socket
import statistics
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor

def format_results(results, destination, protocol, port, dns_lookup, source=None):
    local_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    utc_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    source_ip = source if source else socket.gethostbyname(socket.gethostname())

    try:
        destination_ip = socket.gethostbyname(destination)
    except socket.gaierror:
        destination_ip = destination

    destination_fqdn = destination
    if dns_lookup:
        try:
            destination_fqdn = socket.gethostbyaddr(destination_ip)[0]
        except socket.herror:
            pass

    header = f"""
Local Time: {local_time}
UTC Time: {utc_time}
Source: {source_ip}
Destination: {destination_fqdn} {destination_ip} {protocol if protocol else ''} {port if port else ''}
"""

    table_data = []

    current_ttl = 1
    times = []
    total_probes = 0
    successful_probes = 0
    last_ip = None

    for ttl, ip, elapsed_time in results:
        if ttl != current_ttl:
            if times:
                min_time = min(times)
                avg_time = statistics.mean(times)
                max_time = max(times)
                probes = len(times)
                loss = ((total_probes - successful_probes) / total_probes) * 100 if total_probes > 0 else 100
                table_data.append([current_ttl, last_ip, f"{loss:.2f}%", f"{min_time:.2f}/{avg_time:.2f}/{max_time:.2f}", probes])
            else:
                loss = 100
                table_data.append([current_ttl, "*", f"{loss:.2f}%", "*", total_probes])
            current_ttl = ttl
            times = []
            total_probes = 0
            successful_probes = 0

        if isinstance(elapsed_time, float):
            times.append(elapsed_time)
            last_ip = ip
            successful_probes += 1

        total_probes += 1

    if times:
        min_time = min(times)
        avg_time = statistics.mean(times)
        max_time = max(times)
        probes = len(times)
        loss = ((total_probes - successful_probes) / total_probes) * 100 if total_probes > 0 else 100
        table_data.append([current_ttl, last_ip, f"{loss:.2f}%", f"{min_time:.2f}/{avg_time:.2f}/{max_time:.2f}", probes])
    else:
        loss = 100
        table_data.append([current_ttl, "*", f"{loss:.2f}%", "*", total_probes])

    table = tabulate(table_data, headers=["TTL/Hop", "IP", "Loss", "Min/AVG/Max", "Probes"], tablefmt="pretty")

    formatted_results = header + table
    return formatted_results

def print_results(results):
    for result in results:
        print(result)

def save_results_to_file(results, filename):
    with open(filename, 'w') as f:
        f.write(results)
    logging.info(f"Results saved to {filename}")
