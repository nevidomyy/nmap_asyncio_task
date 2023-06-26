"""This a main file"""
import asyncio
import json
import subprocess
import argparse
import re


async def nmap_ip_scan(ip_address: str) -> str:
    """
    :param ip_address: foe example '192.168.1.3'
    :return: information about this address in string format
    """
    process = await asyncio.create_subprocess_shell(f'nmap {ip_address}',
                                                    stdout=subprocess.PIPE)
    output, _ = await process.communicate()
    return output.decode()


async def scan_all_ips(ip_file_path: str, port_file_path: str):
    """
    :param ip_file_path: ip file path in txt format, for example:
    '/my/path/ip.txt
    :param port_file_path: port file path in txt format, for example:
     '/my/path/port.txt
    This function printed information about IP and ports in CLI
    """
    with open(ip_file_path, 'r', encoding='utf-8') as ip_file:
        ip_addresses = ip_file.read().splitlines()
    with open(port_file_path, 'r', encoding='utf-8') as port_file:
        ports = port_file.read().splitlines()

    results = await asyncio.gather(*[nmap_ip_scan(ip_address) for ip_address
                                     in ip_addresses])
    print(json.dumps(parse_results(ip_addresses, ports, results), indent=4))


def parse_results(ip_addresses: list[str], ports: list[str], results: list):
    """
    :param ip_addresses: list of IP addresses
    :param ports: list of ports
    :param results: scan results for IPs
    :return: results with opened and closed ports group by IP
    """
    parsed_results = {}
    for i, ip_address in enumerate(ip_addresses):
        parsed_results[ip_address] = {'Opened_ports': [], 'Closed_ports': []}
        for line in results[i].splitlines():
            if re.match(r'^\d+/(tcp|udp)', line):
                line_parts = line.split()
                if line_parts[1] == 'open':
                    parsed_results[ip_address]['Opened_ports'].append(
                        line_parts[0].split('/')[0])

        closed_ports = [port for port in ports if port not in
                        parsed_results[ip_address]['Opened_ports']]
        parsed_results[ip_address]['Closed_ports'] = closed_ports

    return parsed_results


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
