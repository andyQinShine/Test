class Enviroment(object):
    fromdate = None
    todate = None
    """作为全局共享变量为各模块提供支持"""
    strategies = {} # 策略集合

    cleaners = {}
    readers = {}

