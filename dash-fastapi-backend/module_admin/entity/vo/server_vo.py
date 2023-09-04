from pydantic import BaseModel
from typing import Optional, List


class CpuInfo(BaseModel):
    cpu_num: Optional[int]
    used: Optional[str]
    sys: Optional[str]
    free: Optional[str]


class MemoryInfo(BaseModel):
    total: Optional[str]
    used: Optional[str]
    free: Optional[str]
    usage: Optional[str]


class SysInfo(BaseModel):
    computer_ip: Optional[str]
    computer_name: Optional[str]
    os_arch: Optional[str]
    os_name: Optional[str]


class PyInfo(BaseModel):
    name: Optional[str]
    version: Optional[str]
    start_time: Optional[str]
    run_time: Optional[str]
    home: Optional[str]
    project_dir: Optional[str]


class SysFiles(BaseModel):
    dir_name: Optional[str]
    sys_type_name: Optional[str]
    disk_name: Optional[str]
    total: Optional[str]
    used: Optional[str]
    free: Optional[str]
    usage: Optional[str]


class ServerMonitorModel(BaseModel):
    """
    服务监控对应pydantic模型
    """
    cpu: Optional[CpuInfo]
    py: Optional[PyInfo]
    mem: Optional[MemoryInfo]
    sys: Optional[SysInfo]
    sys_files: Optional[List[SysFiles]]
