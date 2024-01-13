#!/bin/sh

echo "Ожидание запуска базы данных..."
sleep 10

echo "Инициализация базы данных..."
python init_db.py

exec python app.py
