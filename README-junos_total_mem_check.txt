# junos_total_mem_check


Purpose:
The purpose of this tool is to collect and compare summary memory utilization statistics.
This tool should be run as part a larger script where a device trigger or entire test case is inserted between the pre and post-trigger checks.
This tool can also be run without triggers to determine if memory is being consumed while the device is in steady state without invoking any trigger(s).


The following memory data points are collected and compared:
1. Total memory (KBytes and %)
2. Reserved memory (KBytes and %)
3. Wired memory (KBytes and %)
4. Active memory (KBytes and %)
5. Inactive memory (KBytes and %)
6. Cache memory (KBytes and %)
7. Free memory (KBytes and %)


Requirements:
The Paramiko SSH library is required for connectivity to the target device.
Juniper devices running EVO release have not been tested with this tool.


Usage:
you@your_computer# python3 junos_total_mem_check.py <ip-address> <username> <password> <interval-count>


Example Run:
me@my_computer# python3 junos_total_mem_check.py 10.0.0.21 user123 passwd123
Sending command: show system memory | match memory: | no-more

Sending command: show system memory | match memory: | no-more

Wired Memory utilization has consumed and not returned 256 KB during test.
Active Memory utilization has consumed and not returned 2268 KB during test.
Inactive Memory utilization has consumed and not returned 620 KB during test.
