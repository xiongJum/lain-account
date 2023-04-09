import pandas
from config import Common

class DownLoad():

    def __init__(self, main_class, main_confg) -> None:
        self.main_class = main_class
        self.file_path = Common.FILE_PATH
        self.file_name = main_confg.FILE_NAME
        self.database = main_confg.DATABASE

    def download_account(self, condition:dict, file_path=False, file_name=False):

        # 获取路径
        file_path = file_path if file_path else self.file_path
        file_name = file_name if file_name else self.file_name
        file_name = file_path + file_name
        print(file_name)
        # 获取表数据
        tables = self.main_class.find(is_mapping=True, **condition)
        # 使用pandas 读取并进行导出 xlsx表
        pd = pandas.DataFrame(tables, columns=self.database)
        pd.to_excel(file_name, index=False)