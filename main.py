import requests
from bs4 import BeautifulSoup
import html

def get_articles(cat_name):
    url = f'https://pl.wikipedia.org/wiki/Kategoria:{cat_name}'
    res = requests.get(url)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        sec = soup.find("div", class_="mw-category mw-category-columns")
        if sec:
            return [link['href'] for link in sec.find_all("a")[:2]]
    else:
        print(f"Error: {res.status_code}")
    return []

def get_article_data(article_path):
    url = f'https://pl.wikipedia.org{article_path}'
    res = requests.get(url)

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        content = soup.find("div", class_="mw-body-content")

        # Zmieniony warunek: wykluczamy "Kategorie" oraz "Kategoria"
        internal = [a['title'] for a in content.find_all('a', href=True)
                    if a['href'].startswith('/wiki/') and ':' not in a['href'][6:] and a['title'] not in ["Kategorie", "Kategoria"]]
        internal_summary = " | ".join(internal[:5])

        images = [img['src'] for img in content.find_all('img') if '/wiki/' not in img['src']][:3]
        images_summary = " | ".join(images)

        refs = soup.find("div", class_="mw-references-wrap mw-references-columns") or \
               soup.find("div", class_="do-not-make-smaller refsection")

        external = []
        if refs:
            for item in refs.find_all("li"):
                for ref in item.find_all("span", class_="reference-text"):
                    for a in ref.find_all("a", href=True):
                        if "http" in a['href']:
                            external.append(html.escape(a['href']))
                            if len(external) == 3:
                                break
                    if len(external) == 3:
                        break
                if len(external) == 3:
                    break

        external_summary = " | ".join(external)

        cat_sec = soup.find("div", class_="mw-normal-catlinks")
        categories = [a.text.strip() for a in cat_sec.find_all("a")[:4] if a.text.strip() not in ["Kategorie", "Kategoria"]] if cat_sec else []
        categories_summary = " | ".join(categories)

        return [internal_summary, images_summary, external_summary, categories_summary]
    else:
        print(f"Error: {res.status_code}")
    return []

def display_data(category):
    articles = get_articles(category)
    for path in articles:
        article_info = get_article_data(path)
        
        for section in article_info:
            print(section)
    
if __name__ == "__main__":
    cat = input("Enter category name: ").replace(" ", "_")
    display_data(cat)