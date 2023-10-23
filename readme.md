### Login and password for local superuser: 
Login: admin <br/>
Pass: admin

### Making messages for translation
##### For the first time
```
django-admin makemessages -l=ru -l=en -i venv/* -i *.txt
```
##### When the directories locale/en,ru already exist
```
django-admin makemessages --all -i venv/* -i *.txt
```
##### Compile messages
```
django-admin compilemessages
```