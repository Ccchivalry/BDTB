import re
import requests
import pandas as pd

web_url = 'https://ibond.deloitte.com.cn/grade/gradePb.html'
web_header = {'Connection': 'keep-alive',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
              'Host': 'ibond.deloitte.com.cn',
              'Cookie': 'ace_settings=%7B%22sidebar-collapsed%22%3A1%7D; JSESSIONID=2811A7FD0904EE3CC97322BCF12D156D; BIGipServerRA_Ibond=!8UdZJAMffv91ltJfPQCamq130Nw0ssYeKwFrLPjQsjSCYL2os7+nWn9dCxVtqs8wMX0vV8Yjrbfujjc=; Hm_lvt_0726ce0489eac968cf6b74ba6d249811=1558677514; username=""; lockword=""; rememberPwd=""; Hm_lpvt_0726ce0489eac968cf6b74ba6d249811=1558678136; first_session=%7B%22visits%22%3A3%2C%22start%22%3A1558677545494%2C%22last_visit%22%3A1558678300197%2C%22url%22%3A%22https%3A%2F%2Fibond.deloitte.com.cn%2Fmember%2Fhome.html%22%2C%22path%22%3A%22%2Fmember%2Fhome.html%22%2C%22referrer%22%3A%22https%3A%2F%2Fibond.deloitte.com.cn%2Fuser%2Flogin.html%22%2C%22referrer_info%22%3A%7B%22host%22%3A%22ibond.deloitte.com.cn%22%2C%22path%22%3A%22%2Fuser%2Flogin.html%22%2C%22protocol%22%3A%22https%3A%22%2C%22port%22%3A80%2C%22search%22%3A%22%22%2C%22query%22%3A%7B%7D%7D%2C%22search%22%3A%7B%22engine%22%3Anull%2C%22query%22%3Anull%7D%2C%22prev_visit%22%3A1558678015568%2C%22time_since_last_visit%22%3A284629%2C%22version%22%3A0.4%7D',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

bond_list = []
pattern = re.compile('<td class="center"><a onclick.*?>(.*?)</a>.*?<td class="center">(.*?)</td><td class="center">(.*?)<.*?></td><td class="center">(.*?)</td><td class="center">(.*?)</td><td class="center">(.*?)</td><td class="center">(.*?)</td></tr>')
for i in range(564):
    formData = {'page': i, 'selYear': 2015}
    temp_data = requests.post(web_url, data=formData, headers=web_header)
    temp_text = temp_data.text
    items = re.findall(pattern, temp_text.replace('\t', '').replace('\n', ''))
    for item in items:
        bond_list.append([x.strip() for x in item])
#     print(bond_list)
res_15 = pd.DataFrame(bond_list, columns=['企业名称', '所属敞口', '评级结果', '评级状态', '地区', '评级类型', '评级日期'])
print(res_15.shape)
print(res_15.head())
