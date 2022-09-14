# -*- coding: utf-8 -*-
import json
import re
import sys
import time

from workflow import web

reload(sys)
sys.setdefaultencoding('utf8')


def getConvertResult(currency, wf):
    try:
        exchange_url = None
        with open('currency.conf', 'r') as f:
            js = f.read().strip()
            if js is not None and len(js) > 0:
                dic = json.loads(js)
                exchange_url = dic['exchangeUrl']
        if exchange_url is None or len(exchange_url) <= 0:
            raise Exception("Sorry, please setting your currency.conf!")
        url = exchange_url + currency
        last_time = None
        with open('local_cache', 'r') as f:
            js = f.read().strip()
            if js is not None and len(js) > 0:
                dic = json.loads(js)
                last_time = dic['cTime']
        if last_time is None or (int(time.time()) - last_time > 60 * 60 * 3):
            rt = web.get(url, timeout=2).json()
            wf.logger.debug('===>获取币种{0}的换算结果为:{1}'.format(currency, rt))
            if rt is None or rt["conversion_rates"] is None:
                return None
            conversionRates = rt["conversion_rates"]
            currentTime = int(time.time())
            newConvert = {'cTime': currentTime,
                          'convert': {'USD': [], 'CNY': [], 'HKD': [], 'EUR': [], 'RUB': [], 'GBP': [], 'JPY': []}}
            usd = conversionRates.get("USD")  # 美元
            newConvert['convert']['USD'].append(usd)
            newConvert['convert']['USD'].append("美元")
            newConvert['convert']['USD'].append("./images/usd.png")
            cny = conversionRates.get("CNY")  # 人民币
            newConvert['convert']['CNY'].append(cny)
            newConvert['convert']['CNY'].append("人民币")
            if currency == 'CNY':
                newConvert['convert']['CNY'].append("./images/focus_cny.png")
            else:
                newConvert['convert']['CNY'].append("./images/cny.png")
            hkd = conversionRates.get("HKD")  # 港币
            newConvert['convert']['HKD'].append(hkd)
            newConvert['convert']['HKD'].append("港币")
            if currency == 'HKD':
                newConvert['convert']['HKD'].append("./images/focus_hkd.png")
            else:
                newConvert['convert']['HKD'].append("./images/hkd.png")
            eur = conversionRates.get("EUR")  # 欧元
            newConvert['convert']['EUR'].append(eur)
            newConvert['convert']['EUR'].append("欧元")
            newConvert['convert']['EUR'].append("./images/eur.png")
            sur = conversionRates.get("RUB")  # 卢布
            newConvert['convert']['RUB'].append(sur)
            newConvert['convert']['RUB'].append("卢布")
            newConvert['convert']['RUB'].append("./images/rub.png")
            gbp = conversionRates.get("GBP")  # 英镑
            newConvert['convert']['GBP'].append(gbp)
            newConvert['convert']['GBP'].append("英镑")
            newConvert['convert']['GBP'].append("./images/gbp.png")
            jpy = conversionRates.get("JPY")  # 日元
            newConvert['convert']['JPY'].append(jpy)
            newConvert['convert']['JPY'].append("日元")
            newConvert['convert']['JPY'].append("./images/jpy.png")
            # local save
            js = json.dumps(newConvert)
            with open('local_cache', 'w') as f:
                f.write(js)
            return newConvert
        else:
            if currency == 'CNY':
                dic['convert']['CNY'][2] = "./images/focus_cny.png"
            else:
                dic['convert']['CNY'][2] = "./images/cny.png"
            if currency == 'HKD':
                dic['convert']['HKD'][2] = "./images/focus_hkd.png"
            else:
                dic['convert']['HKD'][2] = "./images/hkd.png"
            return dic
    except Exception as ex:
        wf.logger.debug("出现如下异常%s" % ex)
        wf.logger.debug('===>获取币种的换算结果异常')
        return None


def is_float(numStr):
    flag = False
    numStr = str(numStr).strip().lstrip('-').lstrip('+')  # 去除正数(+)、负数(-)符号
    try:
        reg = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
        res = reg.match(str(numStr))
        if res:
            flag = True
    except Exception as ex:
        print("is_float() - error: " + str(ex))
    return flag


def add_space(result, space):
    if result is None:
        return ""
    if space == 0:
        return result
    result = str(result)
    for i in range(0, space):
        result = " " + result
    return result
