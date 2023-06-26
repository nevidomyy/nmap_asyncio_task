"""This a main file"""
import asyncio
import argparse

from functions import scan_all_ips


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="nmap scanner")
    parser.add_argument('-ip_filename', dest='ip_filename',
                        metavar='ip_filename', required=True,
                        help='IPs file path to scan (.txt)')
    parser.add_argument('-port_filename', dest='port_filename',
                        metavar='port_filename', required=True,
                        help='Ports file path to scan (.txt)')
    args = parser.parse_args()
    asyncio.run(scan_all_ips(args.ip_filename, args.port_filename))
