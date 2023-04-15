import argparse, datetime, os, paramiko, re, sys, time
from lib_ssh_connectivity import Device
from lib_ssh_connectivity import create_handle_quiet
from pprint import pprint



def get_system_total_memory(dut_host):
    '''Command sets for device configuration'''
    #command_set_1 = [f'show system memory | match "/" | except ":" | no-more']
    command_set_1 = [f'show system memory | match memory: | no-more']
    '''Create handle'''
    dut_host_session = create_handle_quiet(dut_host)
    dut_host_terminal = dut_host_session.invoke_shell()
    '''Start execution'''
    for command in command_set_1:
        print(f'Sending command: {command}\n')
        try:
            dut_host_terminal.send(f'{command}\n')
            time.sleep(3)
        except:
            print(f"An error occurred.")
            time.sleep(1)
        output = dut_host_terminal.recv(100000).decode('utf-8')
    output_recv = output.split('\r\n')
    dut_host_terminal.send('exit\n')
    return output



'''Parse output from total memory data retrieved'''
def get_total_mem_use(inputs):
    re_total_memory = re.findall(r'Total\s+memory:\s+\d+\s+Kbytes\s+\(\d+', inputs, re.MULTILINE)
    list_total_memory_kb = [item.split() for item in re_total_memory]
    list_total_memory_kb = list_total_memory_kb[0]
    total_memory_kb = int(list_total_memory_kb[2])
    total_memory_pct = int(list_total_memory_kb[4].replace('(', ''))
    re_wired_memory = re.findall(r'Wired\s+memory:\s+\d+\s+Kbytes\s+\(\s+\d+', inputs, re.MULTILINE)
    list_wired_memory_kb = [item.split() for item in re_wired_memory]
    list_wired_memory_kb = list_wired_memory_kb[0]
    wired_memory_kb = int(list_wired_memory_kb[2])
    wired_memory_pct = int(list_wired_memory_kb[5])
    re_reserved_memory = re.findall(r'Reserved\s+memory:\s+\d+\s+Kbytes\s+\(\s+\d+', inputs, re.MULTILINE)
    list_reserved_memory_kb = [item.split() for item in re_reserved_memory]
    list_reserved_memory_kb = list_reserved_memory_kb[0]
    reserved_memory_kb = int(list_reserved_memory_kb[2])
    reserved_memory_pct = int(list_reserved_memory_kb[5])
    re_active_memory = re.findall(r'Active\s+memory:\s+\d+\s+Kbytes\s+\(\s+\d+', inputs, re.MULTILINE)
    list_active_memory_kb = [item.split() for item in re_active_memory]
    list_active_memory_kb = list_active_memory_kb[0]
    active_memory_kb = int(list_active_memory_kb[2])
    active_memory_pct = int(list_active_memory_kb[5])
    re_inactive_memory = re.findall(r'Inactive\s+memory:\s+\d+\s+Kbytes\s+\(\s+\d+', inputs, re.MULTILINE)
    list_inactive_memory_kb = [item.split() for item in re_inactive_memory]
    list_inactive_memory_kb = list_inactive_memory_kb[0]
    inactive_memory_kb = int(list_inactive_memory_kb[2])
    inactive_memory_pct = int(list_inactive_memory_kb[5])
    re_cache_memory = re.findall(r'Cache\s+memory:\s+\d+\s+Kbytes\s+\(\s+\d+', inputs, re.MULTILINE)
    list_cache_memory_kb = [item.split() for item in re_cache_memory]
    list_cache_memory_kb = list_cache_memory_kb[0]
    cache_memory_kb = int(list_cache_memory_kb[2])
    cache_memory_pct = int(list_cache_memory_kb[5])
    re_free_memory = re.findall(r'Free\s+memory:\s+\d+\s+Kbytes\s+\(\s+\d+', inputs, re.MULTILINE)
    list_free_memory_kb = [item.split() for item in re_free_memory]
    list_free_memory_kb = list_free_memory_kb[0]
    free_memory_kb = int(list_free_memory_kb[2])
    free_memory_pct = int(list_free_memory_kb[5])
    memory_dict = {'total_memory_kb' : total_memory_kb,
                   'total_memory_pct' : total_memory_pct,
                   'reserved_memory_kb' : reserved_memory_kb,
                   'reserved_memory_pct' : reserved_memory_pct,
                   'wired_memory_kb' : wired_memory_kb,
                   'wired_memory_pct' : wired_memory_pct,
                   'active_memory_kb' : active_memory_kb,
                   'active_memory_pct' : active_memory_pct,
                   'inactive_memory_kb' : inactive_memory_kb,
                   'inactive_memory_pct' : inactive_memory_pct,
                   'cache_memory_kb' : cache_memory_kb,
                   'cache_memory_pct' : cache_memory_pct,
                   'free_memory_kb' : free_memory_kb,
                   'free_memory_pct' : free_memory_pct
                   }
    return memory_dict


