from module_admin.entity.vo.job_vo import *
from module_admin.dao.job_dao import *
from utils.common_util import export_list2excel
from config.get_scheduler import add_scheduler_job, remove_scheduler_job


class JobService:
    """
    定时任务管理模块服务层
    """

    @classmethod
    def get_job_list_services(cls, result_db: Session, query_object: JobModel):
        """
        获取定时任务列表信息service
        :param result_db: orm对象
        :param query_object: 查询参数对象
        :return: 定时任务列表信息对象
        """
        job_list_result = get_job_list(result_db, query_object)

        return job_list_result

    @classmethod
    def add_job_services(cls, result_db: Session, page_object: JobModel):
        """
        新增定时任务信息service
        :param result_db: orm对象
        :param page_object: 新增定时任务对象
        :return: 新增定时任务校验结果
        """
        add_job_result = add_job_dao(result_db, page_object)

        return add_job_result

    @classmethod
    def edit_job_services(cls, result_db: Session, page_object: JobModel):
        """
        编辑定时任务信息service
        :param result_db: orm对象
        :param page_object: 编辑定时任务对象
        :return: 编辑定时任务校验结果
        """
        edit_job = page_object.dict(exclude_unset=True)
        edit_job_result = edit_job_dao(result_db, edit_job)
        if edit_job.get('status') == '0':
            job_info = cls.detail_job_services(result_db, edit_job.get('job_id'))
            try:
                remove_scheduler_job(job_id=edit_job.get('job_id'))
            except Exception as e:
                print(e)
            finally:
                add_scheduler_job(job_info=job_info)
        if edit_job.get('status') == '1':
            try:
                remove_scheduler_job(job_id=edit_job.get('job_id'))
            except Exception as e:
                print(e)
            finally:
                print('')

        return edit_job_result

    @classmethod
    def delete_job_services(cls, result_db: Session, page_object: DeleteJobModel):
        """
        删除定时任务信息service
        :param result_db: orm对象
        :param page_object: 删除定时任务对象
        :return: 删除定时任务校验结果
        """
        if page_object.job_ids.split(','):
            job_id_list = page_object.job_ids.split(',')
            for job_id in job_id_list:
                job_id_dict = dict(job_id=job_id)
                delete_job_dao(result_db, JobModel(**job_id_dict))
            result = dict(is_success=True, message='删除成功')
        else:
            result = dict(is_success=False, message='传入定时任务id为空')
        return CrudJobResponse(**result)

    @classmethod
    def detail_job_services(cls, result_db: Session, job_id: int):
        """
        获取定时任务详细信息service
        :param result_db: orm对象
        :param job_id: 定时任务id
        :return: 定时任务id对应的信息
        """
        job = get_job_detail_by_id(result_db, job_id=job_id)

        return job

    @staticmethod
    def export_job_list_services(job_list: List):
        """
        导出定时任务信息service
        :param job_list: 定时任务信息列表
        :return: 定时任务信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            "job_id": "任务编码",
            "job_name": "任务名称",
            "job_group": "任务组名",
            "invoke_target": "调用目标字符串",
            "cron_expression": "cron执行表达式",
            "misfire_policy": "计划执行错误策略",
            "concurrent": "是否并发执行",
            "status": "状态",
            "create_by": "创建者",
            "create_time": "创建时间",
            "update_by": "更新者",
            "update_time": "更新时间",
            "remark": "备注",
        }

        data = [JobModel(**vars(row)).dict() for row in job_list]

        for item in data:
            if item.get('status') == '0':
                item['status'] = '正常'
            else:
                item['status'] = '暂停'
            if item.get('job_group') == 'SYSTEM':
                item['job_group'] = '系统'
            else:
                item['job_group'] = '默认'
            if item.get('misfire_policy') == '1':
                item['misfire_policy'] = '立即执行'
            elif item.get('misfire_policy') == '2':
                item['misfire_policy'] = '执行一次'
            else:
                item['misfire_policy'] = '放弃执行'
            if item.get('concurrent') == '0':
                item['concurrent'] = '允许'
            else:
                item['concurrent'] = '禁止'
        new_data = [{mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in data]
        binary_data = export_list2excel(new_data)

        return binary_data
