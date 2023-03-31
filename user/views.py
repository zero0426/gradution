from user.system import data_process
from user import upload_daily_info

data_process.train('510050', 4000, 10)
upload_daily_info.upload()