# ciciot_backend

## Pre Install

环境要求
* python 3.6
* MySQL 5.7

```shell
$ pip  install -r requirements.txt
```


## Run Production

```shell
$ export EMAIL_HOST='smtp.exmail.qq.com'
  export EMAIL_PORT=25
  export EMAIL_HOST_USER='**@fly-over.com.cn'
  export EMAIL_HOST_PASSWORD='*****'
  export EMAIL_FROM='***@fly-over.com.cn'
  export DATABASE_URL='*****'
  export GEETEST_ID='*****'
  export GEETEST_KEY='*******'
  export DJANGO_ENV='PRODUCTION'

$ python manage.py collectstatic

$ uwsgi -ini deploy/uwsgi.ini

$ ln -sv ${PWD}/deploy/ciciot_backend.conf /etc/nginx/conf.d/

$ systemctl start nginx
```
