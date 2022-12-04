import requests
from bs4 import BeautifulSoup


class EtherScan:
    def __init__(self):
        self.scan_url = ''
        self.chain = ''
        self.header = {}

    def get_tokens(self, chain, address):
        response = self.request_scan(chain, address)
        if response.status_code == 200:
            return self.parse_body(chain, response.text)

        return {
            'count': 0,
            'tokens': []
        }

    def request_scan(self, chain, address):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        if self.header is not None:
            for key in self.header.keys():
                headers[key] = self.header[key]

        url = self.scan_url + '/address/' + address
        return requests.get(url, headers=headers)

    def parse_body(self, chain, html):
        token_count = 0
        token_dict = {}
        soup = BeautifulSoup(html, 'lxml')

        container = soup.find(attrs={'id': 'ContentPlaceHolder1_divSummary'})
        tokens = container.findAll('span')
        for item in tokens:
            if 'title' in item.attrs:
                title = item.attrs['title']
                if 'Token Contracts' in title:
                    token_count = int(item.text)

        container = soup.find(attrs={'id': 'availableBalanceClick'})
        if container is None:
            return None
        ul_list = container.findAll('li')

        current_token = ''
        for item in ul_list:
            if 'class' not in item.attrs:
                continue

            class_list = item.attrs['class']
            if 'list-custom-divider' in class_list:
                current_token = item.text + ''
                current_token = current_token.strip().split(' ')[0]
                token_dict[current_token] = []
                continue

            html = str(item)
            soup = BeautifulSoup(html, 'lxml')
            span = soup.select('li  div  div span span')
            if (len(span) > 0):
                token_info = {
                    'token': span[0].attrs['title'],
                }
                span = soup.select('li  div  span.list-amount')
                if len(span) > 0:
                    amount = span[0].text
                    if '$' in amount:
                        amount = amount.split('$')[0].strip() + '$'
                    token_info['amount'] = amount
                link = soup.select('li a')
                if len(link) > 0:
                    token_info['url'] = self.scan_url + link[0].attrs['href']
                token_dict[current_token].append(token_info)
            else:
                token_info = {
                    'token': ''
                }
                span = soup.select('li  div div span')
                if (len(span) > 0):
                    token_info['token'] = span[0].text
                span = soup.select('li  div span.list-amount')
                if (len(span) > 0):
                    token_info['amount'] = span[0].text
                link = soup.select('li a')
                if len(link) > 0:
                    token_info['url'] = self.scan_url + link[0].attrs['href']
                token_dict[current_token].append(token_info)
        token_list = []
        for key in token_dict.keys():
            token_list.append({
                'chain': key,
                'tokens': token_dict[key]
            })

        return {
            'chain': chain,
            'count': token_count,
            'tokens': token_list
        }
