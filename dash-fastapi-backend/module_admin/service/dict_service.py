from module_admin.entity.vo.dict_vo import *
from module_admin.dao.dict_dao import *


def get_dict_type_list_services(result_db: Session, query_object: DictTypePageObject):
    """
    获取字典类型列表信息service
    :param result_db: orm对象
    :param query_object: 查询参数对象
    :return: 字典类型列表信息对象
    """
    dict_type_list_result = get_dict_type_list(result_db, query_object)

    return dict_type_list_result


def get_all_dict_type_services(result_db: Session):
    """
    获取字所有典类型列表信息service
    :param result_db: orm对象
    :return: 字典类型列表信息对象
    """
    dict_type_list_result = get_all_dict_type(result_db)

    return dict_type_list_result


def add_dict_type_services(result_db: Session, page_object: DictTypeModel):
    """
    新增字典类型信息service
    :param result_db: orm对象
    :param page_object: 新增岗位对象
    :return: 新增字典类型校验结果
    """
    add_dict_type_result = add_dict_type_dao(result_db, page_object)

    return add_dict_type_result


def edit_dict_type_services(result_db: Session, page_object: DictTypeModel):
    """
    编辑字典类型信息service
    :param result_db: orm对象
    :param page_object: 编辑字典类型对象
    :return: 编辑字典类型校验结果
    """
    edit_dict_type = page_object.dict(exclude_unset=True)
    edit_dict_type_result = edit_dict_type_dao(result_db, edit_dict_type)

    return edit_dict_type_result


def delete_dict_type_services(result_db: Session, page_object: DeleteDictTypeModel):
    """
    删除字典类型信息service
    :param result_db: orm对象
    :param page_object: 删除字典类型对象
    :return: 删除字典类型校验结果
    """
    if page_object.dict_ids.split(','):
        dict_id_list = page_object.dict_ids.split(',')
        for dict_id in dict_id_list:
            dict_id_dict = dict(dict_id=dict_id)
            delete_dict_type_dao(result_db, DictTypeModel(**dict_id_dict))
        result = dict(is_success=True, message='删除成功')
    else:
        result = dict(is_success=False, message='传入字典类型id为空')
    return CrudDictResponse(**result)


def detail_dict_type_services(result_db: Session, dict_id: int):
    """
    获取字典类型详细信息service
    :param result_db: orm对象
    :param dict_id: 字典类型id
    :return: 字典类型id对应的信息
    """
    dict_type = get_dict_type_detail_by_id(result_db, dict_id=dict_id)

    return dict_type


def get_dict_data_list_services(result_db: Session, query_object: DictDataPageObject):
    """
    获取字典数据列表信息service
    :param result_db: orm对象
    :param query_object: 查询参数对象
    :return: 字典数据列表信息对象
    """
    dict_data_list_result = get_dict_data_list(result_db, query_object)

    return dict_data_list_result


def add_dict_data_services(result_db: Session, page_object: DictDataModel):
    """
    新增字典数据信息service
    :param result_db: orm对象
    :param page_object: 新增岗位对象
    :return: 新增字典数据校验结果
    """
    add_dict_data_result = add_dict_data_dao(result_db, page_object)

    return add_dict_data_result


def edit_dict_data_services(result_db: Session, page_object: DictDataModel):
    """
    编辑字典数据信息service
    :param result_db: orm对象
    :param page_object: 编辑字典数据对象
    :return: 编辑字典数据校验结果
    """
    edit_data_type = page_object.dict(exclude_unset=True)
    edit_dict_data_result = edit_dict_data_dao(result_db, edit_data_type)

    return edit_dict_data_result


def delete_dict_data_services(result_db: Session, page_object: DeleteDictDataModel):
    """
    删除字典数据信息service
    :param result_db: orm对象
    :param page_object: 删除字典数据对象
    :return: 删除字典数据校验结果
    """
    if page_object.dict_codes.split(','):
        dict_code_list = page_object.dict_codes.split(',')
        for dict_code in dict_code_list:
            dict_code_dict = dict(dict_code=dict_code)
            delete_dict_data_dao(result_db, DictDataModel(**dict_code_dict))
        result = dict(is_success=True, message='删除成功')
    else:
        result = dict(is_success=False, message='传入字典数据id为空')
    return CrudDictResponse(**result)


def detail_dict_data_services(result_db: Session, dict_code: int):
    """
    获取字典数据详细信息service
    :param result_db: orm对象
    :param dict_code: 字典数据id
    :return: 字典数据id对应的信息
    """
    dict_data = get_dict_data_detail_by_id(result_db, dict_code=dict_code)

    return dict_data