'''
Pre and post memory usage diff
'''
def get_diffs_mem_use(pre_mem_dict, post_mem_dict):
    diff_total_memory_kb = post_mem_dict['total_memory_kb'] - pre_mem_dict['total_memory_kb']
    diff_total_memory_pct = post_mem_dict['total_memory_pct'] - pre_mem_dict['total_memory_pct']
    diff_reserved_memory_kb = post_mem_dict['reserved_memory_kb'] - pre_mem_dict['reserved_memory_kb']
    diff_reserved_memory_pct = post_mem_dict['reserved_memory_pct'] - pre_mem_dict['reserved_memory_pct']
    diff_wired_memory_kb = post_mem_dict['wired_memory_kb'] - pre_mem_dict['wired_memory_kb']
    diff_wired_memory_pct = post_mem_dict['wired_memory_pct'] - pre_mem_dict['wired_memory_pct']
    diff_active_memory_kb = post_mem_dict['active_memory_kb'] - pre_mem_dict['active_memory_kb']
    diff_active_memory_pct = post_mem_dict['active_memory_pct'] - pre_mem_dict['active_memory_pct']
    diff_inactive_memory_kb = post_mem_dict['inactive_memory_kb'] - pre_mem_dict['inactive_memory_kb']
    diff_inactive_memory_pct = post_mem_dict['inactive_memory_pct'] - pre_mem_dict['inactive_memory_pct']
    diff_cache_memory_kb = post_mem_dict['cache_memory_kb'] - pre_mem_dict['cache_memory_kb']
    diff_cache_memory_pct = post_mem_dict['cache_memory_pct'] - pre_mem_dict['cache_memory_pct']
    diff_free_memory_kb = post_mem_dict['free_memory_kb'] - pre_mem_dict['free_memory_kb']
    diff_free_memory_pct = post_mem_dict['free_memory_pct'] - pre_mem_dict['free_memory_pct']
    if diff_total_memory_kb > 0:
        print(f'Total Memory utilization has consumed and not returned {diff_total_memory_kb} KB during test.')
    if diff_reserved_memory_kb > 0:
        print(f'Reserved Memory utilization has consumed and not returned {diff_reserved_memory_kb} KB during test.')
    if diff_wired_memory_kb > 0:
        print(f'Wired Memory utilization has consumed and not returned {diff_wired_memory_kb} KB during test.')
    if diff_active_memory_kb > 0:
        print(f'Active Memory utilization has consumed and not returned {diff_active_memory_kb} KB during test.')
    if diff_inactive_memory_kb > 0:
        print(f'Inactive Memory utilization has consumed and not returned {diff_inactive_memory_kb} KB during test.')
    if diff_cache_memory_kb > 0:
        print(f'Total Cache utilization has consumed and not returned {diff_cache_memory_kb} KB during test.')
    if diff_free_memory_kb > 0:
        print(f'Free Memory utilization has consumed and not returned {diff_free_memory_kb} KB during test.')
    if diff_total_memory_pct > 0:
        print(f'Total Memory utilization has consumed and not returned {diff_total_memory_pct} KB during test.')
    if diff_reserved_memory_pct > 0:
        print(f'Reserved Memory utilization has consumed and not returned {diff_reserved_memory_pct} KB during test.')
    if diff_wired_memory_pct > 0:
        print(f'Wired Memory utilization has consumed and not returned {diff_wired_memory_pct} KB during test.')
    if diff_active_memory_pct > 0:
        print(f'Active Memory utilization has consumed and not returned {diff_active_memory_pct} KB during test.')
    if diff_inactive_memory_pct > 0:
        print(f'Inactive Memory utilization has consumed and not returned {diff_inactive_memory_pct} KB during test.')
    if diff_cache_memory_pct > 0:
        print(f'Total Cache utilization has consumed and not returned {diff_cache_memory_pct} KB during test.')
    if diff_free_memory_pct > 0:
        print(f'Free Memory utilization has consumed and not returned {diff_free_memory_pct} KB during test.')
    memory_dict = {'diff_total_memory_kb' : diff_total_memory_kb,
                   'diff_total_memory_pct' : diff_total_memory_pct,
                   'diff_reserved_memory_kb' : diff_reserved_memory_kb,
                   'diff_reserved_memory_pct' : diff_reserved_memory_pct,
                   'diff_wired_memory_kb' : diff_wired_memory_kb,
                   'diff_wired_memory_pct' : diff_wired_memory_pct,
                   'diff_active_memory_kb' : diff_active_memory_kb,
                   'diff_active_memory_pct' : diff_active_memory_pct,
                   'diff_inactive_memory_kb' : diff_inactive_memory_kb,
                   'diff_inactive_memory_pct' : diff_inactive_memory_pct,
                   'diff_cache_memory_kb' : diff_cache_memory_kb,
                   'diff_cache_memory_pct' : diff_cache_memory_pct,
                   'diff_free_memory_kb' : diff_free_memory_kb,
                   'diff_free_memory_pct' : diff_free_memory_pct
                   }
    return memory_dict
