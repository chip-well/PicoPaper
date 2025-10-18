# picopaper

A minimal static site generator for blogs built with Python 3 and Jinja2

- Status: alpha - expect many changes
- [Issue Tracker](https://git.uphillsecurity.com/cf7/picopaper/issues)
- Goals: keeping it simple and easy to understand
- Demo: [picopaper.com](https://picopaper.com/)

Show cases:
- [securitypending.com](https://securitypending.com/)

---

## Features

**Available**:
- Simple use, easy to understand and modify
- config file for settings
- Themes
- Long- and short form content
- Pages
- Static files
- separate feeds (used for categories, tagging, etc) `/feed/{tag}`
- exclusion of feeds from main feed (drafts or system notes)
- HTML anchors for headers

**Ideas**:
- RSS
- Dark mode
- logo
- custom error pages (404, etc)

**Not planned**:

---

## Usage

### Creating a new page or article

Put markdown file into `items` dir. **Important naming convention**:

```
2025-10-03_long_building-a-static-site-generator.md
2025-10-05_short_quick-update_draft.md
```

Format: `YYYY-MM-DD_type_slug[_feed].md`

- `2025-10-03` - date of the article
- `_long_` - type of content: `long`, `short`, or `page`
- `building-a-static-site-generator` - slug/path for the URL
- `_draft` (optional) - feed tag for categorization

The first `#` header is the title of the article - no frontmatter needed.

**Types of content**:
- `long` - only title with link to articles will be displayed in feed
- `short` - title and all content will be displayed
- `page` - won't be displayed in feed at all

### Feeds

Posts can be tagged with an optional feed category (e.g., `_python`, `_webdev`). Posts with feed tags:
- Appear on the main page (unless excluded in config)
- Have their own feed page at `/feed/{tag}/`

**Configuration in `config.py`:**
```python
# Exclude specific feeds from main page (they'll still have /feed/name/ pages)
EXCLUDE_FEEDS_FROM_MAIN = ['draft', 'private']
```

This is useful for draft posts or topic-specific content you want separated from the main feed.

---

## Installation

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# or: venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your blog in `config.py`:
```python
BLOG_TITLE = "My Blog"
BLOG_DESCRIPTION = "A simple blog built with picopaper"
THEME = "default"
```

4. Generate the site:
```bash
venv/bin/python picopaper.py
```

5. Serve locally for testing:
```bash
cd output
python3 -m http.server 8000
```

Visit http://localhost:8000

### Docker

Build and run with Docker:

```bash
# Build the image
docker build -t picopaper .

# Run the container
docker run --rm -v $(pwd):/app picopaper
```

For Podman (recommended for rootless):

```bash
# Build the image
podman build -t picopaper .

# Run with user namespace mapping
podman run --rm --userns=keep-id -v $(pwd):/app picopaper
```

The generated site will be available in the `output/` directory.

---

## Directory Structure

- `items/` - Markdown content files
- `theme/` - Theme directory containing templates and assets
  - `default/` - Default theme
    - `templates/` - Jinja2 templates
    - `assets/` - CSS and static assets
- `images/` - Image files (copied to output)
- `static/` - Static files copied as-is (GPG keys, .well-known, etc.)
- `output/` - Generated site (do not edit)
- `config.py` - Blog configuration

## Themes

Themes are organized in the `theme/` directory. Each theme has its own subdirectory containing:
- `templates/` - Jinja2 template files
- `assets/` - CSS, JavaScript, and other static assets

To switch themes, change the `THEME` setting in `config.py`

---

## Notes

- [Github Mirror](https://github.com/CaffeineFueled1/picopaper)

---

## Security

For security concerns or reports, please contact via `hello a t uphillsecurity d o t com` [gpg](https://uphillsecurity.com/gpg).

---

## License

**Apache License**

Version 2.0, January 2004

http://www.apache.org/licenses/

- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Patent use
- ✅ Private use
- ✅ Limitations
- ❌Trademark use
- ❌Liability
- ❌Warranty
