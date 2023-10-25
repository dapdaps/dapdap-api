# Pthon 3.10 + 
# dapdap-api

# Start script
web
```shell
uvicorn main:app --host 0.0.0.0 --port 8101
```

celery
more see run_celery.sh
```shell
celery multi start -A core.celery_app  worker --loglevel=info --logfile=logs/celery.log
celery -A core.celery_app flower --port=5555 --basic-auth="user1:password1,user2:password2"
celery -A core.celery_app beat --loglevel=info --logfile=logs/celery-beat.log
```