from bilibili import bilibili
import utils
import printer
import asyncio


# 领取银瓜子
async def GetAward():
    temp = await bilibili.get_time_about_silver()
    # print (temp['code'])    #宝箱领完返回的code为-10017
    if temp['code'] == -10017:
        printer.info(["# 今日宝箱领取完毕"])
    else:
        time_start = temp['data']['time_start']
        time_end = temp['data']['time_end']
        json_response = await bilibili.get_silver(time_start, time_end)
        return json_response
    

async def run():
    while True:
        printer.info(["检查宝箱状态"], True)
        json_rsp = await GetAward()
        if json_rsp is None or json_rsp['code'] == -10017:
            sleeptime = (utils.seconds_until_tomorrow() + 300)
            await asyncio.sleep(sleeptime)
        elif not json_rsp['code']:
            printer.info(["# 打开了宝箱"])
        elif json_rsp['code'] == 400:
            print('小黑屋, 6小时后重试')
            await asyncio.sleep(21600)
        else:
            printer.info(["# 继续等待宝箱冷却..."])
            # 未来如果取消了这个东西就睡眠185s，否则精确睡眠
            # surplus里面是min，float格式
            sleeptime = (json_rsp['data'].get('surplus', 3)) * 60 + 5
            await asyncio.sleep(sleeptime)
            
