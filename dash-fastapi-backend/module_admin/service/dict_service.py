import json
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from config.enums import RedisInitKeyConfig
from exceptions.exception import ServiceException
from module_admin.dao.dict_dao import DictDataDao, DictTypeDao
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.dict_vo import (
    DeleteDictDataModel,
    DeleteDictTypeModel,
    DictDataModel,
    DictDataPageQueryModel,
    DictTypeModel,
    DictTypePageQueryModel,
)
from utils.common_util import export_list2excel, SqlalchemyUtil


class DictTypeService:
    """
    字典类型管理模块服务层
    """

    @classmethod
    async def get_dict_type_list_services(
        cls, query_db: AsyncSession, query_object: DictTypePageQueryModel, is_page: bool = False
    ):
        """
        获取字典类型列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 字典类型列表信息对象
        """
        dict_type_list_result = await DictTypeDao.get_dict_type_list(query_db, query_object, is_page)

        return dict_type_list_result

    @classmethod
    async def check_dict_type_unique_services(cls, query_db: AsyncSession, page_object: DictTypeModel):
        """
        校验字典类型称是否唯一service

        :param query_db: orm对象
        :param page_object: 字典类型对象
        :return: 校验结果
        """
        dict_id = -1 if page_object.dict_id is None else page_object.dict_id
        dict_type = await DictTypeDao.get_dict_type_detail_by_info(
            query_db, DictTypeModel(dict_type=page_object.dict_type)
        )
        if dict_type and dict_type.dict_id != dict_id:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def add_dict_type_services(cls, request: Request, query_db: AsyncSession, page_object: DictTypeModel):
        """
        新增字典类型信息service

        :param request: Request对象
        :param query_db: orm对象
        :param page_object: 新增岗位对象
        :return: 新增字典类型校验结果
        """
        if not await cls.check_dict_type_unique_services(query_db, page_object):
            raise ServiceException(message=f'新增字典{page_object.dict_name}失败，字典类型已存在')
        else:
            try:
                await DictTypeDao.add_dict_type_dao(query_db, page_object)
                await query_db.commit()
                await request.app.state.redis.set(f'{RedisInitKeyConfig.SYS_DICT.key}:{page_object.dict_type}', '')
                result = dict(is_success=True, message='新增成功')
            except Exception as e:
                await query_db.rollback()
                raise e

        return CrudResponseModel(**result)

    @classmethod
    async def edit_dict_type_services(cls, request: Request, query_db: AsyncSession, page_object: DictTypeModel):
        """
        编辑字典类型信息service

        :param request: Request对象
        :param query_db: orm对象
        :param page_object: 编辑字典类型对象
        :return: 编辑字典类型校验结果
        """
        edit_dict_type = page_object.model_dump(exclude_unset=True)
        dict_type_info = await cls.dict_type_detail_services(query_db, page_object.dict_id)
        if dict_type_info.dict_id:
            if not await cls.check_dict_type_unique_services(query_db, page_object):
                raise ServiceException(message=f'修改字典{page_object.dict_name}失败，字典类型已存在')
            else:
                try:
                    query_dict_data = DictDataPageQueryModel(dict_type=dict_type_info.dict_type)
                    dict_data_list = await DictDataDao.get_dict_data_list(query_db, query_dict_data, is_page=False)
                    if dict_type_info.dict_type != page_object.dict_type:
                        for dict_data in dict_data_list:
                            edit_dict_data = DictDataModel(
                                dict_code=dict_data.dict_code,
                                dict_type=page_object.dict_type,
                                update_by=page_object.update_by,
                            ).model_dump(exclude_unset=True)
                            await DictDataDao.edit_dict_data_dao(query_db, edit_dict_data)
                    await DictTypeDao.edit_dict_type_dao(query_db, edit_dict_type)
                    await query_db.commit()
                    if dict_type_info.dict_type != page_object.dict_type:
                        dict_data = [SqlalchemyUtil.serialize_result(row) for row in dict_data_list if row]
                        await request.app.state.redis.set(
                            f'{RedisInitKeyConfig.SYS_DICT.key}:{page_object.dict_type}',
                            json.dumps(dict_data, ensure_ascii=False, default=str),
                        )
                    return CrudResponseModel(is_success=True, message='更新成功')
                except Exception as e:
                    await query_db.rollback()
                    raise e
        else:
            raise ServiceException(message='字典类型不存在')

    @classmethod
    async def delete_dict_type_services(
        cls, request: Request, query_db: AsyncSession, page_object: DeleteDictTypeModel
    ):
        """
        删除字典类型信息service

        :param request: Request对象
        :param query_db: orm对象
        :param page_object: 删除字典类型对象
        :return: 删除字典类型校验结果
        """
        if page_object.dict_ids:
            dict_id_list = page_object.dict_ids.split(',')
            try:
                delete_dict_type_list = []
                for dict_id in dict_id_list:
                    dict_type_into = await cls.dict_type_detail_services(query_db, int(dict_id))
                    if (await DictDataDao.count_dict_data_dao(query_db, dict_type_into.dict_type)) > 0:
                        raise ServiceException(message=f'{dict_type_into.dict_name}已分配，不能删除')
                    await DictTypeDao.delete_dict_type_dao(query_db, DictTypeModel(dict_id=int(dict_id)))
                    delete_dict_type_list.append(f'{RedisInitKeyConfig.SYS_DICT.key}:{dict_type_into.dict_type}')
                await query_db.commit()
                if delete_dict_type_list:
                    await request.app.state.redis.delete(*delete_dict_type_list)
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入字典类型id为空')

    @classmethod
    async def dict_type_detail_services(cls, query_db: AsyncSession, dict_id: int):
        """
        获取字典类型详细信息service

        :param query_db: orm对象
        :param dict_id: 字典类型id
        :return: 字典类型id对应的信息
        """
        dict_type = await DictTypeDao.get_dict_type_detail_by_id(query_db, dict_id=dict_id)
        if dict_type:
            result = DictTypeModel(**SqlalchemyUtil.serialize_result(dict_type))
        else:
            result = DictTypeModel(**dict())

        return result

    @staticmethod
    async def export_dict_type_list_services(dict_type_list: List):
        """
        导出字典类型信息service

        :param dict_type_list: 字典信息列表
        :return: 字典信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'dict_id': '字典编号',
            'dict_name': '字典名称',
            'dict_type': '字典类型',
            'status': '状态',
            'create_by': '创建者',
            'create_time': '创建时间',
            'update_by': '更新者',
            'update_time': '更新时间',
            'remark': '备注',
        }

        data = dict_type_list

        for item in data:
            if item.get('status') == '0':
                item['status'] = '正常'
            else:
                item['status'] = '停用'
        new_data = [
            {mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in data
        ]
        binary_data = export_list2excel(new_data)

        return binary_data

    @classmethod
    async def refresh_sys_dict_services(cls, request: Request, query_db: AsyncSession):
        """
        刷新字典缓存信息service

        :param request: Request对象
        :param query_db: orm对象
        :return: 刷新字典缓存校验结果
        """
        await DictDataService.init_cache_sys_dict_services(query_db, request.app.state.redis)
        result = dict(is_success=True, message='刷新成功')

        return CrudResponseModel(**result)


class DictDataService:
    """
    字典数据管理模块服务层
    """

    @classmethod
    async def get_dict_data_list_services(
        cls, query_db: AsyncSession, query_object: DictDataPageQueryModel, is_page: bool = False
    ):
        """
        获取字典数据列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 字典数据列表信息对象
        """
        dict_data_list_result = await DictDataDao.get_dict_data_list(query_db, query_object, is_page)

        return dict_data_list_result

    @classmethod
    async def query_dict_data_list_services(cls, query_db: AsyncSession, dict_type: str):
        """
        获取字典数据列表信息service

        :param query_db: orm对象
        :param dict_type: 字典类型
        :return: 字典数据列表信息对象
        """
        dict_data_list_result = await DictDataDao.query_dict_data_list(query_db, dict_type)

        return dict_data_list_result

    @classmethod
    async def init_cache_sys_dict_services(cls, query_db: AsyncSession, redis):
        """
        应用初始化：获取所有字典类型对应的字典数据信息并缓存service

        :param query_db: orm对象
        :param redis: redis对象
        :return:
        """
        # 获取以sys_dict:开头的键列表
        keys = await redis.keys(f'{RedisInitKeyConfig.SYS_DICT.key}:*')
        # 删除匹配的键
        if keys:
            await redis.delete(*keys)
        dict_type_all = await DictTypeDao.get_all_dict_type(query_db)
        for dict_type_obj in [item for item in dict_type_all if item.status == '0']:
            dict_type = dict_type_obj.dict_type
            dict_data_list = await DictDataDao.query_dict_data_list(query_db, dict_type)
            dict_data = [SqlalchemyUtil.serialize_result(row) for row in dict_data_list if row]
            await redis.set(
                f'{RedisInitKeyConfig.SYS_DICT.key}:{dict_type}',
                json.dumps(dict_data, ensure_ascii=False, default=str),
            )

    @classmethod
    async def query_dict_data_list_from_cache_services(cls, redis, dict_type: str):
        """
        从缓存获取字典数据列表信息service

        :param redis: redis对象
        :param dict_type: 字典类型
        :return: 字典数据列表信息对象
        """
        result = []
        dict_data_list_result = await redis.get(f'{RedisInitKeyConfig.SYS_DICT.key}:{dict_type}')
        if dict_data_list_result:
            result = json.loads(dict_data_list_result)

        return SqlalchemyUtil.serialize_result(result)

    @classmethod
    async def check_dict_data_unique_services(cls, query_db: AsyncSession, page_object: DictDataModel):
        """
        校验字典数据是否唯一service

        :param query_db: orm对象
        :param page_object: 字典数据对象
        :return: 校验结果
        """
        dict_code = -1 if page_object.dict_code is None else page_object.dict_code
        dict_data = await DictDataDao.get_dict_data_detail_by_info(query_db, page_object)
        if dict_data and dict_data.dict_code != dict_code:
            return CommonConstant.NOT_UNIQUE
        return CommonConstant.UNIQUE

    @classmethod
    async def add_dict_data_services(cls, request: Request, query_db: AsyncSession, page_object: DictDataModel):
        """
        新增字典数据信息service

        :param request: Request对象
        :param query_db: orm对象
        :param page_object: 新增岗位对象
        :return: 新增字典数据校验结果
        """
        if not await cls.check_dict_data_unique_services(query_db, page_object):
            raise ServiceException(
                message=f'新增字典数据{page_object.dict_label}失败，{page_object.dict_type}下已存在该字典数据'
            )
        else:
            try:
                await DictDataDao.add_dict_data_dao(query_db, page_object)
                await query_db.commit()
                dict_data_list = await cls.query_dict_data_list_services(query_db, page_object.dict_type)
                await request.app.state.redis.set(
                    f'{RedisInitKeyConfig.SYS_DICT.key}:{page_object.dict_type}',
                    json.dumps(
                        SqlalchemyUtil.serialize_result(dict_data_list), ensure_ascii=False, default=str
                    ),
                )
                return CrudResponseModel(is_success=True, message='新增成功')
            except Exception as e:
                await query_db.rollback()
                raise e

    @classmethod
    async def edit_dict_data_services(cls, request: Request, query_db: AsyncSession, page_object: DictDataModel):
        """
        编辑字典数据信息service

        :param request: Request对象
        :param query_db: orm对象
        :param page_object: 编辑字典数据对象
        :return: 编辑字典数据校验结果
        """
        edit_data_type = page_object.model_dump(exclude_unset=True)
        dict_data_info = await cls.dict_data_detail_services(query_db, page_object.dict_code)
        if dict_data_info.dict_code:
            if not await cls.check_dict_data_unique_services(query_db, page_object):
                raise ServiceException(
                    message=f'新增字典数据{page_object.dict_label}失败，{page_object.dict_type}下已存在该字典数据'
                )
            else:
                try:
                    await DictDataDao.edit_dict_data_dao(query_db, edit_data_type)
                    await query_db.commit()
                    dict_data_list = await cls.query_dict_data_list_services(query_db, page_object.dict_type)
                    await request.app.state.redis.set(
                        f'{RedisInitKeyConfig.SYS_DICT.key}:{page_object.dict_type}',
                        json.dumps(
                            SqlalchemyUtil.serialize_result(dict_data_list), ensure_ascii=False, default=str
                        ),
                    )
                    return CrudResponseModel(is_success=True, message='更新成功')
                except Exception as e:
                    await query_db.rollback()
                    raise e
        else:
            raise ServiceException(message='字典数据不存在')

    @classmethod
    async def delete_dict_data_services(
        cls, request: Request, query_db: AsyncSession, page_object: DeleteDictDataModel
    ):
        """
        删除字典数据信息service

        :param request: Request对象
        :param query_db: orm对象
        :param page_object: 删除字典数据对象
        :return: 删除字典数据校验结果
        """
        if page_object.dict_codes:
            dict_code_list = page_object.dict_codes.split(',')
            try:
                delete_dict_type_list = []
                for dict_code in dict_code_list:
                    dict_data = await cls.dict_data_detail_services(query_db, int(dict_code))
                    await DictDataDao.delete_dict_data_dao(query_db, DictDataModel(dict_code=dict_code))
                    delete_dict_type_list.append(dict_data.dict_type)
                await query_db.commit()
                for dict_type in list(set(delete_dict_type_list)):
                    dict_data_list = await cls.query_dict_data_list_services(query_db, dict_type)
                    await request.app.state.redis.set(
                        f'{RedisInitKeyConfig.SYS_DICT.key}:{dict_type}',
                        json.dumps(
                            SqlalchemyUtil.serialize_result(dict_data_list), ensure_ascii=False, default=str
                        ),
                    )
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入字典数据id为空')

    @classmethod
    async def dict_data_detail_services(cls, query_db: AsyncSession, dict_code: int):
        """
        获取字典数据详细信息service

        :param query_db: orm对象
        :param dict_code: 字典数据id
        :return: 字典数据id对应的信息
        """
        dict_data = await DictDataDao.get_dict_data_detail_by_id(query_db, dict_code=dict_code)
        if dict_data:
            result = DictDataModel(**SqlalchemyUtil.serialize_result(dict_data))
        else:
            result = DictDataModel(**dict())

        return result

    @staticmethod
    async def export_dict_data_list_services(dict_data_list: List):
        """
        导出字典数据信息service

        :param dict_data_list: 字典数据信息列表
        :return: 字典数据信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'dict_code': '字典编码',
            'dict_sort': '字典标签',
            'dict_label': '字典键值',
            'dict_value': '字典排序',
            'dict_type': '字典类型',
            'css_class': '样式属性',
            'list_class': '表格回显样式',
            'is_default': '是否默认',
            'status': '状态',
            'create_by': '创建者',
            'create_time': '创建时间',
            'update_by': '更新者',
            'update_time': '更新时间',
            'remark': '备注',
        }

        data = dict_data_list

        for item in data:
            if item.get('status') == '0':
                item['status'] = '正常'
            else:
                item['status'] = '停用'
            if item.get('is_default') == 'Y':
                item['is_default'] = '是'
            else:
                item['is_default'] = '否'
        new_data = [
            {mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in data
        ]
        binary_data = export_list2excel(new_data)

        return binary_data
