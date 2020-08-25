# %% [markdown]
# 研究有些股票开始上涨的原因.
# 本来想用 祥和实业 从20200728 开始的这波涨势为例子进行研究, 但是考虑到 daily data 的原因.是否可以找到一个从 20200810 开始上涨的 股票.
# 载入数据
#%%
import math
import datetime
import multiprocessing as mp
import tushare as ts
import os
import numpy as np
import pandas as pd
import datetime
p = print
# tushare 的初始化
token = '42e0612206685cd9bcd250cc5a3ef3931149303bc1d512c261174b5d'
pro = ts.pro_api(token)
# 获取当前上市公司列表，包括股票代码，注册地，行业，上市时间等数据
basic = pro.stock_basic(list_status = 'L')

#%%
basic

# %%
