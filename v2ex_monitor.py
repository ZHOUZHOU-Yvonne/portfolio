"""
V2EX 外包节点监控 - 每30分钟抓取新帖，发现匹配项目自动生成回复话术
"""
import requests, re, json, os, time
from datetime import datetime

DATA_FILE = os.path.expanduser('~/.v2ex_posts.json')
OUTPUT_FILE = os.path.expanduser('~/Desktop/v2ex_leads.txt')
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

KEYWORDS = [
    'python', '爬虫', '小程序', 'api', '接口', '网站', '网页', '前端',
    '自动化', 'excel', 'pdf', '数据', '采集', '抓取', '后端',
    '全栈', '脚本', 'react', 'vue', 'node', 'javascript',
    '外包', '兼职', '私活', '接单', '短期', '远程',
    '电商', '支付', '跨境', 'ozon', '1688', '淘宝', '京东',
]

def fetch_posts():
    try:
        r = requests.get('https://www.v2ex.com/go/outsourcing', headers=HEADERS, timeout=15)
        titles = re.findall(r'<span class="item_title"><a[^>]*>(.*?)</a>', r.text)
        links = re.findall(r'<span class="item_title"><a href="([^"]+)"', r.text)
        posts = []
        for t, l in zip(titles, links):
            posts.append({
                'title': t.strip(),
                'url': f'https://www.v2ex.com{l}',
                'id': l.split('/')[-1].split('#')[0]
            })
        return posts
    except Exception as e:
        print(f"Fetch error: {e}")
        return []

def match_keywords(post):
    text = post['title'].lower()
    matched = [kw for kw in KEYWORDS if kw in text]
    return matched

def load_seen():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []

def save_seen(ids):
    with open(DATA_FILE, 'w') as f:
        json.dump(ids, f)

def generate_pitch(post, keywords):
    title = post['title']
    if '小程序' in title:
        return f"你好，看到你的小程序需求。我是独立开发者，做过多个小程序项目，3-5天交付，源码+部署+文档。方便聊聊需求？微信 zhouyajiezzz@gmail.com"
    elif any(kw in title.lower() for kw in ['python', '爬虫', '采集', '抓取']):
        return f"你好，Python爬虫/数据采集我可以做。之前做过电商、社交媒体等平台的数据采集。1-2天交付，方便发一下具体需求？"
    elif any(kw in title.lower() for kw in ['api', '接口', '对接']):
        return f"你好，API对接我可以做。之前接过1688、淘宝开放平台的项目。你这边具体要对接什么平台？"
    elif any(kw in title.lower() for kw in ['网站', '网页', '前端', '全栈']):
        return f"你好，网站开发我可以接。全栈开发，前端React/Vue，后端Python/Node。方便说说具体要做什么类型的网站？"
    else:
        return f"你好，看到你的需求。我是全栈独立开发者，可以接这个项目。方便聊聊具体细节？"

def main():
    posts = fetch_posts()
    if not posts:
        return

    seen = set(load_seen())
    new_leads = []

    for post in posts:
        if post['id'] in seen:
            continue
        seen.add(post['id'])

        keywords = match_keywords(post)
        if keywords and not any(kw in post['title'] for kw in ['[接单]', '[接單]']):
            # Skip posts from other freelancers advertising
            if re.search(r'\[接单\]|接单\|', post['title']):
                continue
            pitch = generate_pitch(post, keywords)
            new_leads.append({
                'title': post['title'],
                'url': post['url'],
                'keywords': keywords,
                'pitch': pitch,
                'time': datetime.now().isoformat()
            })

    save_seen(list(seen))

    if new_leads:
        with open(OUTPUT_FILE, 'a') as f:
            for lead in new_leads:
                f.write(f"\n{'='*60}\n")
                f.write(f"🔔 {lead['time']}\n")
                f.write(f"📌 {lead['title']}\n")
                f.write(f"🔗 {lead['url']}\n")
                f.write(f"🏷️ 匹配关键词: {', '.join(lead['keywords'])}\n")
                f.write(f"💬 回复话术:\n{lead['pitch']}\n")

        print(f"Found {len(new_leads)} new leads!")
    else:
        print(f"No new leads at {datetime.now().isoformat()}")

if __name__ == '__main__':
    main()
