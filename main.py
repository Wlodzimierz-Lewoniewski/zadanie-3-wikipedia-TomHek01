import re
import requests

def fetch_html(url):
    """Pobiera kod HTML strony pod danym URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""

def parse_article_page(html):
    """Analizuje HTML artykułu i zwraca wymagane informacje."""
    
    # Wewnętrzne odnośniki do innych artykułów Wikipedii (pierwsze 5)
    internal_links = re.findall(r'<a href="(/wiki/[^":#]+)"[^>]*>(.*?)</a>', html)
    internal_links = [link[1] for link in internal_links[:5]]
    
    # URL-e obrazków (pierwsze 3)
    image_urls = re.findall(r'<img[^>]+src="(//upload\.wikimedia\.org[^"]+)"', html)
    image_urls = ["https:" + url for url in image_urls[:3]]
    
    # URL-e zewnętrzne (pierwsze 3)
    external_links = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*class="external"', html)
    external_links = external_links[:3]
    
    # Kategorie (pierwsze 3)
    categories = re.findall(r'<a[^>]+href="/wiki/Kategoria:[^"]+"[^>]*>([^<]+)</a>', html)
    categories = categories[:3]

    return {
        "internal_links": internal_links or [""],
        "image_urls": image_urls or [""],
        "external_links": external_links or [""],
        "categories": categories or [""]
    }

def print_formatted_data(data):
    """Formatuje i drukuje dane zgodnie z wymaganiami."""
    
    # Wewnętrzne odnośniki
    print(" | ".join(data["internal_links"]))
    
    # URL-e obrazków
    print(" | ".join(data["image_urls"]))
    
    # URL-e zewnętrzne
    print(" | ".join(data["external_links"]))
    
    # Kategorie
    print(" | ".join(data["categories"]))

def main():
    # Odczytaj kategorię od użytkownika
    category = input().strip()
    category_url = f'https://pl.wikipedia.org/wiki/Kategoria:{category.replace(" ", "_")}'
    
    # Pobierz listę artykułów z kategorii
    html = fetch_html(category_url)
    article_links = re.findall(r'<a href="(/wiki/[^":#]+)"[^>]*>(.*?)</a>', html)
    article_urls = ['https://pl.wikipedia.org' + link[0] for link in article_links[:2]]
    
    # Przetwórz i wyświetl dane dla każdego artykułu
    for article_url in article_urls:
        article_html = fetch_html(article_url)
        data = parse_article_page(article_html)
        print_formatted_data(data)

main()
