import requests
from bs4 import BeautifulSoup
import html


# Funkcja do pobierania linków z kategorii
def get_category_links(category):
    url = f'https://pl.wikipedia.org/wiki/Kategoria:{category}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        section = soup.find("div", class_="mw-category mw-category-columns")
        return [a['href'] for a in section.find_all("a")][:2]
    else:
        print(f"Error: {response.status_code}")
        return []


# Funkcja do pobierania danych artykułu
def get_article_data(article_link):
    url = f'https://pl.wikipedia.org{article_link}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find("div", class_="mw-body-content")

        # Internal links (first 5)
        internal_links = [a['title'] for a in content_div.find_all('a', href=True)
                          if a['href'].startswith('/wiki/') and ':' not in a['href'][6:]]
        internal_links_summary = " | ".join(internal_links[:5])

        # Image URLs (first 3)
        images = [img['src'] for img in content_div.find_all('img') if '/wiki/' not in img['src']][:3]
        images_summary = " | ".join(images) if images else ""

        # External sources (first 3)
        refs_div = soup.find("div", class_="mw-references-wrap mw-references-columns")
        if refs_div is None:
            refs_div = soup.find("div", class_="do-not-make-smaller refsection")

        external_links = []
        if refs_div:
            ref_items = refs_div.find_all("li")
            for item in ref_items[:3]:
                ref_links = item.find_all("span", class_="reference-text")
                for link in ref_links:
                    external_links.extend([a['href'] for a in link.find_all("a", href=True) if "http" in a['href']])

        external_links_summary = " | ".join([html.escape(link) for link in external_links[:3]])

        # Categories
        category_section = soup.find("div", class_="mw-normal-catlinks")
        categories = [a.text.strip() for a in category_section.find_all("a")][:3] if category_section else []
        categories_summary = " | ".join(categories)

        # Return gathered data
        return [internal_links_summary, images_summary, external_links_summary, categories_summary]

    else:
        print(f"Error: {response.status_code}")
        return []


# Funkcja główna
def main():
    category = input().replace(" ", "_")

    links = get_category_links(category)
    for link in links:
        data = get_article_data(link)
        for item in data:
            print(item)


# Uruchomienie programu
if __name__ == "__main__":
    main()