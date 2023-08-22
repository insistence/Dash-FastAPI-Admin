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
        dict_type_list_result = get_dict_type_list(result_db, query_object)

        return dict_type_list_result

    @classmethod
    def get_all_dict_type_services(cls, result_db: Session):
        """
        获取字所有典类型列表信息service
        :param result_db: orm对象
        :return: 字典类型列表信息对象
        """
        dict_type_list_result = get_all_dict_type(result_db)

        return dict_type_list_result

    @classmethod
    def add_dict_type_services(cls, result_db: Session, page_object: DictTypeModel):
        """
        新增字典类型信息service
        :param result_db: orm对象
        :param page_object: 新增岗位对象
        :return: 新增字典类型校验结果
        """
        add_dict_type_result = add_dict_type_dao(result_db, page_object)

        return add_dict_type_result

    @classmethod
    def edit_dict_type_services(cls, result_db: Session, page_object: DictTypeModel):
        """
        编辑字典类型信息service
        :param result_db: orm对象
        :param page_object: 编辑字典类型对象
        :return: 编辑字典类型校验结果
        """
        edit_dict_type = page_object.dict(exclude_unset=True)
        edit_dict_type_result = edit_dict_type_dao(result_db, edit_dict_type)

        return edit_dict_type_result

    @classmethod
    def delete_dict_type_services(cls, result_db: Session, page_object: DeleteDictTypeModel):
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

    @classmethod
    def detail_dict_type_services(cls, result_db: Session, dict_id: int):
        """
        获取字典类型详细信息service
        :param result_db: orm对象
        :param dict_id: 字典类型id
        :return: 字典类型id对应的信息
        """
        dict_type = get_dict_type_detail_by_id(result_db, dict_id=dict_id)

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
        dict_data_list_result = get_dict_data_list(result_db, query_object)

        return dict_data_list_result

    @classmethod
    def query_dict_data_list_services(cls, result_db: Session, dict_type: str):
        """
        获取字典数据列表信息service
        :param result_db: orm对象
        :param dict_type: 字典类型
        :return: 字典数据列表信息对象
        """
        dict_data_list_result = query_dict_data_list(result_db, dict_type)

        return dict_data_list_result

    @classmethod
    def add_dict_data_services(cls, result_db: Session, page_object: DictDataModel):
        """
        新增字典数据信息service
        :param result_db: orm对象
        :param page_object: 新增岗位对象
        :return: 新增字典数据校验结果
        """
        add_dict_data_result = add_dict_data_dao(result_db, page_object)

        return add_dict_data_result

    @classmethod
    def edit_dict_data_services(cls, result_db: Session, page_object: DictDataModel):
        """
        编辑字典数据信息service
        :param result_db: orm对象
        :param page_object: 编辑字典数据对象
        :return: 编辑字典数据校验结果
        """
        edit_data_type = page_object.dict(exclude_unset=True)
        edit_dict_data_result = edit_dict_data_dao(result_db, edit_data_type)

        return edit_dict_data_result

    @classmethod
    def delete_dict_data_services(cls, result_db: Session, page_object: DeleteDictDataModel):
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

    @classmethod
    def detail_dict_data_services(cls, result_db: Session, dict_code: int):
        """
        获取字典数据详细信息service
        :param result_db: orm对象
        :param dict_code: 字典数据id
        :return: 字典数据id对应的信息
        """
        dict_data = get_dict_data_detail_by_id(result_db, dict_code=dict_code)

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
