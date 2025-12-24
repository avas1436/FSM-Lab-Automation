import logging
from logging.handlers import RotatingFileHandler

# ساخت Logger اصلی
logger = logging.getLogger("app_log")
logger.setLevel(logging.DEBUG)  # سطح کلی

# فرمت حرفه‌ای
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# هندلر برای کنسول
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# هندلر برای فایل با چرخش
# هر لاگ حداکثر 5 مگابایت حجم خواهد داشت و پس از ساخت چهار فایل اولی حذف خواهد شد
file_handler = RotatingFileHandler(
    "app.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# اضافه کردن هندلرها
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# تست
# برای استفاده تنها کافیست این خط را بنویسی
# from logger_config import logger
# logger.debug("this is debug log!")
# logger.info("this is info log!")
# logger.warning("this is warning log!")
# logger.error("this is error log!")
# logger.critical("this is critical log!")
