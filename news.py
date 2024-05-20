import os
import requests
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta


def _escape_md(text, is_url=False):
    chars_to_escape = ['[', ']', '*', '_']
    if not is_url:
        chars_to_escape.extend(['(', ')'])
    for char in chars_to_escape:
        text = text.replace(char, '\\' + char)
    return text


def fetch_and_convert_to_md(_url):
    print(f"Fetching and converting data from {_url}")
    response = requests.get(_url)
    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}")
        return []

    root = ET.fromstring(response.content)

    md_lines = []
    for item in root.findall('.//item'):
        title = _escape_md(item.find('title').text)
        link = _escape_md(item.find('link').text, is_url=True)
        date_str = item.find('pubDate').text.replace('GMT', '+0000')
        date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
        formatted_date = date.strftime("%d-%m-%Y")
        source = _escape_md(item.find('source').text if item.find('source') is not None else 'Unknown')

        md_lines.append((date, f"- [{title}]({link}) ({formatted_date}) - {source}"))

    return md_lines


def get_urls_for_last_months(_keyword, _months=8):
    print(f"Generating URLs for the last {_months} months")
    base_url = "https://news.google.com/rss/search"
    urls = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=_months * 30)

    while end_date > start_date:
        start_period = end_date.replace(day=1)
        end_period = (start_period - timedelta(days=1)).replace(day=1)
        url = f"{base_url}?q={_keyword}+after:{end_period.strftime('%Y-%m-%d')}+before:{start_period.strftime('%Y-%m-%d')}&hl=pl&gl=PL&ceid=PL:pl"
        urls.append(url)
        end_date = end_period

    return urls


def _save_news_to_monthly_files(_md_lines, _output_dir='result'):
    print("Saving news to monthly files")
    # Group news by month
    news_by_month = {}
    for date, line in _md_lines:
        _month = date.strftime("%Y-%m")
        if _month not in news_by_month:
            news_by_month[_month] = []
        news_by_month[_month].append(line)

    # Save news to monthly files
    for _month, lines in news_by_month.items():
        with open(os.path.join(_output_dir, f"{_month}.md"), 'w') as monthFile:
            monthFile.write("\n".join(lines))

    # Return sorted list of months
    return sorted(news_by_month.keys(), reverse=True)


if __name__ == "__main__":
    if not os.path.exists('result'):
        os.makedirs('result')
    keyword = input("Enter the keyword: ")
    months = int(input("Enter the number of months: "))
    urls = get_urls_for_last_months(keyword, months)

    all_md_lines = []
    for url in urls:
        all_md_lines.extend(fetch_and_convert_to_md(url))

    # Sort by date, most recent first
    all_md_lines.sort(key=lambda x: x[0], reverse=True)
    months = _save_news_to_monthly_files(all_md_lines, 'result')

    # Extract just the markdown lines
    markdown_content = "\n".join([line[1] for line in all_md_lines])

    with open('result/output.md', 'w') as file:
        for month in months:
            formatted_month = f"Publikacje w {month[5:7]}-{month[0:4]}"
            file.write(f"- [{formatted_month}]({month}.md)\n")

    print("Markdown content has been saved to result/output.md")
