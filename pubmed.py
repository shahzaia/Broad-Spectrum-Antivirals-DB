import requests
import scrapy
import pandas as pd
import csv
import os
# start_date = date.today()-timedelta(days=30)
# start_date = start_date.strftime('%Y/%m/%d')
# end_date = date.today().strftime('%Y/%m/%d')

csv_file = "pubmed.csv"
data = list()

if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    data = list(df['URL'])

file = open(csv_file, mode='a', newline='', encoding="utf-8")
writer = csv.writer(file)
if len(data) == 0:
    writer.writerow(['URL', 'Title', 'Author', 'Citation', 'PMID', 'Description'])

def parse(keyword, start_date, end_date,  pg_no=1):
    url = f"https://pubmed.ncbi.nlm.nih.gov/?term={keyword}&filter=dates.{start_date}-{end_date}&page={pg_no}"
    req = requests.get(url)
    response = scrapy.Selector(text=req.text)
    parse_articles(response)
    page = int(response.css("input.page-number::attr(value)").get(''))
    total_page = int(response.css("label.of-total-pages::text").get('').split()[1])

    if page < total_page:
        page += 1
        url = f"https://pubmed.ncbi.nlm.nih.gov/?term={keyword}&filter=dates.{start_date}-{end_date}&page={page}"
        req = requests.get(url)
        response = scrapy.Selector(text=req.text)
        parse_articles(response)
    file.close()


def parse_articles(response):
    articles = response.css("article.full-docsum")
    for article in articles:
        article_url = article.css('a.docsum-title::attr(href)').get('').strip('/')
        if len(data) > 1 and int(article_url) in data:
            continue
        title = " ".join(article.css('a.docsum-title *::text').getall()).strip()
        author_name = article.css("span.docsum-authors.full-authors::text").get('')
        journal_citation = article.css('span.docsum-journal-citation.full-journal-citation::text').get('')
        pmid = article.css("span.docsum-pmid::text").get('')
        desc = ' '.join(article.css("div.full-view-snippet::text").getall()).strip()
        writer.writerow([article_url, title, author_name, journal_citation, pmid, desc])

