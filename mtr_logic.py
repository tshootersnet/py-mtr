# mtr_logic.py
import logging
import random
from scapy.all import IP, ICMP, UDP, TCP, ESP, sr1, Raw

def perform_trace(destination, protocol, port=None, dns_lookup=False, num_probes=3, max-hops=30, source=None):
    timeout = 2
    ident = random.randint(0, 65535)  # Initialize the IP identification field

    results = []
    protocol = protocol.upper()  # Convert protocol to uppercase
    src_ip = None  # Initialize src_ip

    logging.info(f"Tracing route to {destination} with max {max-hops} hops using {protocol} protocol")

    for ttl in range(1, max-hops + 1):
        successful_probes = 0
        total_probes = 0
        for _ in range(num_probes):
            if protocol == "ICMP":
                pkt = IP(src=source, dst=destination, ttl=ttl, id=ident) / ICMP()
            elif protocol == "UDP":
                source_port = random.randint(1024, 65535)
                payload = b'Malformed payload'
                pkt = IP(src=source, dst=destination, ttl=ttl, id=ident) / UDP(sport=source_port, dport=port) / Raw(load=payload)
            elif protocol == "TCP":
                source_port = random.randint(1024, 65535)
                pkt = IP(src=source, dst=destination, ttl=ttl, id=ident) / TCP(sport=source_port, dport=port, flags="S")
            elif protocol == "ESP":
                pkt = IP(src=source, dst=destination, ttl=ttl, id=ident) / ESP()

            response = sr1(pkt, timeout=timeout, verbose=0)
            total_probes += 1

            if response:
                elapsed_time = (response.time - pkt.sent_time) * 1000
                src_ip = response.src
                results.append((ttl, src_ip, elapsed_time))
                logging.info(f"{ttl}\t{src_ip}\t{elapsed_time:.2f} ms")
                successful_probes += 1

                if src_ip == destination:
                    if total_probes >= num_probes:
                        return results
            else:
                logging.info(f"{ttl}\t*")
                results.append((ttl, '*', '*'))

            ident += 1  # Increment the identification field for each packet

        if src_ip == destination and total_probes >= num_probes:
            break

    return results
