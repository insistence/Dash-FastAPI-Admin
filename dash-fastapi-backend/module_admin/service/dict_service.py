from fastapi import Request
import json
from config.env import RedisInitKeyConfig
from module_admin.entity.vo.dict_vo import *
from module_admin.dao.dict_dao import *
from utils.common_util import export_list2excel


class DictTypeService:
    """
    字典类型管理模块服务层
    """

    @classmethod
    def get_dict_type_list_services(cls, result_db: Session, query_object: DictTypeQueryModel):
        """
        获取字典类型列表信息service
        :param result_db: orm对象
        :param query_object: 查询参数对象
        :return: 字典类型列表信息对象
        """
        dict_type_list_result = DictTypeDao.get_dict_type_list(result_db, query_object)

        return dict_type_list_result

    @classmethod
    def get_all_dict_type_services(cls, result_db: Session):
        """
        获取字所有典类型列表信息service
        :param result_db: orm对象
        :return: 字典类型列表信息对象
        """
        dict_type_list_result = DictTypeDao.get_all_dict_type(result_db)

        return dict_type_list_result

    @classmethod
    async def add_dict_type_services(cls, request: Request, result_db: Session, page_object: DictTypeModel):
        """
        新增字典类型信息service
        :param request: Request对象
        :param result_db: orm对象
        :param page_object: 新增岗位对象
        :return: 新增字典类型校验结果
        """
        dict_type = DictTypeDao.get_dict_type_detail_by_info(result_db, DictTypeModel(**dict(dict_type=page_object.dict_type)))
        if dict_type:
            result = dict(is_success=False, message='字典类型已存在')
        else:
            try:
                DictTypeDao.add_dict_type_dao(result_db, page_object)
                result_db.commit()
                await DictDataService.init_cache_sys_dict_services(result_db, request.app.state.redis)
                result = dict(is_success=True, message='新增成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))

        return CrudDictResponse(**result)

    @classmethod
    async def edit_dict_type_services(cls, request: Request, result_db: Session, page_object: DictTypeModel):
        """
        编辑字典类型信息service
        :param request: Request对象
        :param result_db: orm对象
        :param page_object: 编辑字典类型对象
        :return: 编辑字典类型校验结果
        """
        edit_dict_type = page_object.dict(exclude_unset=True)
        dict_type_info = cls.detail_dict_type_services(result_db, edit_dict_type.get('dict_id'))
        if dict_type_info:
            if dict_type_info.dict_type != page_object.dict_type or dict_type_info.dict_name != page_object.dict_name:
                dict_type = DictTypeDao.get_dict_type_detail_by_info(result_db, DictTypeModel(
                    **dict(dict_type=page_object.dict_type)))
                if dict_type:
                    result = dict(is_success=False, message='字典类型已存在')
                    return CrudDictResponse(**result)
            try:
                if dict_type_info.dict_type != page_object.dict_type:
                    query_dict_data = DictDataModel(**(dict(dict_type=dict_type_info.dict_type)))
                    dict_data_list = DictDataDao.get_dict_data_list(result_db, query_dict_data)
                    for dict_data in dict_data_list:
                        edit_dict_data = DictDataModel(**(dict(dict_code=dict_data.dict_code, dict_type=page_object.dict_type, update_by=page_object.update_by))).dict(exclude_unset=True)
                        DictDataDao.edit_dict_data_dao(result_db, edit_dict_data)
                DictTypeDao.edit_dict_type_dao(result_db, edit_dict_type)
                result_db.commit()
                await DictDataService.init_cache_sys_dict_services(result_db, request.app.state.redis)
                result = dict(is_success=True, message='更新成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='字典类型不存在')

        return CrudDictResponse(**result)

    @classmethod
    async def delete_dict_type_services(cls, request: Request, result_db: Session, page_object: DeleteDictTypeModel):
        """
        删除字典类型信息service
        :param request: Request对象
        :param result_db: orm对象
        :param page_object: 删除字典类型对象
        :return: 删除字典类型校验结果
        """
        if page_object.dict_ids.split(','):
            dict_id_list = page_object.dict_ids.split(',')
            try:
                for dict_id in dict_id_list:
                    dict_id_dict = dict(dict_id=dict_id)
                    DictTypeDao.delete_dict_type_dao(result_db, DictTypeModel(**dict_id_dict))
                result_db.commit()
                await DictDataService.init_cache_sys_dict_services(result_db, request.app.state.redis)
                result = dict(is_success=True, message='删除成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='传入字典类型id为空')
        return CrudDictResponse(**result)

    @classmethod
    def detail_dict_type_services(cls, result_db: Session, dict_id: int):
        """
        获取字典类型详细信息service
        :param result_db: orm对象
        :param dict_id: 字典类型id
        :return: 字典类型id对应的信息
        """
        dict_type = DictTypeDao.get_dict_type_detail_by_id(result_db, dict_id=dict_id)

        return dict_type

    @staticmethod
    def export_dict_type_list_services(dict_type_list: List):
        """
        导出字典类型信息service
        :param dict_type_list: 字典信息列表
        :return: 字典信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            "dict_id": "字典编号",
            "dict_name": "字典名称",
            "dict_type": "字典类型",
            "status": "状态",
            "create_by": "创建者",
            "create_time": "创建时间",
            "update_by": "更新者",
            "update_time": "更新时间",
            "remark": "备注",
        }

        data = [DictTypeModel(**vars(row)).dict() for row in dict_type_list]

        for item in data:
            if item.get('status') == '0':
                item['status'] = '正常'
            else:
                item['status'] = '停用'
        new_data = [{mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in data]
        binary_data = export_list2excel(new_data)

        return binary_data

    @classmethod
    async def refresh_sys_dict_services(cls, request: Request, result_db: Session):
        """
        刷新字典缓存信息service
        :param request: Request对象
        :param result_db: orm对象
        :return: 刷新字典缓存校验结果
        """
        await DictDataService.init_cache_sys_dict_services(result_db, request.app.state.redis)
        result = dict(is_success=True, message='刷新成功')

        return CrudDictResponse(**result)


class DictDataService:
    """
    字典数据管理模块服务层
    """

    @classmethod
    def get_dict_data_list_services(cls, result_db: Session, query_object: DictDataModel):
        """
        获取字典数据列表信息service
        :param result_db: orm对象
        :param query_object: 查询参数对象
        :return: 字典数据列表信息对象
        """
        dict_data_list_result = DictDataDao.get_dict_data_list(result_db, query_object)

        return dict_data_list_result

    @classmethod
    def query_dict_data_list_services(cls, result_db: Session, dict_type: str):
        """
        获取字典数据列表信息service
        :param result_db: orm对象
        :param dict_type: 字典类型
        :return: 字典数据列表信息对象
        """
        dict_data_list_result = DictDataDao.query_dict_data_list(result_db, dict_type)

        return dict_data_list_result

    @classmethod
    async def init_cache_sys_dict_services(cls, result_db: Session, redis):
        """
        应用初始化：获取所有字典类型对应的字典数据信息并缓存service
        :param result_db: orm对象
        :param redis: redis对象
        :return:
        """
        # 获取以sys_dict:开头的键列表
        keys = await redis.keys(f"{RedisInitKeyConfig.SYS_DICT.get('key')}:*")
        # 删除匹配的键
        if keys:
            await redis.delete(*keys)
        dict_type_all = DictTypeDao.get_all_dict_type(result_db)
        for dict_type_obj in [item for item in dict_type_all if item.status == '0']:
            dict_type = dict_type_obj.dict_type
            dict_data_list = DictDataDao.query_dict_data_list(result_db, dict_type)
            dict_data = [DictDataModel(**vars(row)).dict() for row in dict_data_list if row]
            await redis.set(f"{RedisInitKeyConfig.SYS_DICT.get('key')}:{dict_type}", json.dumps(dict_data, ensure_ascii=False))

    @classmethod
    async def query_dict_data_list_from_cache_services(cls, redis, dict_type: str):
        """
        从缓存获取字典数据列表信息service
        :param redis: redis对象
        :param dict_type: 字典类型
        :return: 字典数据列表信息对象
        """
        result = []
        dict_data_list_result = await redis.get(f"{RedisInitKeyConfig.SYS_DICT.get('key')}:{dict_type}")
        if dict_data_list_result:
            result = json.loads(dict_data_list_result)

        return result

    @classmethod
    async def add_dict_data_services(cls, request: Request, result_db: Session, page_object: DictDataModel):
        """
        新增字典数据信息service
        :param request: Request对象
        :param result_db: orm对象
        :param page_object: 新增岗位对象
        :return: 新增字典数据校验结果
        """
        dict_data = DictDataDao.get_dict_data_detail_by_info(result_db, page_object)
        if dict_data:
            result = dict(is_success=False, message='字典数据已存在')
        else:
            try:
                DictDataDao.add_dict_data_dao(result_db, page_object)
                result_db.commit()
                await cls.init_cache_sys_dict_services(result_db, request.app.state.redis)
                result = dict(is_success=True, message='新增成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))

        return CrudDictResponse(**result)

    @classmethod
    async def edit_dict_data_services(cls, request: Request, result_db: Session, page_object: DictDataModel):
        """
        编辑字典数据信息service
        :param request: Request对象
        :param result_db: orm对象
        :param page_object: 编辑字典数据对象
        :return: 编辑字典数据校验结果
        """
        edit_data_type = page_object.dict(exclude_unset=True)
        dict_data_info = cls.detail_dict_data_services(result_db, edit_data_type.get('dict_code'))
        if dict_data_info:
            if dict_data_info.dict_type != page_object.dict_type or dict_data_info.dict_label != page_object.dict_label or dict_data_info.dict_value != page_object.dict_value:
                dict_data = DictDataDao.get_dict_data_detail_by_info(result_db, page_object)
                if dict_data:
                    result = dict(is_success=False, message='字典数据已存在')
                    return CrudDictResponse(**result)
            try:
                DictDataDao.edit_dict_data_dao(result_db, edit_data_type)
                result_db.commit()
                await cls.init_cache_sys_dict_services(result_db, request.app.state.redis)
                result = dict(is_success=True, message='更新成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='字典数据不存在')

        return CrudDictResponse(**result)

    @classmethod
    async def delete_dict_data_services(cls, request: Request, result_db: Session, page_object: DeleteDictDataModel):
        """
        删除字典数据信息service
        :param request: Request对象
        :param result_db: orm对象
        :param page_object: 删除字典数据对象
        :return: 删除字典数据校验结果
        """
        if page_object.dict_codes.split(','):
            dict_code_list = page_object.dict_codes.split(',')
            try:
                for dict_code in dict_code_list:
                    dict_code_dict = dict(dict_code=dict_code)
                    DictDataDao.delete_dict_data_dao(result_db, DictDataModel(**dict_code_dict))
                result_db.commit()
                await cls.init_cache_sys_dict_services(result_db, request.app.state.redis)
                result = dict(is_success=True, message='删除成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='传入字典数据id为空')
        return CrudDictResponse(**result)

    @classmethod
    def detail_dict_data_services(cls, result_db: Session, dict_code: int):
        """
        获取字典数据详细信息service
        :param result_db: orm对象
        :param dict_code: 字典数据id
        :return: 字典数据id对应的信息
        """
        dict_data = DictDataDao.get_dict_data_detail_by_id(result_db, dict_code=dict_code)

        return dict_data

    @staticmethod
    def export_dict_data_list_services(dict_data_list: List):
        """
        导出字典数据信息service
        :param dict_data_list: 字典数据信息列表
        :return: 字典数据信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            "dict_code": "字典编码",
            "dict_sort": "字典标签",
            "dict_label": "字典键值",
            "dict_value": "字典排序",
            "dict_type": "字典类型",
            "css_class": "样式属性",
            "list_class": "表格回显样式",
            "is_default": "是否默认",
            "status": "状态",
            "create_by": "创建者",
            "create_time": "创建时间",
            "update_by": "更新者",
            "update_time": "更新时间",
            "remark": "备注",
        }

        data = [DictDataModel(**vars(row)).dict() for row in dict_data_list]

        for item in data:
            if item.get('status') == '0':
                item['status'] = '正常'
            else:
                item['status'] = '停用'
            if item.get('is_default') == 'Y':
                item['is_default'] = '是'
            else:
                item['is_default'] = '否'
        new_data = [{mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in data]
        binary_data = export_list2excel(new_data)

        return binary_data
