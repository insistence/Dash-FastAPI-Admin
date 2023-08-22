from sqlalchemy import and_
from sqlalchemy.orm import Session
from module_admin.entity.do.dict_do import SysDictType, SysDictData
from module_admin.entity.vo.dict_vo import DictTypeModel, DictTypeQueryModel, DictDataModel, CrudDictResponse
from utils.time_format_util import list_format_datetime
from datetime import datetime, time


def get_dict_type_detail_by_id(db: Session, dict_id: int):
    dict_type_info = db.query(SysDictType) \
        .filter(SysDictType.dict_id == dict_id) \
        .first()

    return dict_type_info


def get_all_dict_type(db: Session):
    dict_type_info = db.query(SysDictType).all()

    return list_format_datetime(dict_type_info)


def get_dict_type_list(db: Session, query_object: DictTypeQueryModel):
    """
    根据查询参数获取字典类型列表信息
    :param db: orm对象
    :param query_object: 查询参数对象
    :return: 字典类型列表信息对象
    """
    dict_type_list = db.query(SysDictType) \
        .filter(SysDictType.dict_name.like(f'%{query_object.dict_name}%') if query_object.dict_name else True,
                SysDictType.dict_type.like(f'%{query_object.dict_type}%') if query_object.dict_type else True,
                SysDictType.status == query_object.status if query_object.status else True,
                SysDictType.create_time.between(
                    datetime.combine(datetime.strptime(query_object.create_time_start, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.create_time_end, '%Y-%m-%d'), time(23, 59, 59)))
                if query_object.create_time_start and query_object.create_time_end else True
                ) \
        .distinct().all()

    return list_format_datetime(dict_type_list)


def add_dict_type_dao(db: Session, dict_type: DictTypeModel):
    """
    新增字典类型数据库操作
    :param db: orm对象
    :param dict_type: 字典类型对象
    :return: 新增校验结果
    """
    db_dict_type = SysDictType(**dict_type.dict())
    db.add(db_dict_type)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_dict_type)  # 刷新
    result = dict(is_success=True, message='新增成功')

    return CrudDictResponse(**result)


def edit_dict_type_dao(db: Session, dict_type: dict):
    """
    编辑字典类型数据库操作
    :param db: orm对象
    :param dict_type: 需要更新的字典类型字典
    :return: 编辑校验结果
    """
    is_dict_type_id = db.query(SysDictType).filter(SysDictType.dict_id == dict_type.get('dict_id')).all()
    if not is_dict_type_id:
        result = dict(is_success=False, message='字典类型不存在')
    else:
        db.query(SysDictType) \
            .filter(SysDictType.dict_id == dict_type.get('dict_id')) \
            .update(dict_type)
        db.commit()  # 提交保存到数据库中
        result = dict(is_success=True, message='更新成功')

    return CrudDictResponse(**result)


def delete_dict_type_dao(db: Session, dict_type: DictTypeModel):
    """
    删除字典类型数据库操作
    :param db: orm对象
    :param dict_type: 字典类型对象
    :return:
    """
    db.query(SysDictType) \
        .filter(SysDictType.dict_id == dict_type.dict_id) \
        .delete()
    db.commit()  # 提交保存到数据库中


def get_dict_data_detail_by_id(db: Session, dict_code: int):
    dict_data_info = db.query(SysDictData) \
        .filter(SysDictData.dict_code == dict_code) \
        .first()

    return dict_data_info


def get_dict_data_list(db: Session, query_object: DictDataModel):
    """
    根据查询参数获取字典数据列表信息
    :param db: orm对象
    :param query_object: 查询参数对象
    :return: 字典数据列表信息对象
    """
    dict_data_list = db.query(SysDictData) \
        .filter(SysDictData.dict_type == query_object.dict_type if query_object.dict_type else True,
                SysDictData.dict_label.like(f'%{query_object.dict_label}%') if query_object.dict_label else True,
                SysDictData.status == query_object.status if query_object.status else True
                ) \
        .order_by(SysDictData.dict_sort) \
        .distinct().all()

    return list_format_datetime(dict_data_list)


def query_dict_data_list(db: Session, dict_type: str):
    """
    根据查询参数获取字典数据列表信息
    :param db: orm对象
    :param dict_type: 字典类型
    :return: 字典数据列表信息对象
    """
    dict_data_list = db.query(SysDictData).select_from(SysDictType) \
        .filter(SysDictType.dict_type == dict_type if dict_type else True, SysDictType.status == 0) \
        .outerjoin(SysDictData, and_(SysDictType.dict_type == SysDictData.dict_type, SysDictData.status == 0)) \
        .order_by(SysDictData.dict_sort) \
        .distinct().all()

    return list_format_datetime(dict_data_list)


def add_dict_data_dao(db: Session, dict_data: DictDataModel):
    """
    新增字典数据数据库操作
    :param db: orm对象
    :param dict_data: 字典数据对象
    :return: 新增校验结果
    """
    db_data_type = SysDictData(**dict_data.dict())
    db.add(db_data_type)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_data_type)  # 刷新
    result = dict(is_success=True, message='新增成功')

    return CrudDictResponse(**result)


def edit_dict_data_dao(db: Session, dict_data: dict):
    """
    编辑字典数据数据库操作
    :param db: orm对象
    :param dict_data: 需要更新的字典数据字典
    :return: 编辑校验结果
    """
    is_dict_data_id = db.query(SysDictData).filter(SysDictData.dict_code == dict_data.get('dict_code')).all()
    if not is_dict_data_id:
        result = dict(is_success=False, message='字典数据不存在')
    else:
        db.query(SysDictData) \
            .filter(SysDictData.dict_code == dict_data.get('dict_code')) \
            .update(dict_data)
        db.commit()  # 提交保存到数据库中
        result = dict(is_success=True, message='更新成功')

    return CrudDictResponse(**result)


def delete_dict_data_dao(db: Session, dict_data: DictDataModel):
    """
    删除字典数据数据库操作
    :param db: orm对象
    :param dict_data: 字典数据对象
    :return:
    """
    db.query(SysDictData) \
        .filter(SysDictData.dict_code == dict_data.dict_code) \
        .delete()
    db.commit()  # 提交保存到数据库中
