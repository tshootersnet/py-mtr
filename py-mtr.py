#py-mtr.py

import argparse
import logging
import socket
from packet_creation import create_icmp_packet, create_udp_packet, create_tcp_packet, create_esp_packet
from mtr_logic import perform_trace
from output import format_results

def get_default_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def parse_arguments():
    parser = argparse.ArgumentParser(description='MTR-like tool for Python by tshootersnet')
    parser.add_argument('destination', help='Target destination (IP address or hostname)')
    protocol_group = parser.add_mutually_exclusive_group()
    protocol_group.add_argument('-p', '--protocol', type=str, default='ICMP', help='Protocol to use for probes (ICMP, UDP, TCP, ESP)')
    protocol_group.add_argument('--udp', action='store_const', const='UDP', dest='protocol', help='Use UDP protocol for probes')
    protocol_group.add_argument('--tcp', action='store_const', const='TCP', dest='protocol', help='Use TCP protocol for probes')
    protocol_group.add_argument('--icmp', action='store_const', const='ICMP', dest='protocol', help='Use ICMP protocol for probes')
    protocol_group.add_argument('--esp', action='store_const', const='ESP', dest='protocol', help='Use ESP protocol for probes')
    parser.add_argument('-d', '--dns', action='store_true', help='Perform DNS lookup')
    parser.add_argument('-o', '--output', help='Output file for results')
    parser.add_argument('--port', type=int, help='Port to use for UDP/TCP probes')
    parser.add_argument('--source', help='Source IP address', default=get_default_ip())
    parser.add_argument('-c', '--probes', type=int, help='Number of probes per hop', default=3)
    parser.add_argument('--max_hops', type=int, help='Maximum number of hops', default=10)
    args = parser.parse_args()

    if (args.protocol == 'UDP' or args.protocol == 'TCP') and args.port is None:
        parser.error(f"Protocol {args.protocol} requires --port to be specified")

    return args

def setup_logging():
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def display_executing_message():
    print("Executing, give me a moment...")

def main():
    args = parse_arguments()
    setup_logging()

    display_executing_message()

    protocol = args.protocol.upper()
    valid_protocols = ['ICMP', 'UDP', 'TCP', 'ESP']
    if protocol not in valid_protocols:
        logging.error(f"Invalid protocol '{protocol}'. Choose from {valid_protocols}.")
        return

    logging.info(f'Starting trace to {args.destination} using {protocol} protocol from source IP {args.source}')

    # Perform the trace
    results = perform_trace(args.destination, protocol, args.port, args.dns, args.probes, args.max_hops, args.source)

    # Format and print results
    formatted_results = format_results(results, args.destination, protocol, args.port, args.dns, args.source)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(formatted_results)
    else:
        print(formatted_results)

if __name__ == '__main__':
    main()
