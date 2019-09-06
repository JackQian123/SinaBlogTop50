import requests 
import re
import json
from requests.exceptions import RequestException
import time
from urllib.parse import quote

def get_one_page(url):
    headers = {   
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:66.0) Gecko/20100101 Firefox/66.0',
         }      
    # 这里要添加一个请求头，否则会访问网页失败    
    # 使用 RequestException可以捕捉所有的异常        
    try:  
        response = requests.get(url, headers = headers)        
    except RequestException:                
        return None
    return response.text
    time.sleep(2)  # 休眠2秒钟        

def parse_one_page(html): 
	pattern = re.compile('<tr .*?td-01 ranktop">(.*?)</t.*?href="(.*?)&Refer=top" target="_blank">(.*?)</a>', re.S) 
	items = re.findall(pattern, html)
	for item in items: 
		yield { 
			'No.': item[0],
			#'Url': 'https://s.weibo.com/top/summary'+item[1],
			'Title': item[2]
			} 

def write_to_file(content): 
	with open('SinaBlogTop50.txt', 'a', encoding='utf-8') as f:
		f.write(json.dumps(content, ensure_ascii=False) + '\n') 
		f.close()

def main():
    url = 'https://s.weibo.com/top/summary'
    html = get_one_page(url)
    t=time.strftime('%Y.%m.%d(%A)-%I:%M:%S',time.localtime(time.time()))
    with open('SinaBlogTop50.txt', 'a', encoding='utf-8') as f:
    	f.write(json.dumps(t, ensure_ascii=False) + '\n')
    	f.close() 
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':      
    main()