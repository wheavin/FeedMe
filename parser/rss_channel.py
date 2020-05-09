#!/usr/bin/python3
"""
RSS feed channel.
"""


def _validate_item(item):
    elements = ["title", "link", "summary"]
    if not all(element in item for element in elements) or not all(item[element] for element in elements):
        raise RssItemError("Invalid RSS channel entry data: %s" % item)


def _parse_items(items):
    rss_items = []
    if not items:
        rss_items.append("RSS feed is empty")
    for item in items:
        _validate_item(item)
        title = item['title']
        link = item['link']
        summary = item['summary']
        published = _extract_key(item=item, key="published", alternate="updated")
        author = _extract_key(item=item, key="author", alternate=None)
        rss_item = RssItem(title, link, summary, published, author)
        rss_items.append(rss_item.format_item_content())
    return rss_items


def _extract_key(item, key, alternate):
    try:
        value = item[key]
    except KeyError:
        try:
            value = item[alternate] if alternate else None
        except KeyError:
            value = None
    return value


class RssChannel:
    """
    Represents an RSS feed channel.
    """

    def __init__(self, title, url, description, items):
        self.title = title
        self.url = url
        self.description = description
        self.rss_items = _parse_items(items)

    def format_feed_content(self):
        """
        Formats feed content is a clean and readable manner.
        :return: the formatted feed content.
        """
        return "<h2>{title}</h2>" \
               "<p>{summary}</p>" \
               "{rss_items}" \
            .format(title=self.title, url=self.url, summary=self.description, rss_items="\n\n".join(self.rss_items))


class RssItem:
    """
    Represents an RSS feed channel item.
    """

    def __init__(self, title, link, summary, published, author):
        self.title = title
        self.link = link
        self.summary = summary
        self.published = published
        self.author = author

    def format_item_content(self):
        """
        Formats feed item content in a clean and readable manner.
        :return: the formatted item content.
        """
        return "<h3>{title}</h3>" \
               "<p><a href=\"{link}\" target=\"_blank\">{link}</a></p>" \
               "<p>{summary}</p>" \
               "<p>{published} - {author}</p>" \
            .format(title=self.title, link=self.link, summary=self.summary, published=self.published,
                    author=self.author)


class RssItemError(Exception):
    """
    Exception is thrown when feed item element missing or expected data missing.
    """

    def __init__(self, message):
        super(RssItemError, self).__init__(message)
        self.message = message
