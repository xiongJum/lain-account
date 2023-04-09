import sys, os
sys.path.append(os.getcwd())

from config import Fund as cf
from main.main import Main
    

class Fund(Main):
    def __init__(self) -> None:
        self.config = cf
        self.table = 'fund'
        self.join_str = "LEFT JOIN config AS w ON wallet = w.config_id"
        super().__init__()