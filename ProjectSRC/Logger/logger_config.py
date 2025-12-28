import logging
import os
from logging.handlers import RotatingFileHandler

# مسیر پوشه فعلی (همان جایی که logger_config.py قرار دارد)
current_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(current_dir, "app.log")

# ساخت Logger اصلی
logger = logging.getLogger("app_log")
logger.setLevel(logging.DEBUG)

# فرمت حرفه‌ای
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# هندلر برای کنسول
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# هندلر برای فایل با چرخش (در همان پوشه logger_config.py)
file_handler = RotatingFileHandler(
    log_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# جلوگیری از دوباره اضافه شدن هندلرها
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

logger.debug("Logger initialized, file handler active.")


# تست
# برای استفاده تنها کافیست این خط را بنویسی
# from logger_config import logger
# logger.debug("this is debug log!")
# logger.info("this is info log!")
# logger.warning("this is warning log!")
# logger.error("this is error log!")
# logger.critical("this is critical log!")
