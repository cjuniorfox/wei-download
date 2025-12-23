from pyquery import PyQuery as pq
import gdown
import os
import argparse
import re

def read_urls(base_url):
    content = pq(url=base_url)
    post_content = content.find('div.post-content p')
    urls = [
        {
            'title': item.find("strong").text(),
            'url': [
                {
                    'text': a.text(),
                    'link':a.attr("href")
                } for a in item.find("a").items()]
        }
        for item in post_content.items()
    ]
    return [url for url in urls if url['title'].startswith("EP")]

def filter_google_drive(urls):
    filtered_urls = []
    for url in urls:
        google_drive_links = [
            link for link in url['url'] if 'drive.google.com' in link['link']
        ]
        if google_drive_links:
            filtered_urls.append({
                'title': url['title'],
                'url': google_drive_links
            })
    return filtered_urls

def download_file_from_google_drive(file_id, ):
    path = gdown.download(id=file_id, quiet=False, fuzzy=True)
    return path

def extract_file_id(google_drive_url):
    if "id=" in google_drive_url:
        return google_drive_url.split("id=")[1].split("&")[0]
    elif "/d/" in google_drive_url:
        return google_drive_url.split("/d/")[1].split("/")[0]
    return None

def prepare_download_list(urls):
    download_list = []
    for url in urls:
        for link in url['url']:
            if 'drive.google.com' in link['link']:
                file_id = extract_file_id(link['link'])
                download_list.append({
                    'title': url['title'],
                    'file_id': file_id
                })
    return download_list

def rename_donwloaded_file(path, season):
    try:
        filename = os.path.basename(path) if path else None
        if not filename:
            return
        
        # Remove "WEI FANSUB -" prefix
        cleaned = re.sub(r"^WEI FANSUB\s*-\s*", "", filename, flags=re.IGNORECASE)
        
        # Match pattern: <title>..EP[0-9][0-9].<ext>
        match = re.match(r"^(.+?)\s*EP(\d{2})\.(.+)$", cleaned, flags=re.IGNORECASE)
        if not match:
            print(f"Could not parse filename: {filename}")
            return
        
        title = match.group(1).strip()
        episode = match.group(2)
        extension = match.group(3)
        
        # Normalize title: replace underscores/dashes with spaces, capitalize each word
        title = re.sub(r"[_-]+", " ", title)
        title = " ".join([word.capitalize() for word in title.split()])
    except Exception as e:
        print(f"Error parsing file {filename}: {e}")
        return
        
    # Create new filename
    new_filename = f"{title} - S{str(season).zfill(2)}E{episode} Wei Fansubs.{extension}"
    
    # Create directory with title if not exists
    directory = title
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Move and rename file
    if filename and path:
        new_path = os.path.join(os.path.join(os.path.dirname(path), directory), new_filename)
        os.rename(path, new_path)

def download_files(download_list, season=1):
    for item in download_list:
        path = download_file_from_google_drive(item['file_id'])
        rename_donwloaded_file(path, season)        
        
def delete_zip_file(file_path):
    os.remove(file_path)
    
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Download files from Weifansub Google Drive links.")
    argparser.add_argument("url", type=str, help="The base URL of the Weifansub post.")
    argparser.add_argument("--season", "-s", type=int, default=1, help="Season number for renaming files.")
    args = argparser.parse_args()
    base_url = args.url
    #
    urls = read_urls(base_url)
    filtered = filter_google_drive(urls)
    download_list = prepare_download_list(filtered)
    download_files(download_list, season=args.season)
    print("All files downloaded.")