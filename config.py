"""Configuration file for picopaper blog"""

BLOG_TITLE = "Christophers Blog"
BLOG_DESCRIPTION = "we like simple."
THEME = "dark"

# Exclude specific feeds from the main page (they'll still have their own /feed/name/ pages)
EXCLUDE_FEEDS_FROM_MAIN = ['draft','private']  # e.g., ['python', 'drafts']

# Navigation bar items - list of dictionaries with 'text' and 'url' keys
NAVBAR_ITEMS = [
    {'text': 'Home', 'url': '/'},
    {'text': 'About', 'url': '/about/'}
]

