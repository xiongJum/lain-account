import sys, os, copy
sys.path.append(os.getcwd())

from openpyxl import load_workbook
import datetime, time
import pandas
import uuid

from config import Common
from my_sqlite3 import Db


class OpenFile():

    def __init__(self) -> None:
        # self.my_class = my_class
        self.database = self.config.DATABASE
        self.must_database = self.config.MUST_DATABASE
        # 具有外键属性的列名,主要是连表查询
        self.foreign = Common.FOREIGN_KEY
        self.foreign_key = self.foreign.keys()
        self.foreign_value = self.foreign.values()
        # self.config_types = Common.FOREIGN_KEY.keys()
        self.id_name = self.database[0]
        self.empty = ['', 'null', 'None', None]
        self.db = Db('account.db')

    def open_file(self, filename=False):
        filename = filename if filename else self.filename

        # 读取 excel 表
        workbook = load_workbook(filename=filename)
        wb = workbook.active
        # 获取整张表数据
        table = [[cell.value for cell in row] for row in wb.rows]
        # 表标题 和 表内容
        table_values, table_cloumn  = table[1:], table[0]
        # 复制一份没有被转换id的表
        import_fail = copy.deepcopy(table_values)
        # 待删除列表
        del_rows = []
        # 获取配置列表
        configs = self.__conifg()
        # 格式化时间标识
        is_date, is_date_created = True, True
        try:
            date_index = table_cloumn.index('date')
        except KeyError:
            is_date = False
        try:
            date_created_index = table_cloumn.index('date_created')
        except KeyError:
            is_date_created = False
        
        for index, row in enumerate(table_values):
            # 获取所有需要转换为id的配置类型
            for config_type in self.foreign_key:
                # 获取配置所在列表下标位置
                row_index = table_cloumn.index(config_type)
                # 将配置名称替换为配置id
                for i, mapping in enumerate(configs[config_type]):
                    if mapping[1] == row[row_index]:
                        row[row_index]  = mapping[0]
                        break
                    # 将没有的配置id的行数加入到待删除列表中
                    if mapping[1] != row[row_index] and index not in del_rows and (i+1) == len(configs[config_type]):
                        del_rows.append(index)
            
            # 将必填项的空内容添加到待删除列表中
            for cloumn in self.must_database:
                row_index = table_cloumn.index(cloumn)
                if row[row_index] in self.empty:
                    del_rows.append(index)
                    continue

            # 将发生日期和创建日期转换为日期字符串
            if is_date:
                try:
                    row[date_index] = row[date_index].strftime('%Y-%m-%d')
                except ValueError as e:
                    print(e)
                except AttributeError:
                    try:
                        datetime.datetime.strptime(row[date_index], '%Y-%m-%d')
                    except ValueError:
                        del_rows.append(index)
                    except TypeError:
                        del_rows.append(index)
            
            if is_date_created:
                try:
                    row[date_created_index] = row[date_created_index].strftime('%Y-%m-%d %H:%M:%S')
                except ValueError as e:
                    print(e)
                except AttributeError as e:
                    try:
                        datetime.datetime.strptime(row[date_created_index], '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        row[date_created_index] = time.strftime('%Y-%m-%d %H:%M:%S')

            id_index = table_cloumn.index(self.id_name)
            if row[id_index] in self.empty:
                row[id_index] = str(uuid.uuid4())
            else:
                if self.find(id=row[row_index]): del_rows.append(index)

        # 去重
        del_rows = list(set(del_rows))
        # 删除部分行数,内容不和规定的
        table = [row for index, row in  enumerate(table_values) if index not in del_rows]

        # 进行导入
        self.__upload(table_cloumn, table)
        # 打印导入失败的表单
        self.__print_fail_table(import_fail, table_cloumn, del_rows)


    def __conifg(self):
        from main.config import Config
        import pandas
        # 获取配置表
        config = Config().find()
        config = pandas.DataFrame(config)
        # 将配置表转变为字典 key 为配置类型 如 books

        def __config_value(config_key):
            # 将相同类型的列表结合在一起
            return [config.loc[index].values[0:2] for index in config.index if config.loc[index].values[2] == config_key]

        configs = {config.loc[index].values[2]: __config_value(config.loc[index].values[2]) for index in config.index}

        return configs
    
    def __upload(self, cloumns, values):

        cloumns = ', '.join(cloumns)

        values = '),('.join([str(row)[1:-1] for row in values])
        values =  values.replace("'null',", 'null,').replace(", 'null'", ', null')   
        values =  values.replace("None", 'null')     
        sql = f"INSERT INTO {self.table} ({cloumns}) VALUES ({values});"
        print(sql)
        self.db.other(sql)

    def __print_fail_table(self, import_fail, table_cloumn, del_rows):

        # 打印和展示导入失败的表
        if del_rows:
            is_import = input("存在导入失败的行数,是否进行导出? y/N: ")
            import_fail_table = [t for i, t in enumerate(import_fail) if i in del_rows]
            import_fail_table = pandas.DataFrame(import_fail_table, columns=table_cloumn)
            if is_import.upper() == 'Y':
                try:
                    import_fail_table.to_excel(f'fial_账单表.xlsx', index=False)
                    print(f"导出成功 \n {import_fail_table}")
                except Exception:
                    print("导出失败")