import requests
from bs4 import BeautifulSoup
import json
import time

OUTPUT_FILE = "docs/eps.json"

def fetch_eps(stock_code, market="sii"):
    """
    抓取單一股票 EPS
    market = "sii" 上市公司
    market = "otc" 上櫃公司
    """
    url = "https://mops.twse.com.tw/mops/web/ajax_t163sb04"
    payload = {
        "encodeURIComponent": "1",
        "step": "1",
        "firstin": "1",
        "off": "1",
        "queryName": "co_id",
        "inpuType": "co_id",
        "TYPEK": market,
        "co_id": stock_code
    }
    res = requests.post(url, data=payload)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    table = soup.find("table", {"class": "hasBorder"})
    if not table:
        return []

    rows = table.find_all("tr")[2:]  # 前兩列是表頭
    eps_list = []
    for row in rows:
        cols = [c.text.strip() for c in row.find_all("td")]
        if len(cols) >= 5:
            year, season, eps = cols[0], cols[1], cols[4]
            if eps and eps != "—":
                try:
                    eps_value = float(eps)
                except:
                    eps_value = None
                eps_list.append({
                    "date": f"{year}Q{season}",
                    "eps": eps_value
                })
    return eps_list

def main():
    # ✅ 這裡你可以指定要追蹤的股票
    stock_list = {
        "2330": "sii",  # 台積電 (上市)
        "2317": "sii",  # 鴻海 (上市)
        "2881": "sii",  # 富邦金 (上市)
        "2882": "sii",  # 國泰金 (上市)
    }

    all_eps = {}
    for code, market in stock_list.items():
        eps = fetch_eps(code, market)
        all_eps[code] = eps
        print(f"{code} 抓到 {len(eps)} 筆 EPS")
        time.sleep(5)  # 避免爬太快被擋

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_eps, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
