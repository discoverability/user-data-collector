FLASK_APP="sniffer_api.py"
rm -rf migrations 
rm -rf app/app.db
flask db init
flask db migrate
flask db upgrade

flask run --host=0.0.0.0 --port=5000
