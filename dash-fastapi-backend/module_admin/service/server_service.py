import psutil
from utils.common_util import bytes2human
import platform
import socket
import os
import time
from module_admin.entity.vo.server_vo import *


def get_server_monitor_info():
    # CPU信息
    # 获取CPU总核心数
    cpu_num = psutil.cpu_count(logical=True)
    cpu_usage_percent = psutil.cpu_times_percent()
    cpu_used = f'{cpu_usage_percent.user}%'
    cpu_sys = f'{cpu_usage_percent.system}%'
    cpu_free = f'{cpu_usage_percent.idle}%'
    cpu = CpuInfo(**dict(cpu_num=cpu_num, used=cpu_used, sys=cpu_sys, free=cpu_free))

    # 内存信息
    memory_info = psutil.virtual_memory()
    memory_total = bytes2human(memory_info.total)
    memory_used = bytes2human(memory_info.used)
    memory_free = bytes2human(memory_info.free)
    memory_usage = f'{memory_info.percent}%'
    mem = MemoryInfo(**dict(total=memory_total, used=memory_used, free=memory_free, usage=memory_usage))

    # 主机信息
    # 获取主机名
    hostname = socket.gethostname()
    # 获取IP
    computer_ip = socket.gethostbyname(hostname)
    os_name = platform.platform()
    computer_name = platform.node()
    os_arch = platform.machine()
    sys = SysInfo(**dict(computer_ip=computer_ip, computer_name=computer_name, os_arch=os_arch, os_name=os_name))

    # python解释器信息
    current_pid = os.getpid()
    current_process = psutil.Process(current_pid)
    python_name = current_process.name()
    python_version = platform.python_version()
    python_home = current_process.exe()
    start_time_stamp = current_process.create_time()
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time_stamp))
    current_time_stamp = time.time()
    difference = current_time_stamp - start_time_stamp
    # 将时间差转换为天、小时和分钟数
    days = int(difference // (24 * 60 * 60))  # 每天的秒数
    hours = int((difference % (24 * 60 * 60)) // (60 * 60))  # 每小时的秒数
    minutes = int((difference % (60 * 60)) // 60)  # 每分钟的秒数
    run_time = f"{days}天{hours}小时{minutes}分钟"
    project_dir = os.path.abspath(os.getcwd())
    py = PyInfo(
        **dict(
            name=python_name,
            version=python_version,
            start_time=start_time,
            run_time=run_time,
            home=python_home,
            project_dir=project_dir
        )
    )

    # 磁盘信息
    io = psutil.disk_partitions()
    sys_files = []
    for i in io:
        o = psutil.disk_usage(i.device)
        disk_data = {
            "dir_name": i.device,
            "sys_type_name": i.fstype,
            "disk_name": "本地固定磁盘（" + i.mountpoint.replace('\\', '') + "）",
            "total": bytes2human(o.total),
            "used": bytes2human(o.used),
            "free": bytes2human(o.free),
            "usage": f'{psutil.disk_usage(i.device).percent}%'
        }
        sys_files.append(SysFiles(**disk_data))

    result = dict(cpu=cpu, mem=mem, sys=sys, py=py, sys_files=sys_files)

    return ServerMonitorModel(**result)
