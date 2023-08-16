from module_admin.entity.vo.log_vo import *
from module_admin.dao.log_dao import *
from utils.common_util import export_list2excel


def get_operation_log_list_services(result_db: Session, query_object: OperLogQueryModel):
    """
    获取操作日志列表信息service
    :param result_db: orm对象
    :param query_object: 查询参数对象
    :return: 操作日志列表信息对象
    """
    operation_log_list_result = get_operation_log_list(result_db, query_object)

    return operation_log_list_result


def add_operation_log_services(result_db: Session, page_object: OperLogModel):
    """
    新增操作日志service
    :param result_db: orm对象
    :param page_object: 新增操作日志对象
    :return: 新增操作日志校验结果
    """
    add_operation_log_result = add_operation_log_dao(result_db, page_object)

    return add_operation_log_result


def delete_operation_log_services(result_db: Session, page_object: DeleteOperLogModel):
    """
    删除操作日志信息service
    :param result_db: orm对象
    :param page_object: 删除操作日志对象
    :return: 删除操作日志校验结果
    """
    if page_object.oper_ids.split(','):
        oper_id_list = page_object.oper_ids.split(',')
        for oper_id in oper_id_list:
            oper_id_dict = dict(oper_id=oper_id)
            delete_operation_log_dao(result_db, OperLogModel(**oper_id_dict))
        result = dict(is_success=True, message='删除成功')
    else:
        result = dict(is_success=False, message='传入操作日志id为空')
    return CrudLogResponse(**result)


def clear_operation_log_services(result_db: Session, page_object: ClearOperLogModel):
    """
    清除操作日志信息service
    :param result_db: orm对象
    :param page_object: 清除操作日志对象
    :return: 清除操作日志校验结果
    """
    if page_object.oper_type == 'clear':
        clear_operation_log_dao(result_db)
        result = dict(is_success=True, message='清除成功')
    else:
        result = dict(is_success=False, message='清除标识不合法')

    return CrudLogResponse(**result)


def detail_operation_log_services(result_db: Session, oper_id: int):
    """
    获取操作日志详细信息service
    :param result_db: orm对象
    :param oper_id: 操作日志id
    :return: 操作日志id对应的信息
    """
    operation_log = get_operation_log_detail_by_id(result_db, oper_id=oper_id)

    return operation_log


def export_operation_log_list_services(operation_log_list: List):
    """
    导出操作日志信息service
    :param operation_log_list: 操作日志信息列表
    :return: 操作日志信息对应excel的二进制数据
    """
    # 创建一个映射字典，将英文键映射到中文键
    mapping_dict = {
        "oper_id": "日志编号",
        "title": "系统模块",
        "business_type": "操作类型",
        "method": "方法名称",
        "request_method": "请求方式",
        "oper_name": "操作人员",
        "dept_name": "部门名称",
        "oper_url": "请求URL",
        "oper_ip": "操作地址",
        "oper_location": "操作地点",
        "oper_param": "请求参数",
        "json_result": "返回参数",
        "status": "操作状态",
        "error_msg": "错误消息",
        "oper_time": "操作日期",
        "cost_time": "消耗时间"
    }

    data = [OperLogModel(**vars(row)).dict() for row in operation_log_list]

    for item in data:
        if item.get('status') == 0:
            item['status'] = '成功'
        else:
            item['status'] = '失败'
        if item.get('business_type') == 1:
            item['business_type'] = '新增'
        elif item.get('business_type') == 2:
            item['business_type'] = '修改'
        elif item.get('business_type') == 3:
            item['business_type'] = '删除'
        elif item.get('business_type') == 4:
            item['business_type'] = '授权'
        elif item.get('business_type') == 5:
            item['business_type'] = '导出'
        elif item.get('business_type') == 6:
            item['business_type'] = '导入'
        elif item.get('business_type') == 7:
            item['business_type'] = '强退'
        elif item.get('business_type') == 8:
            item['business_type'] = '生成代码'
        elif item.get('business_type') == 9:
            item['business_type'] = '清空数据'
        else:
            item['business_type'] = '其他'
    new_data = [{mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in data]
    binary_data = export_list2excel(new_data)

    return binary_data


def get_login_log_list_services(result_db: Session, query_object: LoginLogQueryModel):
    """
    获取登录日志列表信息service
    :param result_db: orm对象
    :param query_object: 查询参数对象
    :return: 登录日志列表信息对象
    """
    operation_log_list_result = get_login_log_list(result_db, query_object)

    return operation_log_list_result


def add_login_log_services(result_db: Session, page_object: LogininforModel):
    """
    新增登录日志service
    :param result_db: orm对象
    :param page_object: 新增登录日志对象
    :return: 新增登录日志校验结果
    """
    add_login_log_result = add_login_log_dao(result_db, page_object)

    return add_login_log_result


def delete_login_log_services(result_db: Session, page_object: DeleteLoginLogModel):
    """
    删除操作日志信息service
    :param result_db: orm对象
    :param page_object: 删除操作日志对象
    :return: 删除操作日志校验结果
    """
    if page_object.info_ids.split(','):
        info_id_list = page_object.info_ids.split(',')
        for info_id in info_id_list:
            info_id_dict = dict(info_id=info_id)
            delete_login_log_dao(result_db, LogininforModel(**info_id_dict))
        result = dict(is_success=True, message='删除成功')
    else:
        result = dict(is_success=False, message='传入登录日志id为空')
    return CrudLogResponse(**result)


def clear_login_log_services(result_db: Session, page_object: ClearLoginLogModel):
    """
    清除操作日志信息service
    :param result_db: orm对象
    :param page_object: 清除操作日志对象
    :return: 清除操作日志校验结果
    """
    if page_object.oper_type == 'clear':
        clear_login_log_dao(result_db)
        result = dict(is_success=True, message='清除成功')
    else:
        result = dict(is_success=False, message='清除标识不合法')

    return CrudLogResponse(**result)


def export_login_log_list_services(login_log_list: List):
    """
    导出登录日志信息service
    :param login_log_list: 登录日志信息列表
    :return: 登录日志信息对应excel的二进制数据
    """
    # 创建一个映射字典，将英文键映射到中文键
    mapping_dict = {
        "info_id": "访问编号",
        "user_name": "用户名称",
        "ipaddr": "登录地址",
        "login_location": "登录地点",
        "browser": "浏览器",
        "os": "操作系统",
        "status": "登录状态",
        "msg": "操作信息",
        "login_time": "登录日期"
    }

    data = [LogininforModel(**vars(row)).dict() for row in login_log_list]

    for item in data:
        if item.get('status') == '0':
            item['status'] = '成功'
        else:
            item['status'] = '失败'
    new_data = [{mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in data]
    binary_data = export_list2excel(new_data)

    return binary_data
