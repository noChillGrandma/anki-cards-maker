import requests
from bs4 import BeautifulSoup

# List of Blogspot domains to scrape
blogs = [
    "vimma50.blogspot.com",
    # "example2.blogspot.com",
    # add more blog domains here
]

def fetch_posts(blog_domain):
    """
    Fetch ALL posts via the Blogspot JSON feed using pagination.
    """
    all_entries = []
    start_index = 1
    max_results = 150  # Maximum allowed by Blogspot API
    
    while True:
        url = f"https://{blog_domain}/feeds/posts/default?alt=json&max-results={max_results}&start-index={start_index}"
        print(f"  Fetching posts {start_index}-{start_index + max_results - 1}...")
        
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            entries = data.get("feed", {}).get("entry", [])
            if not entries:
                break  # No more posts
                
            all_entries.extend(entries)
            
            # Check if we got fewer posts than requested (means we reached the end)
            if len(entries) < max_results:
                break
                
            start_index += max_results
            
        except Exception as e:
            print(f"  Error fetching batch starting at {start_index}: {e}")
            break
    
    return all_entries

def extract_text(html_content):
    """
    Strip HTML tags and return plain text.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def main():
    all_posts = []
    
    for blog in blogs:
        print(f"Processing {blog}...")
        try:
            entries = fetch_posts(blog)
            print(f"Found {len(entries)} posts from {blog}")
            
            for entry in entries:
                # JSON feed uses 'content' or 'summary' for post body
                raw_html = entry.get("content", {}).get("$t") or entry.get("summary", {}).get("$t", "")
                if raw_html:
                    text = extract_text(raw_html)
                    if text.strip():  # Only add non-empty posts
                        all_posts.append(text)
        except Exception as e:
            print(f"Error processing {blog}: {e}")
    
    # Save all posts to file
    if all_posts:
        with open("scraped_blogposts.txt", "w", encoding="utf-8") as f:
            for post in all_posts:
                f.write(post + "\n\n")
        
        print(f"✅ Successfully saved {len(all_posts)} posts to scraped_blogposts.txt")
    else:
        print("❌ No posts were extracted")

if __name__ == "__main__":
    main()
