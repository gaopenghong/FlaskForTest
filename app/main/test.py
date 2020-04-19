# -*- coding: utf-8 -*-
# __author__ = liuchunfu
# __time__   = 2019-08-16


import requests


def login():
    url = "https://t1ua.fuyoukache.com/api/uc/src/image/genCheckCodeRequest"
    res = requests.post(url)
    url1 = "https://t1ua.fuyoukache.com/api/uc/auth/login"
    params = {
        'userName': '18515579500',
        'userPassword': 'Fy@123456789',
        'requestId': res.text,
        'checkCode': '1123'
    }
    res1 = requests.post(url1, params)
    print(res1.json())
    data = res1.json()
    name = data['data'][0]['name']
    print(name)


def bubbleSort(arr):
    n = len(arr)

    # 遍历所有数组元素
    for i in range(n):

        # Last i elements are already in place
        for j in range(0, n - i - 1):

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


if __name__ == '__main__':
    # login()
    arr = [64, 34, 25, 12, 22, 11, 90]

    res = bubbleSort(arr)
    print(res)
    print("排序后的数组:")
    for i in range(len(arr)):
        print("%d" % arr[i])
