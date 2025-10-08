import asyncio
from time import sleep
from src.tasks.celery_app import celery_instance
import os
from PIL import Image
from src.database import async_session_maker_null_pool

from src.utils.db_manager import DBManager


@celery_instance.task
def test_task():
    sleep(5)
    print("TASK IS DONE YEAH!")


@celery_instance.task
def resize_image(image_path: str):
    output_dir = 'src/static/images'
    # Загружаем оригинальное изображение
    img = Image.open(image_path)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Определяем размеры, которые нужно сделать
    sizes = [10000, 500, 200]

    for width in sizes:
        # Вычисляем высоту с сохранением пропорций
        ratio = width / img.width
        height = int(img.height * ratio)
        resized_img = img.resize((width, height), Image.Resampling.LANCZOS)

        # Формируем имя файла
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        new_filename = f"{base_name}_{width}px.jpg"
        save_path = os.path.join(output_dir, new_filename)

        # Сохраняем результат
        resized_img.save(save_path, "JPEG", quality=90)
        print(f"✅ Сохранено: {save_path}")
    print(f"Images saved in sizes: {sizes} in folder {output_dir}")


async def get_today_checkin_users_helper():
    print("I STARTED")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        res = await db.bookings.get_booking_with_today_checkin()
        print(f"today will book {res}")


@celery_instance.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    print('I am here')
    asyncio.run(get_today_checkin_users_helper())
