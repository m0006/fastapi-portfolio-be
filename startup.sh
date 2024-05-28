alembic -c taximovement/alembic.ini upgrade head
alembic -c mahousing/alembic.ini upgrade head

python load_taxi_data.py
python load_housing_data.py

uvicorn main:app --host 0.0.0.0 --port 10000
