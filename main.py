from bs4.element import Tag
import requests
from bs4 import BeautifulSoup
from functools import reduce

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47'
}
OWNER = 'tony11306'
BAHAMUT_DOMAIN = 'https://home.gamer.com.tw/'
BAHAMUT_BLOG_URL = BAHAMUT_DOMAIN + 'creation.php?owner=' + OWNER

BAHAMUT_BLOG_CREATION_API = f'https://api.gamer.com.tw/home/v1/creation_list.php?owner={OWNER}&page=1&keyword=0&type=kind1&search_type=&kind1=0&row=5'

STATIC_README = '''
### Hi there 👋. This is tony11306's github

- 📫 Contact me with this email: `tony20020507@gmail.com`
- 🐉 巴哈姆特小屋 / Bahamut home: [傳送門 Portal](https://home.gamer.com.tw/homeindex.php)，Will post some articles when having free time.
'''

def get_five_recent_post_new_version():
    CREATION_URL = 'https://home.gamer.com.tw/artwork.php?sn='
    response = requests.get(BAHAMUT_BLOG_CREATION_API, headers=HEADERS)
    response_json = response.json()
    def to_article_imfo(creation):
        return {
            'title': creation['title'],
            'brief': creation['content'],
            'url': CREATION_URL + creation['csn']
        }
    return list(map(to_article_imfo, response_json['data']['list']))

def get_five_recent_post():
    response = requests.get(url=BAHAMUT_BLOG_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, features='html.parser')
    def get_article_imfo(article: Tag): # recv a div that the class is "HOME-mainbox1b"
        return {
            'title': article.find('a', class_='TS1').text,
            'brief': article.find('span', class_='ST1').next_sibling.text.strip().replace('(繼續閱讀)', '').replace('\n', ' '),
            'url': BAHAMUT_DOMAIN + article.find('a', class_='TS1').attrs['href']
        }
    
    articles = soup.find('p', class_='HOME-toptag').find_next_siblings(limit=5)
    article_imfos = list(map(get_article_imfo, articles))

    return article_imfos

def update_readme(posts):
    readme_content = f'{STATIC_README}\n ## Recent posts in my blog\n'
    
    def reduce_posts_to_content(post1, post2):
        return post1 + post2
    readme_content += reduce(reduce_posts_to_content, map(lambda post: f'\n### [{post["title"]}]({post["url"]})\n> {post["brief"]}\n', posts))
    print(readme_content)

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)


if __name__ == '__main__':
    posts = get_five_recent_post_new_version()
    update_readme(posts)