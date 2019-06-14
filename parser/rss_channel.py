class RssChannel:

    def __init__(self, title, url, description, items):
        self.title = title
        self.url = url
        self.description = description
        self.rss_items = self._parse_items(items)

    def _parse_items(self, items):
        rss_items = []
        for item in items:
            title = item['title']
            link = item['link']
            summary = item['summary']
            published = item['published']
            author = item['author']
            rss_items.append(RssItem(title, link, summary, published, author))
        return rss_items


class RssItem:

    def __init__(self, title, link, summary, published, author):
        self.title = title
        self.link = link
        self.summary = summary
        self.published = published
        self.author = author
