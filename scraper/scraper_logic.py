import requests
from bs4 import BeautifulSoup
import re


import requests
from bs4 import BeautifulSoup
import re


def run_scraper(url, keywords, case_sensitive, prefix_suffix, deep_search, max_depth, scraped_urls=None, current_depth=0):
    if scraped_urls is None:
        scraped_urls = set()

    # Avoid re-scraping the same URL
    if url in scraped_urls:
        return []
    scraped_urls.add(url)

    results = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()

        if not case_sensitive:
            text = text.lower()

        for keyword in keywords:
            keyword = keyword.strip()
            if not case_sensitive:
                keyword = keyword.lower()

            if prefix_suffix:
                # Match only if the keyword is not directly followed or preceded by an alphanumeric character
                pattern = r'(?<!\w)' + re.escape(keyword) + r'(?!\w)'
            else:
                pattern = re.escape(keyword)

            matches = re.findall(pattern, text)
            if matches:
                results.append(
                    f"'{keyword}' found {len(matches)} times in {url}")

        if deep_search and current_depth < max_depth:
            # Find all links on the page
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('http'):
                    # Recursively scrape the linked page with increased depth
                    results += run_scraper(href, keywords, case_sensitive, prefix_suffix,
                                           deep_search, max_depth, scraped_urls, current_depth + 1)

    except requests.RequestException as e:
        results.append(f"Error accessing {url}: {str(e)}")

    return results
