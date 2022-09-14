# -*- coding: utf-8 -*-
import sys

import common
from workflow import Workflow3

reload(sys)
sys.setdefaultencoding('utf8')


def main(wf):
    conversionRates = common.getConvertResult(currency='HKD', wf=wf)
    if conversionRates is None or conversionRates['convert'] is None:
        wf.add_item(valid=False, title="汇率获取失败", subtitle="", arg="汇率获取失败")
        wf.send_feedback()
        return
    query = wf.args[0].strip()
    if not isinstance(query, unicode):
        query = query.decode('utf8')
    # 默认展示1个单位
    if len(query) == 0:
        count = 1
    else:
        if not query.isdigit() and not common.is_float(numStr=query):
            wf.add_item(valid=False, title="请输入数字", subtitle="", arg="请输入数字")
            wf.send_feedback()
            return
        count = float(query)
    for cKey in conversionRates['convert']:
        conversion = conversionRates['convert'][cKey][0]
        if conversion is None:
            result = "无"
        else:
            result = conversionRates['convert'][cKey][0] * count
        wf.add_item(valid=True, title=common.add_space(result=result, space=4),
                    subtitle=common.add_space(result=conversionRates['convert'][cKey][1] + "（点击复制到剪贴板）", space=5),
                    arg=result, icon=conversionRates['convert'][cKey][2])
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
