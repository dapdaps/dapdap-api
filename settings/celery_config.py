# @Time : 10/18/23 11:35 AM
# @Author : HanyuLiu/Rainman
# @Email : rainman@ref.finance
# @File : celery_config.py

accept_content = ['json']
enable_utc = False
task_serializer = 'json'
timezone = 'UTC'
task_track_started = True
worker_hijack_root_logger = False
worker_redirect_stdouts_level = 'ERROR'
result_expires = 60 * 60 * 24