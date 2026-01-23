#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS 源可用性检测脚本
"""
import requests
import sys
from urllib.parse import urlparse

# 设置Windows终端编码
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

RSS_SOURCES = {
    "Hacker News": "https://hnrss.org/frontpage",
    "阮一峰": "http://www.ruanyifeng.com/blog/atom.xml",

    # 游戏
    "TapTap": "https://www.taptap.cn/moment/rss/1",
    "机核": "https://www.gcores.com/rss",
    "3DMGame": "https://www.3dmgame.com/rss/news.xml",
    "Steam新品": "https://store.steampowered.com/feeds/newreleases/",

    # AI
    "36氪": "https://36kr.com/feed",
    "IT之家": "https://www.ithome.com/rss/",
    "量子位": "https://www.qbitai.com/feed",
    "机器之心": "https://www.jiqizhixin.com/rss",
    "OpenAI Blog": "https://openai.com/news/rss.xml",
    "Anthropic Blog": "https://www.anthropic.com/news/rss.xml",

    # 科技
    "少数派": "https://sspai.com/feed",
    "Product Hunt": "https://www.producthunt.com/posts.rss",
    "V2EX": "https://www.v2ex.com/index.xml",

    # 社交媒体
    "X 游戏趋势": "https://nitter.net/search/gaming%20news%20-%20from%40gaming/rss",
    "X AI讨论": "https://nitter.net/search/ai%20news%20-%20from%04OpenAI/rss",
    "YouTube 游戏": "https://www.youtube.com/rss/feed/featured",
    "Reddit gaming": "https://www.reddit.com/r/gaming/hot/.rss",
    "Reddit Games": "https://www.reddit.com/r/Games/hot/.rss",
    "Reddit AI": "https://www.reddit.com/r/artificial/hot/.rss",
    "Reddit ML": "https://www.reddit.com/r/MachineLearning/hot/.rss",
    "小红书": "https://xiaohongshu-search-api.vercel.app/api/rss",
}

def check_rss(url, timeout=10):
    """检查RSS源是否可用"""
    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if 'xml' in content_type.lower() or 'rss' in content_type.lower() or 'atom' in content_type.lower():
                return True, "✅ OK"
            else:
                return True, f"⚠️ 内容类型: {content_type}"
        else:
            return False, f"❌ HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "❌ 超时"
    except requests.exceptions.ConnectionError:
        return False, "❌ 连接失败"
    except Exception as e:
        return False, f"❌ {str(e)[:30]}"

def main():
    print("=" * 60)
    print("RSS 源可用性检测")
    print("=" * 60)

    results = {"ok": [], "warn": [], "fail": []}

    for name, url in RSS_SOURCES.items():
        success, msg = check_rss(url)
        status_icon = "✅" if success and "OK" in msg else "⚠️" if success else "❌"

        print(f"{status_icon} {name:20s} {msg}")

        if success and "OK" in msg:
            results["ok"].append(name)
        elif success:
            results["warn"].append(name)
        else:
            results["fail"].append(name)

    print("\n" + "=" * 60)
    print("统计结果")
    print("=" * 60)
    print(f"✅ 正常 ({len(results['ok'])}): {', '.join(results['ok'])}")
    if results['warn']:
        print(f"⚠️  警告 ({len(results['warn'])}): {', '.join(results['warn'])}")
    if results['fail']:
        print(f"❌ 失败 ({len(results['fail'])}): {', '.join(results['fail'])}")

    print(f"\n总计: {len(RSS_SOURCES)} 个源, {len(results['ok'])} 个可用")

if __name__ == "__main__":
    main()
