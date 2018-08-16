class Enviroment(object):

    """作为全局共享变量为各模块提供支持"""
    fromdate = None
    base : str = 'btc'  # 计价币种
    quote : str = None  # 商品币种
    price_precision : str = None   # 价格精度
    amount_precision : str = None  # 数量精度
    bar_period : str = None # bar的时间粒度

