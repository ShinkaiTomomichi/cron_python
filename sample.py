import numpy as np
import pathlib
import datetime

# 利用するディレクトリの絶対パス
OUTPUT_DIR_PATH = ''

if __name__ == "__main__":
    now = datetime.datetime.today()
    file_name = str(now.month) + '-' + str(now.day) + '-' + str(now.hour) + '-' + str(now.minute)

    file_maker = pathlib.Path(OUTPUT_DIR_PATH + file_name+'.txt')
    print(file_name)
    file_maker.touch()
