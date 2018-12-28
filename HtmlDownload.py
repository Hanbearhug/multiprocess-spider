import requests


class HtmlDownloader:
    def download(self, url):
        if url is None:
            return None
        agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
        headers = {'User-Agent': agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.text