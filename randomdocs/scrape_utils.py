import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

def get_articles_from_links(base_url, links, category_path=""):
    articles = []
    for link in links:
        api_title = link.text.strip()
        if link['href'].startswith("#"):
            full_url = base_url + category_path + link['href']
        else:
            full_url = base_url + link['href']
        article = {
            'title': api_title,
            'url': full_url
        }
        # ignore various non-tech related articles
        if 'utm_source' not in full_url:
            articles.append(article)
    return articles

def get_python_articles_from_links(base_url, category_path, links):
    articles = []
    for link in links:
        api_title = link.text.strip()
        directory = '/' + category_path.strip('/').split('/')[0] + '/'
        full_url = base_url + directory + link['href'].lstrip('/')
        article = {
            'title': api_title,
            'url': full_url
        }
        articles.append(article)
    return articles

def get_links_from_urls_with_selectors(base_url, urls_with_selectors):
    all_articles = []
    for category_path, selector in urls_with_selectors:
        url = f"{base_url}{category_path}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select(selector)
        articles = get_articles_from_links(base_url, links, category_path)
        all_articles.extend(articles)
    return all_articles

def get_links_from_mdn(category_path, selector):
    base_url = "https://developer.mozilla.org"
    urls_with_selectors = [(category_path, selector)]
    return get_links_from_urls_with_selectors(base_url, urls_with_selectors)

def get_mdn_webapi_links():
    return get_links_from_mdn("/en-US/docs/Web/API", ".section-content a")

def get_mdn_js_reference_links():
    base_url = "/en-US/docs/Web/JavaScript/Reference"
    endpoints = [
        "",
        "/Global_Objects",
        "/Global_Objects/Array",
        "/Global_Objects/String",
        "/Global_Objects/Set",
        "/Global_Objects/Object",
        "/Global_Objects/Symbol",
        "/Global_Objects/Number",
        "/Global_Objects/Math",
        "/Global_Objects/Function",
        "/Global_Objects/Map"
    ]
    all_links = []
    for endpoint in endpoints:
        all_links.extend(get_links_from_mdn(base_url + endpoint, ".sidebar-body a"))
    return all_links

def get_mdn_http_reference_links():
    return get_links_from_mdn("/en-US/docs/Web/HTTP", ".sidebar-body a")

def get_vue_links():
    base_url = "https://vuejs.org"
    urls_with_selectors = [
        ("/glossary/", ".table-of-contents a"),
        ("/guide/introduction.html", ".VPSidebar a"),
        ("/api/", "#api-index a"),
    ]
    return get_links_from_urls_with_selectors(base_url, urls_with_selectors)

def get_python_links():
    base_url = "https://docs.python.org/3.12"
    urls_with_selectors = [
        ("/library/index.html", ".toctree-wrapper a"),
        ("/reference/index.html", ".toctree-wrapper a"),
        ("/howto/index.html", ".toctree-wrapper a"),
    ]

    all_articles = []
    for category_path, selector in urls_with_selectors:
        url = f"{base_url}{category_path}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select(selector)
        articles = get_python_articles_from_links(base_url, category_path, links)
        all_articles.extend(articles)
    return all_articles

def get_links_from_wikipedia_categories(categories):
    base_url = "https://en.wikipedia.org/w/api.php"
    all_articles = []
    excluded_articles = ["Rhyme Time Town"]

    def fetch_category(category):
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{category}",
            "cmlimit": 500,
            "format": "json"
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        for member in data['query']['categorymembers']:
            title = member['title']
            if member['ns'] == 0 and title not in excluded_articles:
                link = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                all_articles.append({"title": title, "url": link})

    for category in categories:
        fetch_category(category)

    return all_articles

