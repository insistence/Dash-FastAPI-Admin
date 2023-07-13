from module_admin.entity.vo.log_vo import *
from module_admin.dao.log_dao import *


def get_operation_log_list_services(result_db: Session, page_object: OperLogPageObject):
    """
    获取操作日志列表信息service
    :param result_db: orm对象
    :param page_object: 分页查询参数对象
    :return: 操作日志列表信息对象
    """
    operation_log_list_result = get_operation_log_list(result_db, page_object)

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


def get_login_log_list_services(result_db: Session, page_object: LoginLogPageObject):
    """
    获取登录日志列表信息service
    :param result_db: orm对象
    :param page_object: 分页查询参数对象
    :return: 登录日志列表信息对象
    """
    operation_log_list_result = get_login_log_list(result_db, page_object)

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
