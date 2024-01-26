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
##### Complaints post_save sms delivery
In the list of settings /admin/app_settings/appsettings/
it's necessary to create setting with key complaints_telephones_list
and the list of telephone numbers for sms sending when Complaint and
suggestion is created.

##### Push notifications
For push notifications it's necessary place file firebase_private_key.json in ./project
directory. The content of this file is generated on Firebase 
https://console.firebase.google.com/u/0/project/vitalii-fecf8/settings/serviceaccounts/adminsdk