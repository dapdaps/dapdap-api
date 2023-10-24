# Pthon 3.10 + 
# dapdap-api

# Start script
web
```shell
uvicorn main:app --host 0.0.0.0 --port 8101
```

celery
```shell
export DATABASE_HOST=;export DATABASE_NAME=;export DATABASE_USERNAME=;export DATABASE_PASSWORD=;
celery -A core.celery_app  worker --loglevel=info --logfile=logs/celery.log
celery -A core.celery_app flower --port=5555 --basic-auth="user1:password1,user2:password2"
celery -A core.celery_app beat --loglevel=info --logfile=logs/celery-beat.log
```