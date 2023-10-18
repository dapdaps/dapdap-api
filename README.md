# Pthon 3.10 + 
# dapdap-api

# Start script
web
```shell
uvicorn main:app --host 0.0.0.0 --port 8101
```

celery
```shell
celery -A core.celery_app  worker --loglevel=info --logfile=logs/celery.log
celery -A core.celery_app flower --port=5555
celery -A core.celery_app beat --loglevel=info --logfile=logs/celery-beat.log
```