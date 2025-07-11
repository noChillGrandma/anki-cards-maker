import requests
from bs4 import BeautifulSoup
import os

# List of Blogspot domains to scrape
blogs = [
    "mumminmatkat.blogspot.com",
    # add more blog domains here
]

SCRAPED_BLOGS_FILE = "scraped_blogs.txt"

def load_scraped_blogs():
    """Load the list of already scraped blogs from file"""
    if os.path.exists(SCRAPED_BLOGS_FILE):
        with open(SCRAPED_BLOGS_FILE, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_scraped_blog(blog_domain):
    """Add a blog domain to the scraped blogs list"""
    with open(SCRAPED_BLOGS_FILE, 'a', encoding='utf-8') as f:
        f.write(blog_domain + '\n')

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
    scraped_blogs = load_scraped_blogs()
    
    for blog in blogs:
        if blog in scraped_blogs:
            print(f"⏭️  Skipping {blog} (already scraped)")
            continue
            
        print(f"Processing {blog}...")
        try:
            entries = fetch_posts(blog)
            print(f"Found {len(entries)} posts from {blog}")
            
            blog_posts = []
            for entry in entries:
                # JSON feed uses 'content' or 'summary' for post body
                raw_html = entry.get("content", {}).get("$t") or entry.get("summary", {}).get("$t", "")
                if raw_html:
                    text = extract_text(raw_html)
                    if text.strip():  # Only add non-empty posts
                        blog_posts.append(text)
            
            if blog_posts:
                all_posts.extend(blog_posts)
                save_scraped_blog(blog)
                print(f"✅ Successfully scraped {len(blog_posts)} posts from {blog}")
            else:
                print(f"⚠️  No posts extracted from {blog}")
                
        except Exception as e:
            print(f"❌ Error processing {blog}: {e}")
    
    # Save all posts to text_input.txt
    if all_posts:
        with open("text_input.txt", "w", encoding="utf-8") as f:
            for post in all_posts:
                f.write(post + "\n\n")
        
        print(f"✅ Successfully saved {len(all_posts)} posts to text_input.txt")
    else:
        print("❌ No new posts were extracted")

if __name__ == "__main__":
    main()
