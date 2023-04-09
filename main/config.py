import sys, os
sys.path.append(os.getcwd())

from config import Config as cc
from main.main import Main
from error.my_exception import *

class Config(Main):
    def __init__(self) -> None:
        self.config = cc
        self.table = 'config'
        self.join_str = "LEFT JOIN config AS p ON config.bcategory=p.config_id"
        super().__init__()

    def disable(self, id):
        """禁用配置项"""
        sql = f"UPDATE {self.table} SET is_flag = 1 WHERE config_id='{id}';"
        self.db.other(sql_str=sql)

    def enable(self,id):
        """启用配置项"""
        sql = f"UPDATE {self.table} SET is_flag = 0 WHERE config_id='{id}';"
        self.db.other(sql_str=sql)

    def personal_verify(self, param, mode_name):
        
        if mode_name not in ['remove','find']:
            # 检查是名称是否相同
            config_name = param['config_name']
            config_type = param['type']
            is_repeat_data = self.find(config_name=config_name, type=config_type)
            if is_repeat_data:
                config_id = [config[0] for config in is_repeat_data]
                raise DataRepeat(f"已存在相同的数据,其id为{config_id}")
                    
        return param