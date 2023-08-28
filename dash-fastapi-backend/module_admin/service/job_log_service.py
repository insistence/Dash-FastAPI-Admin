from module_admin.entity.vo.job_vo import *
from module_admin.dao.job_log_dao import *
from module_admin.dao.dict_dao import DictDataDao
from utils.common_util import export_list2excel


class JobLogService:
    """
    定时任务日志管理模块服务层
    """

    @classmethod
    def get_job_log_list_services(cls, result_db: Session, query_object: JobLogQueryModel):
        """
        获取定时任务日志列表信息service
        :param result_db: orm对象
        :param query_object: 查询参数对象
        :return: 定时任务日志列表信息对象
        """
        job_log_list_result = JobLogDao.get_job_log_list(result_db, query_object)

        return job_log_list_result

    @classmethod
    def add_job_log_services(cls, result_db: Session, page_object: JobLogModel):
        """
        新增定时任务日志信息service
        :param result_db: orm对象
        :param page_object: 新增定时任务日志对象
        :return: 新增定时任务日志校验结果
        """
        try:
            JobLogDao.add_job_log_dao(result_db, page_object)
            result_db.commit()
            result = dict(is_success=True, message='新增成功')
        except Exception as e:
            result_db.rollback()
            result = dict(is_success=False, message=str(e))

        return CrudJobResponse(**result)

    @classmethod
    def delete_job_log_services(cls, result_db: Session, page_object: DeleteJobLogModel):
        """
        删除定时任务日志信息service
        :param result_db: orm对象
        :param page_object: 删除定时任务日志对象
        :return: 删除定时任务日志校验结果
        """
        if page_object.job_log_ids.split(','):
            job_log_id_list = page_object.job_log_ids.split(',')
            try:
                for job_log_id in job_log_id_list:
                    job_log_id_dict = dict(job_log_id=job_log_id)
                    JobLogDao.delete_job_log_dao(result_db, JobLogModel(**job_log_id_dict))
                result_db.commit()
                result = dict(is_success=True, message='删除成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='传入定时任务日志id为空')
        return CrudJobResponse(**result)

    @classmethod
    def detail_job_log_services(cls, result_db: Session, job_log_id: int):
        """
        获取定时任务日志详细信息service
        :param result_db: orm对象
        :param job_log_id: 定时任务日志id
        :return: 定时任务日志id对应的信息
        """
        job_log = JobLogDao.get_job_log_detail_by_id(result_db, job_log_id=job_log_id)

        return job_log

    @classmethod
    def clear_job_log_services(cls, result_db: Session, page_object: ClearJobLogModel):
        """
        清除定时任务日志信息service
        :param result_db: orm对象
        :param page_object: 清除定时任务日志对象
        :return: 清除定时任务日志校验结果
        """
        if page_object.oper_type == 'clear':
            try:
                JobLogDao.clear_job_log_dao(result_db)
                result_db.commit()
                result = dict(is_success=True, message='清除成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='清除标识不合法')

        return CrudJobResponse(**result)

    @staticmethod
    def export_job_log_list_services(result_db, job_log_list: List):
        """
        导出定时任务日志信息service
        :param result_db: orm对象
        :param job_log_list: 定时任务日志信息列表
        :return: 定时任务日志信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            "job_log_id": "任务日志编码",
            "job_name": "任务名称",
            "job_group": "任务组名",
            "job_executor": "任务执行器",
            "invoke_target": "调用目标字符串",
            "job_args": "位置参数",
            "job_kwargs": "关键字参数",
            "job_trigger": "任务触发器",
            "job_message": "日志信息",
            "status": "执行状态",
            "exception_info": "异常信息",
            "create_time": "创建时间",
        }

        data = [JobLogModel(**vars(row)).dict() for row in job_log_list]
        job_group_list = DictDataDao.query_dict_data_list(result_db, dict_type='sys_job_group')
        job_group_option = [dict(label=item.dict_label, value=item.dict_value) for item in job_group_list]
        job_group_option_dict = {item.get('value'): item for item in job_group_option}

        for item in data:
            if item.get('status') == '0':
                item['status'] = '正常'
            else:
                item['status'] = '暂停'
            if str(item.get('job_group')) in job_group_option_dict.keys():
                item['job_group'] = job_group_option_dict.get(str(item.get('job_group'))).get('label')
        new_data = [{mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in
                    data]
        binary_data = export_list2excel(new_data)

        return binary_data
