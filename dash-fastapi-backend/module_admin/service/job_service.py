from module_admin.entity.vo.job_vo import *
from module_admin.dao.job_dao import *
from module_admin.service.dict_service import Request, DictDataService
from utils.common_util import export_list2excel
from config.get_scheduler import SchedulerUtil


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
        job_list_result = JobDao.get_job_list(result_db, query_object)

        return job_list_result

    @classmethod
    def add_job_services(cls, result_db: Session, page_object: JobModel):
        """
        新增定时任务信息service
        :param result_db: orm对象
        :param page_object: 新增定时任务对象
        :return: 新增定时任务校验结果
        """
        job = JobDao.get_job_detail_by_info(result_db, page_object)
        if job:
            result = dict(is_success=False, message='定时任务已存在')
        else:
            try:
                JobDao.add_job_dao(result_db, page_object)
                job_info = JobDao.get_job_detail_by_info(result_db, page_object)
                if job_info.status == '0':
                    SchedulerUtil.add_scheduler_job(job_info=job_info)
                result_db.commit()
                result = dict(is_success=True, message='新增成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))

        return CrudJobResponse(**result)

    @classmethod
    def edit_job_services(cls, result_db: Session, page_object: EditJobModel):
        """
        编辑定时任务信息service
        :param result_db: orm对象
        :param page_object: 编辑定时任务对象
        :return: 编辑定时任务校验结果
        """
        edit_job = page_object.dict(exclude_unset=True)
        if page_object.type == 'status':
            del edit_job['type']
        job_info = cls.detail_job_services(result_db, edit_job.get('job_id'))
        if job_info:
            if page_object.type != 'status' and (job_info.job_name != page_object.job_name or job_info.job_group != page_object.job_group or job_info.invoke_target != page_object.invoke_target or job_info.cron_expression != page_object.cron_expression):
                job = JobDao.get_job_detail_by_info(result_db, page_object)
                if job:
                    result = dict(is_success=False, message='定时任务已存在')
                    return CrudJobResponse(**result)
            try:
                JobDao.edit_job_dao(result_db, edit_job)
                query_job = SchedulerUtil.get_scheduler_job(job_id=edit_job.get('job_id'))
                if query_job:
                    SchedulerUtil.remove_scheduler_job(job_id=edit_job.get('job_id'))
                if edit_job.get('status') == '0':
                    SchedulerUtil.add_scheduler_job(job_info=job_info)
                result_db.commit()
                result = dict(is_success=True, message='更新成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='定时任务不存在')

        return CrudJobResponse(**result)

    @classmethod
    def execute_job_once_services(cls, result_db: Session, page_object: JobModel):
        """
        执行一次定时任务service
        :param result_db: orm对象
        :param page_object: 定时任务对象
        :return: 执行一次定时任务结果
        """
        query_job = SchedulerUtil.get_scheduler_job(job_id=page_object.job_id)
        if query_job:
            SchedulerUtil.remove_scheduler_job(job_id=page_object.job_id)
        job_info = cls.detail_job_services(result_db, page_object.job_id)
        if job_info:
            SchedulerUtil.execute_scheduler_job_once(job_info=job_info)
            result = dict(is_success=True, message='执行成功')
        else:
            result = dict(is_success=False, message='定时任务不存在')

        return CrudJobResponse(**result)

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
            try:
                for job_id in job_id_list:
                    job_id_dict = dict(job_id=job_id)
                    JobDao.delete_job_dao(result_db, JobModel(**job_id_dict))
                result_db.commit()
                result = dict(is_success=True, message='删除成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
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
        job = JobDao.get_job_detail_by_id(result_db, job_id=job_id)

        return job

    @staticmethod
    async def export_job_list_services(request: Request, job_list: List):
        """
        导出定时任务信息service
        :param request: Request对象
        :param job_list: 定时任务信息列表
        :return: 定时任务信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            "job_id": "任务编码",
            "job_name": "任务名称",
            "job_group": "任务组名",
            "job_executor": "任务执行器",
            "invoke_target": "调用目标字符串",
            "job_args": "位置参数",
            "job_kwargs": "关键字参数",
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
        job_group_list = await DictDataService.query_dict_data_list_from_cache_services(request.app.state.redis, dict_type='sys_job_group')
        job_group_option = [dict(label=item.dict_label, value=item.dict_value) for item in job_group_list]
        job_group_option_dict = {item.get('value'): item for item in job_group_option}

        for item in data:
            if item.get('status') == '0':
                item['status'] = '正常'
            else:
                item['status'] = '暂停'
            if str(item.get('job_group')) in job_group_option_dict.keys():
                item['job_group'] = job_group_option_dict.get(str(item.get('job_group'))).get('label')
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
