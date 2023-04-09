class DateIncorrect(Exception):
    """时间不合规"""
    pass

class DataInvalidation(Exception):
    """数据无效"""
    pass

class DataRepeat(Exception):
    """数据重复"""
    pass

class ParamAbsence(Exception):
    """参数缺失"""
    pass