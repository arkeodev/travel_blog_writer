# Define a custom User-Agent
USER_AGENT = "TravelBlogWriterApp/1.0 (https://github.com/arkeodev/travel_blog_writer; arkeodev@gmail.com) Python/3.9"

def fetch_image(url):
    headers = {
        "User-Agent": USER_AGENT
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))
