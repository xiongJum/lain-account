import sys, os
sys.path.append(os.getcwd())

from config import Account as ca
from main.main import Main

class Account(Main):
    
    def __init__(self) -> None:
        self.config = ca
        self.table = 'bill'
        self.join_str = """
            LEFT JOIN config as b ON bill.bcategory = b.config_id
            LEFT JOIN config as s ON scategory = s.config_id
            LEFT JOIN config as p ON pay = p.config_id
            LEFT JOIN config as w ON wallet = w.config_id
            LEFT JOIN config as bs ON books = bs.config_id
        """
        super().__init__()