import sys, os
sys.path.append(os.getcwd())

from tabulate import tabulate
import pandas
from main import account, config, fund
from config import Account, Config, Fund
from export_Import.upload import OpenFile
from export_Import.download import DownLoad


def find(param, config):

    for index, args in enumerate(sys.argv):

        sys_argv_len = len(sys.argv)
        if sys_argv_len > 3:
            param_id = sys.argv[3]
            cloumns = config.DATABASE[1:]

        if args in ['--all', '-a'] and len(sys.argv) > index:
            """查询数据"""
            # 当 argv 的长度大于3时, 获取并拼接条件
            all_kwargs =  {value.split("=")[0]: value.split("=")[1] for value in sys.argv[3:]} if sys_argv_len > 2 else {}
            try:
                tables = param.find(is_mapping=True, **all_kwargs)
            except Exception as e:
                print(e)
            # 增加表名称,并通过表格形式打印出来
            tables_list = [table for table in tables]

            df = pandas.DataFrame(tables_list, columns=config.DATABASE_ZH.values())
            # df = df.drop(['ID'], axis=1)
            print(df)

            # tables_list.insert(0, config.DATABASE_ZH.values())
            # print(tabulate(tables_list, headers='firstrow', tablefmt='fancy_grid', showindex=True))

        if args in ['--new', '-n'] and len(sys.argv) > index:
            values = sys.argv[3:]
            # 组合列名和值,将其转换为字典形式
            all_kwargs = {cloumns[index]: value for index, value in enumerate(values) }
            # try:
            #     param.add(**all_kwargs)
            # except Exception as e:
            #     print(e)
            param.add(**all_kwargs)

        
        if args in ['--mod', '-m'] and len(sys.argv) > index:
            new_param = sys.argv[4:]
            # 格式化参数，将其转化为字典
            all_kwargs = {value.split("=")[0]: value.split("=")[1] for value in new_param}
            # 调取方法
            param.mod(id=param_id, **all_kwargs)


        if args in ['--del', '-r'] and len(sys.argv) > index:
            # 调取方法进行删除
            param.remove(id=param_id)

        if args in ['--upload', '-u'] and len(sys.argv) > index:
            # 上传
            # of = OpenFile()
            file_name = sys.argv[3] if sys_argv_len > 3 else False
            try:
                param.open_file()
            except FileNotFoundError as e:
                print("找不到文件,请检查路径是否正确", e)

        if args in ['--down', '-dl'] and len(sys.argv) > index:
            # 下载
            all_kwargs =  {value.split("=")[0]: value.split("=")[1] for value in sys.argv[3:]} if sys_argv_len > 2 else {}
            down = DownLoad(param, config)
            down.download_account(all_kwargs)
        
        # 禁用启用配置项
        if param.__class__.__name__ == 'Config':
            if args in ['--disable', '-d'] and len(sys.argv) > index:
                param.disable(param_id)
            if args in ['--enable', '-e'] and len(sys.argv) > index:
                param.enable(param_id)
        

def run():

    if len(sys.argv) > 1:
        if sys.argv[1] == 'bill':
            find(account.Account(), Account)

        elif sys.argv[1] == 'config':
            find(config.Config(), Config)

        elif sys.argv[1] == 'fund':
            find(fund.Fund(), Fund)
    else:

        print("""
            key: 
                bill  账单
                config 配置项
                fund   年初余额
            value:
                --all -a 查看全部  [<key> --all]
                --all -a 按照条件查看  [<key> --all <cloumn=value> <cloumn2=value2>]
                --mod -m 修改     [<key> --mod <id> <cloumn=value> <cloumn2=value2>]
                --del -r 删除     [<key> --del <id>]
                --new -n 增加     [<key> --new <value> <value2>]
                --upload -u 导入  [<key> --upload]
                --down -dl 导入   [<key> --down <可选><cloumn=value>]
            以下当 key 为 config时
                --disable -d 禁用 [<key> --disable <value>]
                --enable  -e 启用 [<key> --disable <value>]
        """)

if __name__ == '__main__':

    run()