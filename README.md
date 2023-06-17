# nmap_asyncio_task
Scanning is performed asynchronously, which reduces program execution time\
ip.txt - A file with a list of ip addresses to be scanned\
port.txt - A file with a list of ports

Print the result to the console in json format. The result should be:\
a) a list of "open" ports on each host (which nmap determined to be "open");\
b) a list of ports from the file (specified at the start of the program) that were closed.

# Run
- python3 main.py -ip_filename ip.txt -port_filename ports.txt
