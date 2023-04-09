import pandas, json, datetime
from config import Common


class Upload():

    def __init__(self, main_class, main_confg) -> None:
        self.main_class = main_class
        self.file_path = Common.FILE_PATH
        self.file_name = main_confg.FILE_NAME

    def upload_account(self, file_name=False, file_path=False):

        # 拼接导出路径
        file_path = file_path if file_path else self.file_path
        file_name = file_name if file_name else self.file_name
        file_name = file_path + file_name

        # 使用 pandas 读取文件
        pf = pandas.read_excel(file_name, index_col=False)
        # 获取文件数据
        ## 获取行数,并生成相同数量的空列表
        row = pf.last_valid_index()
        if not row: exit('请添加文件后进行导入')
        # 将时间或则日期格式化为字符串
        if 'date' in pf:
                if type(pf['date']) != str:
                    pf['date'] = pf['date'].dt.strftime('%Y-%m-%d')
        if 'date_created' in pf:
                if pf['date_created'].empty:
                    pf['date_created'] = pf['date_created'].dt.strftime('%Y-%m-%d %H:%M:%S')
        import_data = [list() for i in range(row+1)]
        # 将读取的数据,从json转换为列表
        read_csv = json.loads(pf.to_json())
        read_csv_values = read_csv.values()
        read_csv_keys  = list(read_csv.keys())

        for values in read_csv_values:
            for index, value in values.items():
                index, value = int(index), str(value)
                import_data[index].append(value)
        
        self.main_class._import(read_csv_keys, import_data)