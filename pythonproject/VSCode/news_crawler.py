import requests
from bs4 import BeautifulSoup
import time
import csv

class NewsCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = 'https://www.sina.com.cn'
    def get_news_list(self, url):
        """获取新闻列表"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取新闻链接和标题
            news_items = []
            # 不同新闻板块的选择器可能不同，这里以新浪新闻首页为例
            for item in soup.select('.news-item'):
                title_elem = item.select_one('a')
                if title_elem:
                    title = title_elem.text.strip()
                    link = title_elem.get('href')
                    if link and 'sina.com.cn' not in link:
                        link = self.base_url + link
                    time_elem = item.select_one('.time')
                    time = time_elem.text.strip() if time_elem else ''
                    news_items.append({
                        'title': title,
                        'link': link,
                        'time': time
                    })
            return news_items
        except Exception as e:
            print(f"获取新闻列表失败: {e}")
            return []
    
    def get_news_content(self, url):
        """获取新闻内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取新闻内容
            content_elem = soup.select_one('.article-content')
            if not content_elem:
                content_elem = soup.select_one('.content')
            if content_elem:
                content = '\n'.join([p.text.strip() for p in content_elem.select('p')])
            else:
                content = ''
            
            # 提取新闻来源
            source_elem = soup.select_one('.source')
            source = source_elem.text.strip() if source_elem else ''
            
            return {
                'content': content,
                'source': source
            }
        except Exception as e:
            print(f"获取新闻内容失败: {e}")
            return {'content': '', 'source': ''}
    
    def crawl(self, url, output_file='news.csv', max_news=50):
        """爬取新闻并保存到CSV文件"""
        print(f"开始爬取新闻: {url}")
        news_list = self.get_news_list(url)
        
        # 限制爬取数量
        news_list = news_list[:max_news]
        
        # 保存到CSV文件
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['军事'])
            
            for i, news in enumerate(news_list):
                print(f"爬取第{i+1}/{len(news_list)}条新闻: {news['title']}")
                # 获取新闻内容
                content_data = self.get_news_content(news['link'])
                # 写入CSV
                writer.writerow([
                    news['title']
                ])
                # 避免请求过于频繁
                time.sleep(1)
        
        print(f"爬取完成，共获取{len(news_list)}条新闻，保存到{output_file}")

if __name__ == "__main__":
    crawler = NewsCrawler()
    # 爬取新浪新闻首页
    crawler.crawl('https://news.sina.com.cn/', 'sina_news.csv', max_news=20)
import requests
from bs4 import BeautifulSoup
import time
import csv

class NewsCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = 'https://news.sina.com.cn'
    
    def get_news_list(self, url):
        """获取新闻列表"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取新闻链接和标题
            news_items = []
            # 不同新闻板块的选择器可能不同，这里以新浪新闻首页为例
            for item in soup.select('.news-item'):
                title_elem = item.select_one('a')
                if title_elem:
                    title = title_elem.text.strip()
                    link = title_elem.get('href')
                    if link and 'sina.com.cn' not in link:
                        link = self.base_url + link
                    time_elem = item.select_one('.time')
                    time = time_elem.text.strip() if time_elem else ''
                    news_items.append({
                        'title': title,
                        'link': link,
                        'time': time
                    })
            return news_items
        except Exception as e:
            print(f"获取新闻列表失败: {e}")
            return []
    
    def get_news_content(self, url):
        """获取新闻内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取新闻内容
            content_elem = soup.select_one('.article-content')
            if not content_elem:
                content_elem = soup.select_one('.content')
            if content_elem:
                content = '\n'.join([p.text.strip() for p in content_elem.select('p')])
            else:
                content = ''
            
            # 提取新闻来源
            source_elem = soup.select_one('.source')
            source = source_elem.text.strip() if source_elem else ''
            
            return {
                'content': content,
                'source': source
            }
        except Exception as e:
            print(f"获取新闻内容失败: {e}")
            return {'content': '', 'source': ''}
    
    def crawl(self, url, output_file='news.csv', max_news=50):
        """爬取新闻并保存到CSV文件"""
        print(f"开始爬取新闻: {url}")
        news_list = self.get_news_list(url)
        
        # 限制爬取数量
        news_list = news_list[:max_news]
        
        # 保存到CSV文件
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([''])
            
            for i, news in enumerate(news_list):
                print(f"爬取第{i+1}/{len(news_list)}条新闻: {news['title']}")
                # 获取新闻内容
                content_data = self.get_news_content(news['link'])
                # 写入CSV
                writer.writerow([
                    news['title']
                ])
                # 避免请求过于频繁
                time.sleep(1)
        
        print(f"爬取完成，共获取{len(news_list)}条新闻，保存到{output_file}")

if __name__ == "__main__":
    crawler = NewsCrawler()
    # 爬取新浪新闻首页
    crawler.crawl('https://news.sina.com.cn/', 'sina_news.csv', max_news=20)