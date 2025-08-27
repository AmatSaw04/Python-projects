from bs4 import BeautifulSoup
import requests

live_url = "https://www.amazon.in/iPhone-16-Pro-Max-256/dp/B0DGJJM5HZ?ref_=pd_ci_mcx_mh_pe_rm_d1_cao_p_2_1&pd_rd_i=B0DGJJM5HZ&pd_rd_w=N8Ii1&content-id=amzn1.sym.d80e5568-8218-436c-8a68-b4e9dfb8447e&pf_rd_p=d80e5568-8218-436c-8a68-b4e9dfb8447e&pf_rd_r=940BBCQ55W9NN6RR61P9&pd_rd_wg=VTar3&pd_rd_r=b9f2a321-2d42-4ab7-96cd-f55e8143f897&th=1"
practice_url = "https://appbrewery.github.io/instant_pot/"

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
}
response = requests.get(live_url, headers=header)
soup = BeautifulSoup(response.content, "html.parser")
price = soup.find(name="span" , class_="a-price-whole").get_text()

print(price)
title = soup.find(id="productTitle").get_text().strip()
print(title)
original_price = price.replace(",", "")
ori_price = float(original_price)

buy = 110000

if ori_price < buy:
    message = f"{title} is on sale for {price}!"