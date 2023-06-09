import sys, os
sys.path.append(os.getcwd())
import uuid, copy
from config import Common
from my_sqlite3 import Db
from error import my_exception
import sqlite3
import numpy as np

# 获取当前类名 self.__class__.__name__
# 获取当前方法名  sys._getframe().f_code.co_name

class Main():

    def __init__(self) -> None:
        self.db = Db('account.db')
        # self.table = None
        # self.config = None
        # self.join_str = None
        # 数据库字段
        self.database = self.config.DATABASE
        # 将字段映射为中文,在使用时可以使用中文代替英文列
        self.database_zh = self.config.DATABASE_ZH
        self.config_table = "config"
        # 表id名称
        self.id_name = self.database[0]
        # 连表的部分SQL语句
        self.join_table_cloumn = self.config.JOIN_TABLE_CLOUMN
        # 具有外键属性的列名,主要是连表查询
        self.foreign = Common.FOREIGN_KEY
        self.foreign_key = self.foreign.keys()
        self.foreign_value = self.foreign.values()
        # 浮点型的列名
        self.float_cloumn = Common.FLOAT_CLOUMN
        # 不可修改的参数(数据库字段)
        self.prohibited_mod = Common.PROHIBITED_MOD
        self.empty = ['None', 'null', None, '', ' ', "'None'"] 

    def add(self, **kwargs):

        # 获取当前方法名,传入到校验方法和普通方法中去
        mode_name = sys._getframe().f_code.co_name
        kwargs = self.method_common(kwargs, mode_name=mode_name)
        kwargs = self.verify_common(kwargs, mode_name=mode_name)
        # 私有方法
        self.personal_verify(kwargs, mode_name=mode_name)        
        # 拼接 SQL 字符串,并进行
        ## 生成uuid
        kwargs[self.id_name] = uuid.uuid4()
        cloumns = ','.join(kwargs.keys())
        values = ','.join(value if key in self.float_cloumn else f"'{value}'" for key, value in kwargs.items())
        sql = f"INSERT INTO {self.table} ({cloumns}) VALUES ({values});"
        self.db.other(sql_str=sql)

    def find(self, is_mapping=False, *args, **kwargs):
        
        mode_name = sys._getframe().f_code.co_name
        kwargs = self.method_common(kwargs, mode_name=mode_name)

        # 设置当前列参数
        args  = args if args else self.database
        # 获取查询条件
        condition = ' and '.join(f"{key}='{value}'" for key, value in kwargs.items()) if kwargs else ';'
        # 是否需要进行映射
        if is_mapping:
            ## 替换列名称
            args_mapping = [self.join_table_cloumn[arg] if arg in self.join_table_cloumn.keys() else arg for arg in args]
            ## 将列表格式化为字符串
            cloumns = ', '.join(args_mapping)
            ## 是否需要添加条件
            if kwargs:
                sql = f"SELECT {cloumns} FROM {self.table} {self.join_str} " + ' WHERE ' + condition
            else:
                sql = f"SELECT {cloumns} FROM {self.table} {self.join_str}"

        else:
            cloumns = ', '.join(args)
            if kwargs:
                sql = sql = f"SELECT {cloumns} FROM {self.table}" + ' WHERE ' + condition
            else:
                sql = f"SELECT {cloumns} FROM {self.table}"

        if self.__class__.__name__ == 'Config':
            sql = sql + ' ORDER BY type'

        # print(sql)
        # 返回查询结果
        return self.db.cx(sql_str=sql)

    def remove(self, id):
        # 获取当前方法名称，并进行部分数据校验
        mode_name = sys._getframe().f_code.co_name
        self.personal_verify(id, mode_name=mode_name)
        # 提交SQL语句
        sql = f"DELETE FROM {self.table} WHERE {self.id_name} = '{id}';"
        # print(sql)
        self.db.other(sql_str=sql)

    def mod(self, id, **kwargs):
        
        # 获取当前方法名称，并进行部分数据校验
        mode_name = sys._getframe().f_code.co_name
        # 使用方法并进行校验数据
        kwargs = self.verify_common(self.method_common(kwargs, mode_name), mode_name=mode_name)
        # 拼接SQL字符串，并提交SQL语句
        mod_param = ', '.join([f"{key}='{value}'" for key, value in kwargs.items()])
        sql = f"UPDATE {self.table} SET {mod_param} WHERE {self.id_name} = '{id}'; "
        self.db.other(sql_str=sql)

    def personal_verify(self, param, mode_name):
        
        return param
    
    def verify_common(self, param:dict, mode_name):

        if mode_name in ['add', 'mod', 'find']:
            # 检查时间格式是否正确
            if 'date' in param.keys():
                import datetime
                from error.my_exception import DateIncorrect
                date_str = param['date']
                try:
                    datetime.datetime.strptime(date_str, "%Y-%m-%d")
                except:
                    raise DateIncorrect("时间不合规,请检查后重新输入")
        
        # 检查配置是否被禁用
        if mode_name in ['add', 'mod']:
            for key, value in param.items():
                if key in self.foreign_key:
                    sql = f"select is_flag FROM {self.config_table} WHERE config_id='{value}'"
                    is_flag =  self.db.cx(sql)
                    if is_flag == 1:
                        raise DateIncorrect("无效配置项,请先启用或者新增此配置")
                    
        if mode_name in ['add', '_import']:
            # 当添加的参数类型为中分类时,大分类不能为空
            if 'type' in param.keys():
                if param['type'] == 'scategory':
                    # print(param)
                    if 'bcategory' not in param.keys() or param['bcategory'] in self.empty:
                        raise my_exception.ParamAbsence("缺少必要的参数bcategory") 
        return param
    

    def method_common(self, param:dict, mode_name):
        
        def get_key(dict, value):
            return [k for k,v in dict.items() if v==value][0]
        
        if mode_name in ['mod']:
            # 删除不可修改的字段
            param = {key: value for key, value in param.items() if key not in self.prohibited_mod}

        if mode_name in ['find', 'mod']:
            # 将中文条件的key 转换为字母key
            import copy
            param_copy = copy.deepcopy(param)
            for p in param_copy.keys():
                if p not in self.database_zh.keys(): param[get_key(self.database_zh, p)] = param.pop(p)

        if mode_name in ['find', 'mod', 'add']:
            # 将配置的中文名称转换为配置id
            param = {key: self.__config_id(value, key) if key in self.foreign_key else value 
                                for key, value in param.items()}
            # 删除错误的参数
            param = {key: value for key, value in param.items() if key in self.database}

        return param
    

    def __config_id(self, config_name, config_type):
        """通过中文名称查找并返回配置ID"""
        sql = f"SELECT config_id FROM {self.config_table} WHERE config_name='{config_name}' and type='{config_type}'"
        return self.db.cx(sql_str=sql)
    
    def __config_name(self, config_id, config_type):
        """通过中文名称查找并返回配置ID"""
        sql = f"SELECT config_name FROM {self.config_table} WHERE config_name='{config_id}' and type='{config_type}'"
        return self.db.cx(sql_str=sql)