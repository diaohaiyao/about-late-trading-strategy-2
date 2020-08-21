# 以 博睿 为例子 ,分析研究一只新股 整个上市过程中,连带造成上涨的规律.

#  688229	N博睿
# 上市日期 20200817
#  申购日期 08-05 周三
# 缴款日期 : 08-07
# 首先先研究上市日期, 可能还会把整个研究期限延长到:首次下跌.

# 首先还是要先获取数据

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
#%%
# tushare 的初始化
token = '42e0612206685cd9bcd250cc5a3ef3931149303bc1d512c261174b5d'
pro = ts.pro_api(token)
# 获取当前上市公司列表，包括股票代码，注册地，行业，上市时间等数据
basic = pro.stock_basic(list_status = 'L')
####################################################
# 不要使用新股的股票名字, 新股名: N**, 可能后面会被改
newstock_sym = '688229'
stock_code = list(basic[basic['symbol'] == newstock_sym]['ts_code'])[0]
# 这个数据接口没有考虑复权的问题，进行修改为下面的通用接口：
# 通用接口获得前复权数据：
# stock_data_p = ts.pro_bar(api = pro, ts_code = stock_code, start_date = '20200101', adj = 'qfq')
stock_data_p = ts.pro_bar(api = pro, ts_code = stock_code, adj = 'qfq')
# %%
# 688229	N博睿 所属板块有: 软件服务, 北京板块, 人工智能, 大数据,和 融资融券. 由于融资融券太普遍, 所以暂时不作为一个考察方向.
# 下面读取 所属板块数据,并构筑network
net1_name = '软件服务'
net1 = pd.read_excel('./stock network/' +net1_name +   '.xlsx')
print(net1)
#%%
# for mac
#net1 = pd.read_excel('/Users/jiangsiyuan/Google 云端硬盘/量化交易开发/about late trading strategy/stock network/' +net1_name +   '.xlsx')
#p(net1)
net2_name = '北京板块'
net2 = pd.read_excel('G:/Jiang research/stock network/' +net2_name +   '.xlsx')
#net2 = pd.read_excel('/Users/jiangsiyuan/Google 云端硬盘/量化交易开发/about late trading strategy/stock network/' +net2_name +   '.xlsx')
net3_name = '人工智能'
net3 = pd.read_excel('G:/Jiang research/stock network/' +net3_name +   '.xlsx')
#net3 = pd.read_excel('/Users/jiangsiyuan/Google 云端硬盘/量化交易开发/about late trading strategy/stock network/' +net3_name +   '.xlsx')
net4_name = '大数据'
net4 = pd.read_excel('G:/Jiang research/stock network/' +net4_name +   '.xlsx')
#net4 = pd.read_excel('/Users/jiangsiyuan/Google 云端硬盘/量化交易开发/about late trading strategy/stock network/' +net4_name +   '.xlsx')

#%%
# 显示 net1 的 columns
net1.columns.values.tolist()
#%%
net1['板块名称'] = net1_name
net2['板块名称'] = net2_name
net3['板块名称'] = net3_name
net4['板块名称'] = net4_name
#%%
net_all = pd.DataFrame()
net_all = net_all.append(net1)
net_all = net_all.append(net2)
net_all = net_all.append(net3)
net_all = net_all.append(net4)
print(len(net_all))
#%%
##########################################
# 增加边, 从dataframe 的两个columns
import networkx as nx
G_stock = nx.Graph()
G_stock = nx.from_pandas_edgelist(net_all, '板块名称', '名称')
G_stock.remove_node('*ST信威')
##########################################
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
#figure(figsize = (10, 8))
#nx.draw_shell(G, with_labels =True)
#nx.spring_layout(G_stock)
#nx.draw_networkx(G_stock)
#plt.show()
# ok , 把所有的 net 加进去
# 这里要删除: G_stock.remove_node('*ST信威') 第一次运行好像会产生错误...
color_map = []
launch_date = '20200817'
for node in G_stock :
    if node != '软件服务' and node != '北京板块' and node != '人工智能' and node != '大数据行情':
        if node == '宝信Ｂ':
            color_map.append('blue')
        elif node == '京东方Ａ':
            node = '京东方A'
            stock_code = list(basic[basic['name'] == node]['ts_code'])[0]
            # 这里研究的是  688229	N博睿, 它的上市时间是: 20200817 , 所以也从这一天开始研究
            stock_data_p = ts.pro_bar(api = pro, ts_code = stock_code, start_date = launch_date, adj = 'qfq')
            #p(stock_data_p)
            one_pct_chg = stock_data_p[stock_data_p['trade_date'] == launch_date]['pct_chg']
            if len(one_pct_chg) == 0:
                color_map.append('blue')
            elif float(one_pct_chg) > 0:
                color_map.append('red')
            else :
                color_map.append('green')
        #elif node == '*ST信威':
         #   G_stock.remove_node('*ST信威')
        else :
            node = node.replace(' ', '')
            #print(node)
            stock_code = list(basic[basic['name'] == node]['ts_code'])[0]
            # 这里研究的是  688229	N博睿, 它的上市时间是: 20200817 , 所以也从这一天开始研究
            stock_data_p = ts.pro_bar(api = pro, ts_code = stock_code, start_date = launch_date, adj = 'qfq')
            #p(stock_data_p)
            one_pct_chg = stock_data_p[stock_data_p['trade_date'] == launch_date]['pct_chg']
            if len(one_pct_chg) == 0:
                color_map.append('blue')
            elif float(one_pct_chg) > 8 :
                color_map.append('red')
            else :
                color_map.append('green')
    else:
        color_map.append('black')
