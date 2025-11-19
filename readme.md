




docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=app \
    -e POSTGRES_PASSWORD=BWsBWEHUpSB7 \
    -e POSTGRES_DB=booking \
    --network mynetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16


docker run --name booking_cache \
    -p 7379:6379 \
    --network mynetwork \
    -d redis 


docker run --name booking_fast_api \
    -p 8001:8000 \
    --network mynetwork \
    booking_back


docker run --name booking_celery_worker \
    --network mynetwork \
    booking_back \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_celery_beat \
    --network mynetwork \
    booking_back \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B
    