import requests
from bs4 import BeautifulSoup
import json
import time
import random
import os

BASE_URL = "https://traya.health"
COLLECTION_URL = "https://traya.health/collections/all-products"
OUTPUT_FILE = "data/products.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_product_links():
    print(f"Fetching product list from {COLLECTION_URL}...")
    response = requests.get(COLLECTION_URL, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch collection page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    links = []
    
    # Select product links - this might need adjustment based on actual list page structure
    # Based on read_url_content, it seems standard. 
    # Common Shopify pattern: .grid-view-item__link or a[href*='/products/']
    
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/products/" in href and "collections" not in href:
            full_url = BASE_URL + href if href.startswith("/") else href
            if full_url not in links:
                links.append(full_url)
    
    print(f"Found {len(links)} potential product links.")
    return list(set(links)) # Deduplicate

def scrape_product(url):
    print(f"Scraping {url}...")
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Failed to fetch {url}")
            return None
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Title
        title_tag = soup.select_one("h1.product__title, .product-single__title, h1")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown Product"
        
        # Price
        price_tag = soup.select_one(".price-item--regular .money, .price__regular .price-item--regular, .product-single__price .money, .price .money")
        price = price_tag.get_text(strip=True) if price_tag else "0"
        
        # Description
        # Strategy: Look for p tag after h1, or generic description class
        description = ""
        desc_tag = soup.select_one(".product__description p, .product-single__description p")
        if desc_tag:
            description = desc_tag.get_text(strip=True)
        else:
            # Fallback: try next sibling of title
            if title_tag:
                next_sib = title_tag.find_next_sibling("p")
                if next_sib:
                    description = next_sib.get_text(strip=True)
        
        # Image
        image_url = ""
        img_tag = soup.select_one(".product__media-wrapper img, .product-single__photo img, .product-image-main img")
        if img_tag:
            src = img_tag.get("src") or img_tag.get("data-src")
            if src:
                image_url = "https:" + src if src.startswith("//") else src
        
        # Category (Breadcrumbs)
        category = "General"
        breadcrumb_links = soup.select(".breadcrumb a, .breadcrumbs a, nav[aria-label='Breadcrumb'] a")
        if breadcrumb_links:
            # Usually Home > Category > Product
            # We take the second one if available, else the first
            if len(breadcrumb_links) > 1:
                category = breadcrumb_links[1].get_text(strip=True)
            elif len(breadcrumb_links) > 0:
                category = breadcrumb_links[0].get_text(strip=True)

        # Features
        # Hard to scrape reliably as noted, but let's try to grab list items in description area
        features = []
        feature_tags = soup.select(".product-usp-item p, .product-usp-item span, .product-features li")
        for ft in feature_tags:
            text = ft.get_text(strip=True)
            if text and len(text) > 3:
                features.append(text)
        
        # If no features found, try to extract from description text if it contains bullets
        if not features and description:
            if "•" in description:
                parts = description.split("•")
                features = [p.strip() for p in parts if len(p.strip()) > 3]

        return {
            "title": title,
            "price": price,
            "description": description,
            "features": features,
            "image_url": image_url,
            "category": category,
            "url": url
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def main():
    links = get_product_links()
    products = []
    
    # Limit to 30 to be safe
    target_count = 30
    count = 0
    
    for link in links:
        if count >= target_count:
            break
        
        product = scrape_product(link)
        if product and product["title"] != "Unknown Product":
            products.append(product)
            count += 1
            time.sleep(random.uniform(1, 3)) # Be polite
            
    # Ensure directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    
    print(f"Scraped {len(products)} products. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
