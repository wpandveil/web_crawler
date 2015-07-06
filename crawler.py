#coding:gbk
import sys
import time
import urllib2
import StringIO
from lxml import etree
import random
import lxml.html

"""
download html
"""
def download_html(url):
	html = ""
	try:
		time.sleep(random.randint(1, 2))
		req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) \
		AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept':'text/html;q=0.9,*/*;q=0.8',
		'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding':'gzip',
		'Connection':'close',
		'Referer':None
		}
		req_timeout = 10
		req = urllib2.Request(url, None, req_header)
		response = urllib2.urlopen(req, None, req_timeout)
		html = response.read()
		html = html.replace("&", "&amp;")
		#html = html.replace("xmlns", "id")
		#html = html.replace("id:fb", "class")
		return html
	except:
		return ""


"""
parse html use xpath element
"""
def parse_xpath_value(xpath_element, html):
	try:
		#f = StringIO.StringIO(html)
		#tree = etree.parse(f)
		tree = lxml.html.fromstring(html)
		r = tree.xpath(xpath_element)
		return r
	except:
		return []


"""
parse journal total num
journal_num_str example: "301-328 of 328 results"
"""
def parse_journal_num(journal_num_str):
	begin_pos = journal_num_str.find("of") + 2
	end_pos = journal_num_str.find("results")
	try:
		journal_num = journal_num_str[begin_pos : end_pos]
		return int(journal_num.replace(",", ""))
	except:
		return -1


def main():
	area_id_dict = {
			"multidisciplinary":"1",
			"computer science":"2",
			"arts & humanities":"3",
			"biology":"4",
			"chemistry":"5",
			"medicine":"6",
			"economics & business":"7",
			"engineering":"8",
			"environmental sciences":"9",
			"geosciences":"10",
			"material science":"12",
			"mathematics":"15",
			"agriculture science":"16",
			"physics":"19",
			"social science":"22"
			}
	#area_id_dict = {
	#		"computer science":"2"
	#		}
	## for keyword
	ori_url = "http://academic.research.microsoft.com/RankList?entitytype=8&topDomainID=%s&subDomainID=0&last=0&start=%d&end=%d"
	## for journal
	#ori_url = "http://academic.research.microsoft.com/RankList?entitytype=4&topDomainID=%s&subDomainID=0&last=0&start=%d&end=%d"
	for area in area_id_dict:
		begin_num = 1
		end_num = 100
		total_num = 0
		while begin_num == 1 or begin_num < total_num:
			url = ori_url % (area_id_dict[area], begin_num, end_num)
			print >> sys.stderr, url
			html = download_html(url)
			if begin_num == 1:
				journal_num_xpath = "//div/div/div/div/span/span/text()"
				journal_num_list = parse_xpath_value(journal_num_xpath, html)
				if len(journal_num_list) < 1:
					print >> sys.stderr, "journal num error"
				else:
					journal_num = parse_journal_num(journal_num_list[0])
					total_num = journal_num
					print >> sys.stderr, area + "\t" + str(total_num)
			journal_xpath = "//tbody/tr/td/a/text()"
			journal_list = parse_xpath_value(journal_xpath, html)
			try:
				print area + "\t" + "\t".join(journal_list)
			except:
				print >> sys.stderr, "ERROR" + "\t" + url
				pass
			begin_num += 100
			end_num += 100


if __name__ == "__main__":
	main()
