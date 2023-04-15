import argparse, datetime, os, paramiko, re, sys, time
from pprint import pprint
from lib_ssh_connectivity import Device
from lib_junos_total_memory_check import get_system_total_memory
from lib_junos_total_memory_check import get_total_mem_use
from lib_junos_total_memory_check import get_diffs_mem_use


'''The following code can be used to execute this script file on 1 device under test.'''
cli_args = sys.argv[1:]
dut_ip = cli_args[0]
dut_user = cli_args[1]
dut_pass = cli_args[2]


'''DUT Login parameters'''
host_ip = dut_ip
user = dut_user
passwd = dut_pass
timeout = 30


def main():
    dut_host = Device(host_ip, user, passwd)

    # PRE-TRIGGER: Get memory values
    try:
        pre_inputs = get_system_total_memory(dut_host)
    except:
        print('An error has occurred')

    # PRE-TRIGGER: Call function to parse inputs and return list of 3 dictionaries (proc_name, pid, and res_mem_usage}
    pre_outputs_dict = get_total_mem_use(pre_inputs)

    #########################################
    ###### INSERT TRIGGER ACTIONS HERE#######
    #########################################
    time.sleep(5)
    #########################################
    #########################################
    #########################################

    # POST-TRIGGER: Get memory values
    try:
        post_inputs = get_system_total_memory(dut_host)
        #print(post_inputs)
    except:
        print('An error has occurred')

    # POST-TRIGGER: Call function to parse inputs and return list of 3 dictionaries (proc_name, pid, and res_mem_usage}
    try:
        post_outputs_dict = get_total_mem_use(post_inputs)
    except:
        print('An error has occurred')

    # STEADY STATE: Compare pre and post-trigger memory utilization values
    try:
        diffs = get_diffs_mem_use(pre_outputs_dict, post_outputs_dict)
    except:
        print('An error has occurred')



if __name__ == '__main__':
    main()
