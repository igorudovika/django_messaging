#### Implementation details
1. Backend: Django + Django Rest/
2. Frontend: Angular 1
3. Web socket: Django channels was used to refresh all connected users screens in case of Messages model changes.
This point needs additional work to refresh screens of sender and receiver only and not all connected users
4. Only dev environment was configured/tested. SQLLite as database and Django dev server. 

#### Installation
1. Create virtual env if needed
2. Install requirements:
```
pip install -r requirements.txt
```

#### Start application
```
python3 manage.py runserver
```

#### Work
1. Open http://localhost:8000 url in browser. Hoping work procedure is clear from UI.
2. Database instance is in repo.
Second user: sender2, password: sender2Message.
3. To add more users, please use Django admin panel: http://localhost:8000/admin
4. If you prefer to work with clear env, just delete database file and rerun migrations.



