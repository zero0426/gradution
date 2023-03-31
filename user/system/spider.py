import requests
from bs4 import BeautifulSoup
"""





"""


r = requests.get('https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php/ho/cffex')

soup = BeautifulSoup(r.text, "lxml")
symbol = soup.find(attrs={"id": "option_symbol"}).find_all("li")[0].text
temp_attr = soup.find(attrs={"id": "option_suffix"}).find_all("li")
contract = [item.text for item in temp_attr]
print(contract)
print("hello")



