
from bs4 import BeautifulSoup 
from selenium import webdriver
import requests
import pandas as pd
import time

url_input=input("Enter a Keyword to search:  ")

n=input("1) Featured/Relevance\n2) Price: Low to High\n3) Price: High to Low\n4) Avg. Customer Review\n5) Newest Arrivals\nEnter any one option for sort by: ")

#n=input()
if(n=='1'):
	URL="https://www.amazon.in/s?k="+url_input+"&ref=nb_sb_noss_2"  
elif(n=='2'):
	URL="https://www.amazon.in/s?k="+url_input+"&s=price-asc-rank&qid=1614514656&ref=sr_st_price-asc-rank"  
elif(n=='3'):
	URL="https://www.amazon.in/s?k="+url_input+"&s=price-desc-rank&qid=1614514659&ref=sr_st_price-desc-rank"  
elif(n=='4'):
	URL="https://www.amazon.in/s?k="+url_input+"&s=review-rank&qid=1614515006&ref=sr_st_review-rank"  
elif(n=='5'):
	URL="https://www.amazon.in/s?k="+url_input+"&s=date-desc-rank&qid=1614515046&ref=sr_st_date-desc-rank"  
else:
	print("Selection not Valid...Going with default Selection (Featured)")
	URL="https://www.amazon.in/s?k="+url_input+"&ref=nb_sb_noss_2"  


#np= int(input("Enter number of products (10-50): "))
print("Scraping data...")
#Amazon Part starts here
amazon_products=[]

#URL="https://www.amazon.in/s?k="+url_input+"&ref=nb_sb_noss_2"  
HEADERS = ({'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64)    AppleWebKit/537.36 (KHTML, like Gecko)  hrome/44.0.2403.157 Safari/537.36', 
                           'Accept-Language': 'en-US, en;q=0.5'}) 

webpage = requests.get(URL, headers=HEADERS) 
soup = BeautifulSoup(webpage.content, "lxml")
#print(len(soup.find_all('div',{'data-component-type':'s-search-result'})))

result=soup.find_all('div',{'data-component-type':'s-search-result'})
#item=result[0]

try:
	for item in result:
		if(len(amazon_products)>50):
			break
		atag=item.h2.a
		link="https://www.amazon.in" + atag.get('href')
		
		#price=price_soup.find('span','a-offscreen').text.strip()
		if(item.find('span','a-price')):
			price_soup=item.find('span','a-price')
			price=price_soup.find('span','a-offscreen').text.strip()
		else:
			price="-"
		amazon_products.append([link,atag.text,price])
		
		#print(rating)
		#print(price,atag.text,link)
except Exception as e: print(e)
#print(amazon_products)
for i,j in zip(amazon_products,range(len(amazon_products))):
	#driver =webdriver.Chrome(executable_path='C:\Program Files (x86)\chromedriver.exe')
	#driver.get(i[0])
	webpage = requests.get(i[0], headers=HEADERS) 
	soup = BeautifulSoup(webpage.content, "lxml")
	#print(soup.find('div',{'id':'detailBullets_feature_div'}))
	if(soup.find('div',{'id':'detailBullets_feature_div'})):
		info=soup.find('div',{'id':'detailBullets_feature_div'})
		#nontech
		details=info.text.split()

		asin=details[details.index('ASIN')+2]
		#dept=details[details.index('Department')+2]
		amazon_products[j].append(asin)
		#amazon_products[j].append(dept)
		#print(amazon_products[j])
	else:
		info=soup.find('div',{'id':'prodDetails'})
		#tech
		#print(i[0])
		details=info.find('table',{'id':'productDetails_detailBullets_sections1'}).text.split()
		if "ASIN" in details:
			asin=details[details.index('ASIN')+1]
		else:
			asin="-"
		amazon_products[j].append(asin)

	#time.sleep(10)
	#driver.implicitly_wait(30)
	#driver.close()
df = pd.DataFrame(amazon_products, columns = ['link', 'Name','Price','Product Number']) 
df['source']="Amazon"
#print(df)


writer = pd.ExcelWriter(r'output1.xlsx', engine='xlsxwriter',options={'strings_to_urls': False})
df.to_excel(writer)
writer.close()

print("Data saved to sheet.")
#df.to_excel("output1.xlsx")
#for i in amazon_products:
#	print(i)
# productDetails_detailBullets_sections1  detailBullets_feature_div   model no.

'''

#flipkart part starts here
URL_F="https://www.flipkart.com/search?q="+url_input+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
webpage_f = requests.get(URL, headers=HEADERS)




soup_f = BeautifulSoup(webpage_f.content, "lxml")
#print(soup_f)
flipkart_products=[]
atag_f=soup_f.find_all("div",class_="_4ddWXP")
print(atag_f)
'''