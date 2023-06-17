import asyncio
import json
import re
import subprocess


async def nmap_ip_scan(ip_address: str) -> str:
    process = await asyncio.create_subprocess_shell(f'nmap {ip_address}', stdout=subprocess.PIPE)
    output, _ = await process.communicate()
    return output.decode()


async def scan_all_ips(ip_file_path: str, port_file_path: str) -> dict:
    with open(ip_file_path, 'r') as f:
        ip_addresses = f.read().splitlines()
    with open(port_file_path, 'r') as f:
        ports = f.read().splitlines()

    results = await asyncio.gather(*[nmap_ip_scan(ip_address) for ip_address in ip_addresses])

    parsed_results = {}
    for i, ip_address in enumerate(ip_addresses):
        parsed_results[ip_address] = {'Opened_ports': [], 'Closed_ports': []}
        for line in results[i].splitlines():
            if re.match(r'^\d+/(tcp|udp)', line):
                line_parts = line.split()
                if line_parts[1] == 'open':
                    parsed_results[ip_address]['Opened_ports'].append(line_parts[0].split('/')[0])
        parsed_results[ip_address]['Closed_ports'] = [port for port in ports
                                                      if port not in parsed_results[ip_address]['Opened_ports']]
    return parsed_results


async def main():
    ip_file_path = 'ip.txt'  # or: input('IP File name:')
    port_file_path = 'ports.txt'  # or: input('Ports File name:')
    print(json.dumps(await scan_all_ips(ip_file_path, port_file_path), indent=4))


if __name__ == "__main__":
    asyncio.run(main())
