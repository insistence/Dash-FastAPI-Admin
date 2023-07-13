from pydantic import BaseModel
from typing import Union, Optional, List


class DictTypeModel(BaseModel):
    """
    字典类型表对应pydantic模型
    """
    dict_id: Optional[int]
    dict_name: Optional[str]
    dict_type: Optional[str]
    status: Optional[str]
    create_by: Optional[str]
    create_time: Optional[str]
    update_by: Optional[str]
    update_time: Optional[str]
    remark: Optional[str]

    class Config:
        orm_mode = True


class DictDataModel(BaseModel):
    """
    字典数据表对应pydantic模型
    """
    dict_code: Optional[int]
    dict_sort: Optional[int]
    dict_label: Optional[str]
    dict_value: Optional[str]
    dict_type: Optional[str]
    css_class: Optional[str]
    list_class: Optional[str]
    is_default: Optional[str]
    status: Optional[str]
    create_by: Optional[str]
    create_time: Optional[str]
    update_by: Optional[str]
    update_time: Optional[str]
    remark: Optional[str]

    class Config:
        orm_mode = True


class DictTypePageObject(DictTypeModel):
    """
    字典类型管理分页查询模型
    """
    create_time_start: Optional[str]
    create_time_end: Optional[str]
    page_num: Optional[int]
    page_size: Optional[int]


class DictTypePageObjectResponse(BaseModel):
    """
    字典类型管理列表分页查询返回模型
    """
    rows: List[Union[DictTypeModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class DeleteDictTypeModel(BaseModel):
    """
    删除字典类型模型
    """
    dict_ids: str


class DictDataPageObject(DictDataModel):
    """
    字典数据管理分页查询模型
    """
    page_num: Optional[int]
    page_size: Optional[int]


class DictDataPageObjectResponse(BaseModel):
    """
    字典数据管理列表分页查询返回模型
    """
    rows: List[Union[DictDataModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class DeleteDictDataModel(BaseModel):
    """
    删除字典数据模型
    """
    dict_codes: str


class CrudDictResponse(BaseModel):
    """
    操作字典响应模型
    """
    is_success: bool
    message: str
