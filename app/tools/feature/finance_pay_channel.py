# coding:utf-8
import requests
import time


# 保理对账
def baoli_checking(environment):
    current_month = time.strftime('%Y-%m', time.localtime())
    year = current_month.split('-')[0]
    month = int(current_month.split('-')[1]) + 1
    if month < 10:
        month = '0%s' % month
    url = 'http://%sproxy.fuyoukache.com/fykc-financeana-service/api/internal/checkBaoliOrder?date=%s-%s-20 00:00:00' % (environment, year, month)
    print(url)
    if environment == '' or environment is None:
        return '请选择测试环境'
    r = requests.get(url)
    return r.json()


# 保理还款
def baoli_repayment(environment):
    url = 'http://%scaiwu.fuyoukache.com/api/fy/baoli/batchBaoliPay.do' % environment
    print(url)
    if environment == '' or environment is None:
        return '请选择测试环境'
    r = requests.get(url)
    return r.json()


# 司机付款
def driver_payment(environment):
    url = 'http://%scaiwu.fuyoukache.com/api/internal/short/setPayDebug.do?payDebug=true&password=11231qa2ws3ed' % environment
    print(url)
    if environment == '' or environment is None:
        return '请选择测试环境'
    r = requests.get(url)
    return r.json()


# 经纪人付款
def agent_payment(environment, broker_id, bill_no):
    url = 'http://%scaiwu.fuyoukache.com/service/fykc-caiwu-service/api/internal/broker/paymentBrokerBill.do' % environment
    print(url)
    if environment == '' or environment is None:
        return '请选择测试环境'
    data = {
        'brokerId': broker_id,
        'billNo': bill_no
    }
    r = requests.post(url, data)
    return r.json()


if __name__ == '__main__':
    baoli_checking('t1')
    baoli_repayment('t1')
    driver_payment('t1')
    agent_payment('t1', '111', '222')

