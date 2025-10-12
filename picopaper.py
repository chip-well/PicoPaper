#!/usr/bin/env python3

import os
import re
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import markdown
from config import BLOG_TITLE, BLOG_DESCRIPTION, THEME, EXCLUDE_FEEDS_FROM_MAIN, NAVBAR_ITEMS

class SSGGGenerator:
    def __init__(self, items_dir='items', output_dir='output', theme=None, blog_title=None, blog_description=None):
        self.items_dir = Path(items_dir)
        self.output_dir = Path(output_dir)
        self.theme = theme or THEME
        self.theme_dir = Path('theme') / self.theme
        self.templates_dir = self.theme_dir / 'templates'
        self.assets_dir = self.theme_dir / 'assets'
        self.blog_title = blog_title or BLOG_TITLE
        self.blog_description = blog_description or BLOG_DESCRIPTION
        self.exclude_feeds = EXCLUDE_FEEDS_FROM_MAIN
        self.navbar_items = NAVBAR_ITEMS

        # Setup Jinja2
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))

        # Setup markdown
        self.md = markdown.Markdown(extensions=['extra'])

    def parse_filename(self, filename):
        """Parse filename format: YYYY-MM-DD_type_name[_feed].md"""
        pattern = r'(\d{4}-\d{2}-\d{2})_(short|long|page)_(.+?)(?:_([a-z0-9-]+))?\.md'
        match = re.match(pattern, filename)

        if not match:
            return None

        date_str, post_type, name, feed = match.groups()
        date = datetime.strptime(date_str, '%Y-%m-%d')

        return {
            'date': date,
            'date_str': date.strftime('%Y-%m-%d'),
            'type': post_type,
            'name': name,
            'feed': feed,
            'filename': filename
        }

    def read_post(self, filepath):
        """Read markdown file and extract title and content"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract title (first # heading)
        title_match = re.match(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else 'Untitled'

        # Remove title from content
        if title_match:
            content = content[title_match.end():].strip()

        # Convert markdown to HTML
        html_content = self.md.convert(content)

        return title, html_content

    def collect_posts(self):
        """Collect and parse all posts from items directory"""
        posts = []

        if not self.items_dir.exists():
            print(f"Warning: {self.items_dir} does not exist")
            return posts

        for filepath in self.items_dir.glob('*.md'):
            parsed = self.parse_filename(filepath.name)

            if not parsed:
                print(f"Skipping {filepath.name}: doesn't match naming convention")
                continue

            title, content = self.read_post(filepath)

            post = {
                'date': parsed['date_str'],
                'type': parsed['type'],
                'name': parsed['name'],
                'title': title,
                'content': content,
                'slug': parsed['name'],
                'url': f"{parsed['name']}/",
                'feed': parsed['feed'],
                'source': filepath.name
            }

            posts.append(post)

        # Sort by date, newest first
        posts.sort(key=lambda x: x['date'], reverse=True)

        return posts

    def generate_index(self, posts, feed_name=None):
        """Generate index.html with all posts (or feed-specific index)"""
        template = self.env.get_template('index.tmpl')

        if feed_name:
            title = f"{feed_name} - {self.blog_title}"
            output_path = self.output_dir / 'feed' / feed_name / 'index.html'
        else:
            title = self.blog_title
            output_path = self.output_dir / 'index.html'

        html = template.render(
            title=title,
            blog_title=self.blog_title,
            blog_description=self.blog_description,
            navbar_items=self.navbar_items,
            posts=posts
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ Generated {output_path}")

    def generate_post_page(self, post):
        """Generate individual post page for 'long' posts"""
        template = self.env.get_template('post.tmpl')

        html = template.render(
            title=f"{post['title']} - {self.blog_title}",
            blog_title=self.blog_title,
            blog_description=self.blog_description,
            navbar_items=self.navbar_items,
            post=post
        )

        # Create directory for the post slug
        post_dir = self.output_dir / post['slug']
        post_dir.mkdir(exist_ok=True)

        # Generate index.html inside the slug directory
        output_path = post_dir / 'index.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ Generated {output_path}")

    def copy_assets(self):
        """Copy theme assets and images to output directory"""
        import shutil

        # Copy theme assets
        if self.assets_dir.exists():
            dest_dir = self.output_dir / 'assets'
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(self.assets_dir, dest_dir)
            print(f"✓ Copied theme assets to output")

        # Copy images
        images_dir = Path('images')
        if images_dir.exists():
            dest_dir = self.output_dir / 'images'
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(images_dir, dest_dir)
            print(f"✓ Copied images/ to output")

        # Copy static files (GPG keys, .well-known, etc.)
        static_dir = Path('static')
        if static_dir.exists():
            for item in static_dir.rglob('*'):
                if item.is_file():
                    # Preserve directory structure
                    rel_path = item.relative_to(static_dir)
                    dest_path = self.output_dir / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest_path)
            print(f"✓ Copied static/ to output")

    def generate(self):
        """Main generation process"""
        print(f"Starting picopaper generation with theme '{self.theme}'...")

        # Create output directory
        self.output_dir.mkdir(exist_ok=True)

        # Collect posts
        all_posts = self.collect_posts()
        print(f"Found {len(all_posts)} posts")

        # Filter out pages and excluded feeds from main feed
        feed_posts = [p for p in all_posts
                      if p['type'] != 'page'
                      and p['feed'] not in self.exclude_feeds]

        # Generate main index with filtered feed posts
        self.generate_index(feed_posts)

        # Group posts by feed (include all posts, not just those in main feed)
        feeds = {}
        for post in all_posts:
            if post['feed'] and post['type'] != 'page':
                feeds.setdefault(post['feed'], []).append(post)

        # Generate feed-specific pages
        for feed_name, posts in feeds.items():
            self.generate_index(posts, feed_name)

        # Generate individual pages for long posts, short posts, and pages
        for post in all_posts:
            if post['type'] in ['long', 'short', 'page']:
                self.generate_post_page(post)

        # Copy assets
        self.copy_assets()

        print(f"\n✓ Site generated successfully in {self.output_dir}/")

def main():
    generator = SSGGGenerator()
    generator.generate()

if __name__ == '__main__':
    main()
