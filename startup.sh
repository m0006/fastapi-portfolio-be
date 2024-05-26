alembic -c taxi_movement/alembic.ini upgrade head
python load_data.py
uvicorn main:app --host 0.0.0.0 --port 10000
