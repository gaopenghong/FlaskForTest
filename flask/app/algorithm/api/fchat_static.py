# coding:utf-8
from sshtunnel import SSHTunnelForwarder
import os
import pymysql
import requests
import socket
import pandas as pd
#from app.util.ssh_conf import remote_database
from app.algorithm.models.fchat_model import *


class Forchat(object):

    @staticmethod
    def match(text):
        url = 'http://t1fychat.fuyoukache.com/'
        data = {
            'content': text
        }
        r = requests.post(url, data)
        return r.json()


    @staticmethod
    def match_all():

        test_id_list = db.session.query(Fchatdetail.id).order_by(desc(Fchatdetail.id)).all()  #id 列表
        test_ids = []  ##封装后的ID列表
        for i in test_id_list:
            test_ids.append(i[0])
        for testid in test_ids:
            test_corpus = db.session.query(Fchatdetail.test_corpus).filter_by(id=testid).first()[0]  #测试语料
            exact_intention = db.session.query(Fchatdetail.exact_intention).filter_by(id=testid).first()[0]  ##预期意图
            algorithm_result = Forchat.match(test_corpus)
            if algorithm_result['status']['code'] == 200:
                intention_id = algorithm_result['property']['intentionId']  # 命中意图id
                corpus_ids = algorithm_result['property']['corpusId']  # 相似语料id
                intention_content = db.session.query(Fchatintention.name).filter_by(id=intention_id).first()[0]  # 命中意图
                if intention_content == exact_intention:
                    test_result = '0' #正确
                else:
                    test_result = '1' #错误
                corpus = str(corpus_ids).replace('[', '').replace(']', '')
                update_query = db.session.query(Fchatdetail).filter_by(id=testid).first()
                update_query.result = test_result
                update_query.match_corpus = corpus
                update_query.hit_intention = intention_content
                db.session.commit()
                db.session.close()
                print(testid)
            elif algorithm_result['status']['code'] == 201:
                test_result = '2'  # 未知
                update_query = db.session.query(Fchatdetail).filter_by(id=testid).first()
                update_query.result = test_result
                update_query.match_corpus = None
                update_query.hit_intention = None
                db.session.commit()
                db.session.close()
        '''
        corpusId = db.session.query(Fchatdetail.match_corpus).all()
        for i in corpusId:
            sql11 = 'select content from corpus where id=%s' % i[0]  # 数据库根据ID查询相似语料
            r = remote_database('t3', 'fykc_erobot_service', sql11)
            match_corpus = r[0][0]
            corpusId.match_corpus = match_corpus
            db.session.commit()
            db.session.close()
        '''


    @staticmethod
    def static():
        mysql_cn = pymysql.connect(host='rdst3j60ei1o0m8jjoi5o.mysql.rds.aliyuncs.com', port=3306, user='fykctest',
                                   passwd='fykctest_88', db='ftest')

        df = pd.read_sql('select * from algorithm_test_case_im;', con=mysql_cn)
        mysql_cn.close()
        coverage_rate = len(df[df['result'] != 2]) / len(df)     #覆盖率（正确率和错误率占全部的比例，除去未知）
        accuracy_rate = len(df[df['result'] == 0]) / len(df['id'])    #准确率（正确率占全部的比例）
        precision_rate = len(df[df['result'] == 0]) / len(df[df['result'] != 2])    #精确率（正确率占匹配到了数据的比例）
        recall_rate = len(df[df['result'] == 0]) / len(df['id'])        #召回率
        f_measure = (2*precision_rate*recall_rate)/(precision_rate+recall_rate)     #综合指标 F1=(2*P*R)/(P+R) P:精确率 R:召回率

        return coverage_rate, accuracy_rate, precision_rate, recall_rate, f_measure

    @staticmethod
    def exactstatic():
        mysql_cn = pymysql.connect(host='rdst3j60ei1o0m8jjoi5o.mysql.rds.aliyuncs.com', port=3306, user='fykctest',
                                   passwd='fykctest_88', db='ftest')
        df1 = pd.read_sql('select DISTINCT exact_intention from algorithm_test_case_im', con=mysql_cn)

        df2=df1.values.tolist()
        dfs=[]
        for n in df2:
            dfs.append(n[0])

        for i in dfs:
            df = pd.read_sql('select * from algorithm_test_case_im where exact_intention="%s";' % i, con=mysql_cn)
            intention_exact = i
            coverage_exact = len(df[df['result'] != 2]) / len(df)
            accuracy_exact = len(df[df['result'] == 0]) / len(df['id'])
            recall_exact = len(df[df['result'] == 0]) / len(df['id'])
            if len(df[df['result'] != 2]) ==0:
                precision_exact = 0
                print(precision_exact)
            else:
                precision_exact = len(df[df['result'] == 0]) / len(df[df['result'] != 2])
            if precision_exact + recall_exact ==0:
                f_measure_exact=0
            else:
                f_measure_exact = (2 * precision_exact * recall_exact) / (precision_exact + recall_exact)
            print(intention_exact,coverage_exact, accuracy_exact, precision_exact, recall_exact, f_measure_exact)

        mysql_cn.close()


if __name__=='__main__':
    Forchat.match(text='你好')
