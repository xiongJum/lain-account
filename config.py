class Account:

    DATABASE = ['account_id', 'date', 'amount', 'bcategory', 'scategory', 'pay', 'wallet', 
        'books', 'tag', 'city', 'remark', 'date_created']
    MUST_DATABASE = DATABASE[2:8]
    RELATED = DATABASE[4:8]
    JOIN_TABLE_CLOUMN = {
        "bcategory": "b.config_name as bcategory",
        "scategory": "s.config_name as scategory",
        "pay": "p.config_name as pay",
        "wallet": "w.config_name as wallet",
        "books": "bs.config_name as books",
        "date_created": "bill.date_created as date_created",
    }

    DATABASE_ZH = {
        "account_id": "ID",
        "date": "支付日期",
        "amount": "支付金额",
        "bcategory": "大分类",
        "scategory":"小分类",
        "pay": "支付方式",
        "wallet":"钱包",
        "books":"账本",
        "tag":"标签",
        "city":"城市",
        "remark":"备注",
        "date_created":"创建时间"
    }
    FILE_NAME = '账单表.xlsx'



class Fund:

    DATABASE = ['fund_id', 'wallet', 'start_amount', 'date_created']
    MUST_DATABASE = DATABASE[1:-1]
    JOIN_TABLE_CLOUMN = {
        "wallet": "w.config_name as wallet",
        "date_created": "fund.date_created as date_created",
    }

    DATABASE_ZH = {
        "fund_id": "ID",
        "wallet": "钱包",
        "start_amount": "年初金额",
        "date_created": "创建时间",
    }
    FILE_NAME = '资产表.xlsx'

class Config:

    DATABASE = ['config_id', 'config_name', 'type', 'bcategory', 'is_flag', 'date_created']
    MUST_DATABASE = ['config_name', 'type']

    JOIN_TABLE_CLOUMN = {
        "config_id": "config.config_id as config_id",
        "config_name": "config.config_name as config_name",
        "type": "config.type as type",
        "bcategory": "p.config_name as bcategory",
        "is_flag": "config.is_flag as is_flag",
        "date_created": "config.date_created date_created",
    }

    DATABASE_ZH = {
        "config_id": "ID",
        "config_name": "名称",
        "type": "类型",
        "bcategory": "父类名称",
        "is_flag": "是否禁用",
        "date_created": "创建日期",
    }

    FILE_NAME = '配置表.xlsx'

    FOREIGN_KEY  = {
        "bcategory": "大分类",
        "scategory": "中分类",
        "pay": "支付方式",
        "wallet": "钱包",
        "books": '账本',
    }

class Common:
    PROHIBITED_MOD = ['account_id', 'fund_id', 'fund_id', 'date_created', 'is_flag', 'type', 'parent_id']
    
    FOREIGN_KEY  = {
        "bcategory": "大分类",
        "scategory": "中分类",
        "pay": "支付方式",
        "wallet": "钱包",
        "books": '账本',
    }
    FLOAT_CLOUMN = ['amount', 'start_amount']

    FILE_PATH = './export/'

class TableName:

    TABLE_NAME = ['bill', 'fund', 'config']


