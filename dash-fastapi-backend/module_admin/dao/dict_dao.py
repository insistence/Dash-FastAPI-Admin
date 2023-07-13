from sqlalchemy.orm import Session
from module_admin.entity.do.dict_do import SysDictType, SysDictData
from module_admin.entity.vo.dict_vo import DictTypeModel, DictTypePageObject, DictTypePageObjectResponse, \
    DictDataModel, DictDataPageObject, DictDataPageObjectResponse, CrudDictResponse
from utils.time_format_util import list_format_datetime
from utils.page_util import get_page_info
from datetime import datetime, time


def get_dict_type_detail_by_id(db: Session, dict_id: int):
    dict_type_info = db.query(SysDictType) \
        .filter(SysDictType.dict_id == dict_id) \
        .first()

    return dict_type_info


def get_dict_type_list(db: Session, page_object: DictTypePageObject):
    """
    根据查询参数获取字典类型列表信息
    :param db: orm对象
    :param page_object: 分页查询参数对象
    :return: 字典类型列表信息对象
    """
    count = db.query(SysDictType) \
        .filter(SysDictType.dict_name.like(f'%{page_object.dict_name}%') if page_object.dict_name else True,
                SysDictType.dict_type.like(f'%{page_object.dict_type}%') if page_object.dict_type else True,
                SysDictType.status == page_object.status if page_object.status else True,
                SysDictType.create_time.between(
                    datetime.combine(datetime.strptime(page_object.create_time_start, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(page_object.create_time_end, '%Y-%m-%d'), time(23, 59, 59)))
                            if page_object.create_time_start and page_object.create_time_end else True
                )\
        .distinct().count()
    offset_com = (page_object.page_num - 1) * page_object.page_size
    page_info = get_page_info(offset_com, page_object.page_num, page_object.page_size, count)
    dict_type_list = db.query(SysDictType) \
        .filter(SysDictType.dict_name.like(f'%{page_object.dict_name}%') if page_object.dict_name else True,
                SysDictType.dict_type.like(f'%{page_object.dict_type}%') if page_object.dict_type else True,
                SysDictType.status == page_object.status if page_object.status else True,
                SysDictType.create_time.between(
                    datetime.combine(datetime.strptime(page_object.create_time_start, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(page_object.create_time_end, '%Y-%m-%d'), time(23, 59, 59)))
                            if page_object.create_time_start and page_object.create_time_end else True
                )\
        .offset(page_info.offset) \
        .limit(page_object.page_size) \
        .distinct().all()

    result = dict(
        rows=list_format_datetime(dict_type_list),
        page_num=page_info.page_num,
        page_size=page_info.page_size,
        total=page_info.total,
        has_next=page_info.has_next
    )

    return DictTypePageObjectResponse(**result)


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


def get_dict_data_list(db: Session, page_object: DictDataPageObject):
    """
    根据查询参数获取字典数据列表信息
    :param db: orm对象
    :param page_object: 分页查询参数对象
    :return: 字典数据列表信息对象
    """
    count = db.query(SysDictData) \
        .filter(SysDictData.dict_type == page_object.dict_type if page_object.dict_type else True,
                SysDictData.dict_label.like(f'%{page_object.dict_label}%') if page_object.dict_label else True,
                SysDictData.status == page_object.status if page_object.status else True
                )\
        .order_by(SysDictData.dict_sort)\
        .distinct().count()
    offset_com = (page_object.page_num - 1) * page_object.page_size
    page_info = get_page_info(offset_com, page_object.page_num, page_object.page_size, count)
    dict_data_list = db.query(SysDictData) \
        .filter(SysDictData.dict_type == page_object.dict_type if page_object.dict_type else True,
                SysDictData.dict_label.like(f'%{page_object.dict_label}%') if page_object.dict_label else True,
                SysDictData.status == page_object.status if page_object.status else True
                )\
        .order_by(SysDictData.dict_sort)\
        .offset(page_info.offset) \
        .limit(page_object.page_size) \
        .distinct().all()

    result = dict(
        rows=list_format_datetime(dict_data_list),
        page_num=page_info.page_num,
        page_size=page_info.page_size,
        total=page_info.total,
        has_next=page_info.has_next
    )

    return DictDataPageObjectResponse(**result)


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
