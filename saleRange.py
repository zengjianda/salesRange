# coding:utf8
import logging
import time

import matplotlib.pyplot as plt
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler

level = ["倔强青铜", "秩序白银", "荣耀黄金", "尊贵铂金", "永恒钻石", "至尊星耀", "最强王者"]

def updateLevel(type):
    # 查询数据
    sale_data = pd.read_excel("user.xlsx")
    # 筛选数据
    data = sale_data[["visit_count", "amount_count"]][sale_data.type == type]
    # 数据归一化
    scaler = MinMaxScaler()
    scaler.fit(data)
    on_line_bg = scaler.transform(data)
    data = pd.DataFrame(on_line_bg, columns=["visit_count", "amount_count"])
    #销量占比提高7倍
    data["amount_count"] = data["amount_count"].apply(lambda x: x * 7)
    #柱状图
    data.plot(kind='bar', figsize=(16, 6))
    plt.show()


    # 聚类
    clusterer = KMeans(n_clusters=len(level), random_state=0).fit(data)
    centers = clusterer.cluster_centers_
    # 按销量排序 因为聚类具有随机性
    centers = centers[:, 1]
    centers = centers.tolist()
    from copy import deepcopy
    orders = deepcopy(centers)
    orders.sort()
    values = []
    for i in range(len(centers)):
        for j in range(len(orders)):
            if centers[i] == orders[j]:
                values.append(j)
                break
    #得到数据的预测值
    preds = clusterer.predict(data)
    #聚类得分 越大 聚类效果越好
    score = silhouette_score(data, preds)
    for index, value in enumerate(preds):
        preds[index] = values[value]
    #数据增加聚类值 对应的是王者荣耀等级
    online_data = sale_data[sale_data.type == type]
    online_data["cluster"] = preds

    # for i in online_data.index:
    #     update_sql = "update sysuser set level = " + str(online_data.loc[i].cluster) + " where id = " + str(
    #         online_data.loc[i].id)
    #     print(update_sql)
    #     cursor = con.cursor()
    #     cursor.execute(update_sql)
    #     con.commit()
    #     cursor.close()

    #解决中文乱码问题
    plt.rcParams['font.sans-serif'] = ['SimHei']
    #设置图片尺寸大小
    plt.figure(figsize=(16, 10))
    #设置x轴和y轴的名称
    plt.xlabel("拜访量")
    plt.ylabel("销量")
    #循环展示散点数据
    for i in range(len(level)):
        sales = online_data[online_data.cluster == i]
        plt.scatter(sales["visit_count"], sales["amount_count"], marker='o', label=level[i], s=30)
    #展示每个点的对应的销售名字
    # for i in online_data.index:
    #     plt.annotate(online_data.loc[i].username, xy=(online_data.loc[i].visit_count, online_data.loc[i].amount_count),
    #                  xytext=(-20, 20),
    #                  textcoords='offset points', ha='right', va='bottom',
    #                  bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
    #                  arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    #设置标题
    plt.title("销售排行榜")
    plt.legend(loc='upper right')
    plt.show()


def calcLevel():
    type_list = [0, 1, 2]
    for i in range(len(type_list)):
        updateLevel(type_list[i])


if __name__ == '__main__':
    # log = logging.getLogger('apscheduler.executors.default')
    # log.setLevel(logging.ERROR)  # DEBUG
    #
    # fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    # h = logging.StreamHandler()
    # h.setFormatter(fmt)
    # log.addHandler(h)
    #
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(calcLevel, 'cron', hour=3, minute=0, second=0)
    # scheduler.start()
    # while (True):
    #     time.sleep(2)
    updateLevel(1)
