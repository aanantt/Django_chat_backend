# Chat App - Backend (Django)
### Clone the project

```
git clone https://github.com/aanantt/Django_chat_backend.git
python -m venv venv
source venv/bin/activate
cd Django_chat_backend
pip install -r requirements.txt
```

### Run Migrations
```
python manage.py makemigrations
python manage.py migrate
```
### Run the Project
```
sudo docker run -p 6379:6379 -d redis:5
python manage.py runserver 0.0.0.0:8000
```
Then run the [Flutter Code](https://github.com/aanantt/flutter_chat_frontend) and use the Application :)

### What's Next??
1. Sending and receiving Media Files
2. Personalized Chat list
3. And many more new features...

### Screenshots:
![](https://i.ibb.co/P9GdqkL/Screenshot-from-2021-06-04-20-46-12.png)

![](https://i.ibb.co/5F7Sf79/Screenshot-from-2021-06-04-20-49-53.png)