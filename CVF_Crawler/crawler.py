
import requests
from bs4 import BeautifulSoup
import time
import os
import re

def url_join(comp):
    comp = [i.strip('/') for i in comp]
    return '/'.join(comp)

class Crawler():
    def __init__(self,url,saved_path,header=None):
        self.url = url
        self.header = header
        self.save_path = saved_path
        os.makedirs(saved_path,exist_ok=True)

    def parse(self,year_list,mode='train'):
        availble_conf = self._parse_menu(url_join([self.url,'menu.py']))
        availble_conf = [i for i in availble_conf if i[1] in year_list]
        conf_urls = [url_join([self.url,i[2]['conference']]) for i in availble_conf]
        work_urls = [url_join([self.url,i[2]['workshop']]) for i in availble_conf]

        # conf_save_path = os.path.join(self.save_path,mode,'conference')
        # os.makedirs(conf_save_path,exist_ok=True)
        # for i in conf_urls:
        #     paper_list = self._parse_papers(i)
        #     for j in paper_list:
        #         self._save_file(j,conf_save_path)
        #         time.sleep(2)

        workshop_save_path = os.path.join(self.save_path,mode,'workshop')
        os.makedirs(workshop_save_path,exist_ok=True)
        for page_urls in work_urls:
            work_shop_pages = self._parse_wokshop_page(page_urls)
            for i in work_shop_pages:
                paper_list = self._parse_papers(i)
                for j in paper_list:
                    self._save_file(j,workshop_save_path)
                    time.sleep(2)

        return

    def _parse_menu(self,menu_link):
        r = requests.get(menu_link)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        x = soup.find(id='content').dl.find_all(name='dd')

        def get_single(soup_item):
            conf_name,pub_year = re.split('[ ,]',soup_item.text.strip())[:2]
            href_list = soup_item.find_all('a',href=True)
            url_dict = {'conference':href_list[0]['href'],'workshop':href_list[1]['href']}
            return conf_name,int(pub_year),url_dict

        conf_list = [get_single(i) for i in x]
        return conf_list

    def _parse_papers(self,conf_link):
        r = requests.get(conf_link)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser').find(id='content').find_all('a',href=True)
        paper_urls = []
        for x in soup:
            if x.text == 'pdf':
                paper_urls.append(url_join([self.url,x['href']]))
        return paper_urls

    def _save_file(self,url,save_path):
        try:
            pdf_name = url.split('/')[-1]
            with open(os.path.join(save_path,pdf_name),'wb') as f:
                content = requests.get(url=url,stream=True)
                for chunk in content.iter_content(4096):
                    if chunk:
                        f.write(chunk)
                print(f'Successfully download {pdf_name}')
            return 1
        except:
            print(f'Failed while parsing from {url}!')
            return 0

    def _parse_wokshop_page(self,page_urls):
        r = requests.get(page_urls)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser').find(id='content').dl.find_all('a',href=True)
        subpage_list = [i['href'] for i in soup if 'menu.py' not in i['href']]
        sub_url = '/'.join(page_urls.split('/')[:-1])
        subpage_list = [url_join([sub_url,i]) for i in subpage_list]
        return subpage_list

if __name__=='__main__':
    main_link = 'http://openaccess.thecvf.com'
    cvf_crawler = Crawler(main_link,'./dataset')
    cvf_crawler.parse([2013,2014,2015,2016,2017],'train')
    cvf_crawler.parse([2018],'test')
