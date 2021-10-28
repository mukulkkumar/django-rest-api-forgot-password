# Django Rest Framework - Forgot password API

This repository is all about the forgot password API in django restframework

I have configured other details, you just need to configure these two variables in settings.py file

```
EMAIL_HOST_USER = '********@gmail.com'
EMAIL_HOST_PASSWORD = '**********'
```

I have used it for gmail, so you have to turn on the 'Allow less secure apps' feature in your gmail account configuration.

You can also use my docker hub repository, just pull the image and update above mentioned settings.py variables. I haven't set the environment variables for that :)

```
docker pull kumarm5/django-forgot-password
```