# 作图
figure(figsize = (10*1.5, 8*1.5))
nx.spring_layout(G_stock)
nx.draw_networkx(G_stock, node_color = color_map, node_size = 100, with_labels=False)
plt.show()

#%%
# 如果把所有新上市股票做成 network 呢?
# 所研究股票:  688229	N博睿 与 08-17 上市.
# 等一天上市的股票还有: 龙腾光电688055;













# %%
# 读取整个 G:\Jiang research\stock network 的数据资料:
import os
#path_network = 'G:\Jiang research\stock network'
# for mac
path_network = './stock network'
files_network = os.listdir(path_network)
#print(files_network)

# 暂时还是选择用 dict 存储数据
netdata_dict = dict()
# 在 network 的Excel 文件内容放进 netdata_dict
for net_name in files_network :
    if net_name != '.DS_Store':
        net_one = pd.read_excel(path_network +'/' +net_name)
        #print(net_one[:10])
        net_name_dict = net_name.split('.')[0]
        netdata_dict[net_name_dict] = net_one
        #print(netdata_dict[net_name_dict].iloc[:10])

net_all = pd.DataFrame()
for netname_one , netdata_one in netdata_dict.items() :
    netdata_one['板块名称'] = netname_one
    net_all = net_all.append(netdata_one)
print(len(net_all))

#%%
##########################################
# 增加边, 从dataframe 的两个columns
import networkx as nx
G_stock = nx.Graph()
G_stock = nx.from_pandas_edgelist(net_all, '板块名称', '名称')
G_stock.remove_node('*ST信威')
##########################################
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
#figure(figsize = (10, 8))
#nx.draw_shell(G, with_labels =True)
#nx.spring_layout(G_stock)
#nx.draw_networkx(G_stock)
#plt.show()
# ok , 把所有的 net 加进去
# 这里要删除: G_stock.remove_node('*ST信威') 第一次运行好像会产生错误...
plate_list = list(netdata_dict.keys())
### 重写一个循环
basic['symbol_int'] = basic['symbol'].apply(int) # 新增数据列, 用于检索数据
#############################
color_map = []
select_stocklist = []
#launch_date = '20200817'
#换一个日期看看
#launch_date = '20200814'
for node in G_stock :
    #print(node)
    if node not in plate_list :
        node_symbol = net_all[net_all['名称'] == node].iloc[0]['代码']
        #print(type(node_symbol))
        stock_code_list = list(basic[basic['symbol_int'] == node_symbol]['ts_code'])
        if len(stock_code_list) == 0:
            color_map.append('blue') # 各种目前的异常股票都设定为blue, 以后再说.
        else :
            stock_code = stock_code_list[0]
            #stock_data_p = ts.pro_bar(api = pro, ts_code = stock_code, start_date = launch_date, adj = 'qfq')
            #p(stock_data_p)
            #one_pct_chg = stock_data_p[stock_data_p['trade_date'] == launch_date]['pct_chg']
            stock_data_p = all_stockdata[all_stockdata['ts_code'] == stock_code]
            if len(stock_data_p) == 0:
                color_map.append('blue')
            else :
                one_pct_chg = stock_data_p.iloc[0]['pct_chg']
                if float(one_pct_chg) > 3 :
                    select_stocklist.append(stock_data_p['ts_code'].iloc[0])
                    color_map.append('red')
                else :
                    color_map.append('green')
    else:
        color_map.append('black')

# 作图
figure(figsize = (10*1.5, 8*1.5))
nx.spring_layout(G_stock)
nx.draw_networkx(G_stock, node_color = color_map, node_size = 60, with_labels=False)
plt.show()

# %%
# 获得发行日当天的全部股票的交易数据, 并改变上面每一只股票一查的算法
launch_date = '20200817'
all_stockdata = pd.DataFrame()
for one_ts_code in basic['ts_code']:
    stock_data_p = ts.pro_bar(api = pro, ts_code = one_ts_code, start_date = launch_date, adj = 'qfq')
    try :
        oneday_stockdata = stock_data_p[stock_data_p['trade_date'] == launch_date]
        all_stockdata = all_stockdata.append(oneday_stockdata)
    except :
        print('when ts_code is ', one_ts_code, 'i get a err')

print('len for all stockdata', len(all_stockdata))
print('len for basic is:', len(basic))
all_stockdata.to_csv('./daily data/' +launch_date +'_stockdata.csv')

#%%
# 所有股票中 上涨大于5 的股票:
num_then5 = len(all_stockdata[all_stockdata['pct_chg'] > 5])
print('所有股票中 上涨大于5 的股票共:', num_then5)
# 在 network 中: 即与新股有板块关联的中的 上涨大于 5 的股票
num_then5_network = len(set(select_stocklist))
print('在 network 中占据所有上涨超过 5 的股票的比例:', num_then5_network/num_then5)
# %%
