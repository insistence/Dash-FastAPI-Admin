from utils.request import api_request


def get_job_list_api(page_obj: dict):

    return api_request(method='post', url='/monitor/job/get', is_headers=True, json=page_obj)


def add_job_api(page_obj: dict):

    return api_request(method='post', url='/monitor/job/add', is_headers=True, json=page_obj)


def edit_job_api(page_obj: dict):

    return api_request(method='patch', url='/monitor/job/edit', is_headers=True, json=page_obj)


def delete_job_api(page_obj: dict):

    return api_request(method='post', url='/monitor/job/delete', is_headers=True, json=page_obj)


def get_job_detail_api(job_id: int):

    return api_request(method='get', url=f'/monitor/job/{job_id}', is_headers=True)


def export_job_list_api(page_obj: dict):

    return api_request(method='post', url='/monitor/job/export', is_headers=True, json=page_obj, stream=True)
