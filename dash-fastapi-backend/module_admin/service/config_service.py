from fastapi import Request
from module_admin.entity.vo.config_vo import *
from module_admin.dao.config_dao import *
from utils.common_util import export_list2excel


class ConfigService:
    """
    参数配置管理模块服务层
    """

    @classmethod
    def get_config_list_services(cls, result_db: Session, query_object: ConfigQueryModel):
        """
        获取参数配置列表信息service
        :param result_db: orm对象
        :param query_object: 查询参数对象
        :return: 参数配置列表信息对象
        """
        config_list_result = ConfigDao.get_config_list(result_db, query_object)

        return config_list_result

    @classmethod
    async def init_cache_sys_config_services(cls, result_db: Session, redis):
        """
        应用初始化：获取所有参数配置对应的键值对信息并缓存service
        :param result_db: orm对象
        :param redis: redis对象
        :return:
        """
        # 获取以sys_config:开头的键列表
        keys = await redis.keys('sys_config:*')
        # 删除匹配的键
        if keys:
            await redis.delete(*keys)
        config_all = ConfigDao.get_config_list(result_db, ConfigQueryModel(**dict()))
        for config_obj in config_all:
            if config_obj.config_type == 'Y':
                await redis.set(f'sys_config:{config_obj.config_key}', config_obj.config_value)

    @classmethod
    async def query_config_list_from_cache_services(cls, redis, config_key: str):
        """
        从缓存获取参数键名对应值service
        :param redis: redis对象
        :param config_key: 参数键名
        :return: 参数键名对应值
        """
        result = await redis.get(f'sys_config:{config_key}')

        return result

    @classmethod
    async def add_config_services(cls, request: Request, result_db: Session, page_object: ConfigModel):
        """
        新增参数配置信息service
        :param request: Request对象
        :param result_db: orm对象
        :param page_object: 新增参数配置对象
        :return: 新增参数配置校验结果
        """
        config = ConfigDao.get_config_detail_by_info(result_db, ConfigModel(**dict(config_key=page_object.config_key)))
        if config:
            result = dict(is_success=False, message='参数键名已存在')
        else:
            try:
                ConfigDao.add_config_dao(result_db, page_object)
                result_db.commit()
                await cls.init_cache_sys_config_services(result_db, request.app.state.redis)
                result = dict(is_success=True, message='新增成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))

        return CrudConfigResponse(**result)

    @classmethod
    async def edit_config_services(cls, request: Request, result_db: Session, page_object: ConfigModel):
        """
        编辑参数配置信息service
        :param request: Request对象
        :param result_db: orm对象
        :param page_object: 编辑参数配置对象
        :return: 编辑参数配置校验结果
        """
        edit_config = page_object.dict(exclude_unset=True)
        config_info = cls.detail_config_services(result_db, edit_config.get('config_id'))
        if config_info:
            if config_info.config_key != page_object.config_key or config_info.config_value != page_object.config_value:
                config = ConfigDao.get_config_detail_by_info(result_db, page_object)
                if config:
                    result = dict(is_success=False, message='参数配置已存在')
                    return CrudConfigResponse(**result)
            try:
                ConfigDao.edit_config_dao(result_db, edit_config)
                result_db.commit()
                await cls.init_cache_sys_config_services(result_db, request.app.state.redis)
                result = dict(is_success=True, message='更新成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='参数配置不存在')

        return CrudConfigResponse(**result)

    @classmethod
    async def delete_config_services(cls, request: Request, result_db: Session, page_object: DeleteConfigModel):
        """
        删除参数配置信息service
        :param request: Request对象
        :param result_db: orm对象
        :param page_object: 删除参数配置对象
        :return: 删除参数配置校验结果
        """
        if page_object.config_ids.split(','):
            config_id_list = page_object.config_ids.split(',')
            try:
                for config_id in config_id_list:
                    config_id_dict = dict(config_id=config_id)
                    ConfigDao.delete_config_dao(result_db, ConfigModel(**config_id_dict))
                result_db.commit()
                await cls.init_cache_sys_config_services(result_db, request.app.state.redis)
                result = dict(is_success=True, message='删除成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='传入字典数据id为空')
        return CrudConfigResponse(**result)

    @classmethod
    def detail_config_services(cls, result_db: Session, config_id: int):
        """
        获取参数配置详细信息service
        :param result_db: orm对象
        :param config_id: 参数配置id
        :return: 参数配置id对应的信息
        """
        config = ConfigDao.get_config_detail_by_id(result_db, config_id=config_id)

        return config

    @staticmethod
    def export_config_list_services(config_list: List):
        """
        导出参数配置信息service
        :param config_list: 参数配置信息列表
        :return: 参数配置信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            "config_id": "参数主键",
            "config_name": "参数名称",
            "config_key": "参数键名",
            "config_value": "参数键值",
            "config_type": "系统内置",
            "create_by": "创建者",
            "create_time": "创建时间",
            "update_by": "更新者",
            "update_time": "更新时间",
            "remark": "备注",
        }

        data = [ConfigModel(**vars(row)).dict() for row in config_list]

        for item in data:
            if item.get('config_type') == 'Y':
                item['config_type'] = '是'
            else:
                item['config_type'] = '否'
        new_data = [{mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in data]
        binary_data = export_list2excel(new_data)

        return binary_data

    @classmethod
    async def refresh_sys_config_services(cls, request: Request, result_db: Session):
        """
        刷新字典缓存信息service
        :param request: Request对象
        :param result_db: orm对象
        :return: 刷新字典缓存校验结果
        """
        await cls.init_cache_sys_config_services(result_db, request.app.state.redis)
        result = dict(is_success=True, message='刷新成功')

        return CrudConfigResponse(**result)