def get_30_seconds_of_code_links(category):
    base_url = "https://www.30secondsofcode.org"
    current_url = f'{base_url}/{category}/p/1/'
    articles = []

    while current_url:
        response = requests.get(current_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for card in soup.select(".card"):
            card_title_element = card.select_one("h3")
            if card_title_element:
                title = card_title_element.text.strip()
                link = base_url + card.select_one("h3 a")['href']
                articles.append({"title": title, "url": link})
        next_button = soup.select_one(".icon-chevron-right")
        if next_button:
            current_url = base_url + next_button['href']
        else:
            current_url = None

    return articles

def get_django_usage_links():
    scraped_articles = []
    BASE_URL = 'https://django.readthedocs.io/en/stable/'
    URL = 'https://django.readthedocs.io/en/stable/contents.html'
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_content = soup.select_one('.toctree-wrapper ul')
    articles = main_content.find_all('a')
    for article in articles:
        link = article['href']
        full_link = urljoin(BASE_URL, link)
        title = article.get_text()
        scraped_articles.append({"title": title, "url": full_link})
    return scraped_articles

def get_main_typescript_topics():
    base_url = "https://www.typescriptlang.org"
    doc_url = f"{base_url}/docs/"
    response = requests.get(doc_url)
    soup = BeautifulSoup(response.content, 'lxml')
    main_topics = soup.select(".item a")
    links = [{"title": topic.text.strip(), "url": urljoin(base_url, topic["href"])} for topic in main_topics]
    return links

def get_subtopics_for_topic(url, selector):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    subtopics_section = soup.select_one(selector)
    if not subtopics_section:
        return []
    subtopics = subtopics_section.select("a")
    links = [{"title": topic.text.strip(), "url": urljoin(url, topic["href"])} for topic in subtopics]
    return links

def scrape_typescript_docs():
    main_topics = get_main_typescript_topics()
    all_links = []
    for topic in main_topics:
        all_links.append(topic)
        subtopics = get_subtopics_for_topic(topic["url"], "aside.toc nav")
        all_links.extend(subtopics)
    return all_links

def get_postgresql_main_topics():
    base_url = "https://www.postgresql.org/docs/current/"
    response = requests.get(base_url + "index.html")
    soup = BeautifulSoup(response.content, 'html.parser')
    main_topics = soup.select(".toc a")
    links = [{"title": topic.text.strip(), "url": urljoin(base_url, topic["href"])} for topic in main_topics]
    return links

def scrape_postgresql_docs():
    main_topics = get_postgresql_main_topics()
    all_links = []
    for topic in main_topics:
        all_links.append(topic)
        subtopics = get_subtopics_for_topic(topic["url"], ".toc")
        all_links.extend(subtopics)
    return all_links

def get_links_from_programiz(base_url, paths_and_selectors):
    all_articles = []
    for path, selector in paths_and_selectors:
        if path.startswith("/"):
            url = base_url + path
        else:
            url = base_url + "/" + path
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.select(selector)
        articles = get_articles_from_links(base_url, links)
        all_articles.extend(articles)
    return all_articles

def get_programiz_python_methods():
    base_url = "https://www.programiz.com"
    paths_and_selectors = [("python-programming/methods", ".reference-data--row a")]
    return get_links_from_programiz(base_url, paths_and_selectors)

def get_programiz_python_topics():
    base_url = "https://www.programiz.com"
    paths_and_selectors = [("python-programming", ".right-bar a")]
    return get_links_from_programiz(base_url, paths_and_selectors)

def get_programiz_python_examples():
    base_url = "https://www.programiz.com"
    paths_and_selectors = [("python-programming/examples", ".tabbed-content__right a")]
    return get_links_from_programiz(base_url, paths_and_selectors)

def scrape_programiz_python():
    all_links = []
    all_links.extend(get_programiz_python_methods())
    all_links.extend(get_programiz_python_topics())
    all_links.extend(get_programiz_python_examples())
    return all_links

def get_programiz_javascript():
    base_url = "https://www.programiz.com"
    paths_and_selectors = [("/javascript", ".right-bar a")]
    return get_links_from_programiz(base_url, paths_and_selectors)

def get_programiz_javascript_examples():
    base_url = "https://www.programiz.com"
    paths_and_selectors = [("/javascript/examples", ".tabbed-content__right a")]
    return get_links_from_programiz(base_url, paths_and_selectors)

def get_programiz_python_references():
    base_url = "https://www.programiz.com"
    paths_and_selectors = [("javascript/library", ".reference-data__row__title a")]
    return get_links_from_programiz(base_url, paths_and_selectors)

def scrape_programiz_javascript():
    all_links = []
    all_links.extend(get_programiz_javascript())
    all_links.extend(get_programiz_javascript_examples())
    all_links.extend(get_programiz_python_references())
    return all_links

def scrape_css_tricks_archives():
    base_url = "https://css-tricks.com/archives/page/"
    all_articles = []
    # not the entire archive
    for page_num in range(1, 50):
        url = base_url + str(page_num) + "/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.select(".article-article h2 a")
        for article in articles:
            title = article.text.strip()
            link = article["href"]
            if title:
                all_articles.append({"title": title, "url": link})
        time.sleep(1)
    return all_articles
