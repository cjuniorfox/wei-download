from pyquery import PyQuery as pq
import gdown
import json
import os
import argparse

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

def rename_donwloaded_file(item, path):
    try:
        filename = os.path.basename(path) if path else None
        '''WEI FANSUB - MY_DEAR_DONOVAN_EP01.mp4'''
        #1. Remove prefix
        if filename and filename.startswith("WEI FANSUB - "):
            filename = filename.replace("WEI FANSUB - ", "")
        #2. Get episode title
        title=filename.split("_ EP")[0]
        #3. Get episode number from title
        episode=filename.split("_ EP")[1].split('.')[0]
        #4. Get file extension
        extension=filename.split("_ EP")[1].split('.')[1]
        #5. Replace underscores with spaces
        if title:
            title = title.replace("_", " ")
        #6. Capitalize
        if title:
            title = title.capitalize()
    except Exception as e:
        print(f"Error renaming file {filename}: {e}")
        return
        
    # 7. Create new filename
    new_filename = f"{title} - S01E{episode.zfill(2)}.{extension}"
    
    # 8. Create directory with title if not exists
    directory = title
    if not os.path.exists(directory):
        os.makedirs(directory)
    # 8. Move and Rename file
    if filename and path:
        new_path = os.path.join(os.path.join(os.path.dirname(path), directory), new_filename)
        os.rename(path, new_path)

def download_files(download_list):
    for item in download_list:
        path = download_file_from_google_drive(item['file_id'])
        rename_donwloaded_file(item, path)        
        
def delete_zip_file(file_path):
    os.remove(file_path)
    
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Download files from Weifansub Google Drive links.")
    argparser.add_argument("url", type=str, help="The base URL of the Weifansub post.")
    args = argparser.parse_args()
    base_url = args.url
    #
    base_url = "https://weifansub.com.br/2022/08/15/my-dear-donovan/"
    urls = read_urls(base_url)
    filtered = filter_google_drive(urls)
    download_list = prepare_download_list(filtered)
    download_files(download_list)
    print(json.dumps(download_list, ensure_ascii=False, indent=4))