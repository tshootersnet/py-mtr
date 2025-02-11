# packet_creation.py
import socket
import struct
import random

def create_icmp_packet(destination):
    checksum = 0
    identifier = random.randint(0, 65535)
    sequence = 1
    header = struct.pack('!BBHHH', 8, 0, checksum, identifier, sequence)
    data = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    checksum = calculate_checksum(header + data)
    header = struct.pack('!BBHHH', 8, 0, checksum, identifier, sequence)
    packet = header + data
    return packet

def create_udp_packet(destination):
    source_port = random.randint(1024, 65535)
    dest_port = 33434
    length = 8
    checksum = 0
    header = struct.pack('!HHHH', source_port, dest_port, length, checksum)
    return header

def create_tcp_packet(destination):
    source_port = random.randint(1024, 65535)
    dest_port = 80
    seq = random.randint(0, 4294967295)
    ack_seq = 0
    doff = 5
    flags = 2  # SYN flag
    window = socket.htons(5840)
    checksum = 0
    urg_ptr = 0
    offset_res = (doff << 4) + 0
    tcp_flags = flags
    header = struct.pack('!HHLLBBHHH', source_port, dest_port, seq, ack_seq, offset_res, tcp_flags, window, checksum, urg_ptr)
    return header

def create_esp_packet(destination):
    spi = random.randint(0, 4294967295)
    seq = random.randint(0, 4294967295)
    header = struct.pack('!LL', spi, seq)
    return header

def calculate_checksum(data):
    if len(data) % 2:
        data += b'\x00'
    checksum = sum(struct.unpack('!%dH' % (len(data) // 2), data))
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum += checksum >> 16
    return ~checksum & 0xffff
