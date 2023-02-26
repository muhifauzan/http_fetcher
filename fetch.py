from argparse import ArgumentParser
from bs4 import BeautifulSoup as XMLParser
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import logging as lg
import re
import requests as rq


def get_html_text(url):
    try:
        response = rq.get(url)

        if response.status_code not in range(200, 299):
            raise RuntimeError()

        return response.text

    except rq.RequestException:
        lg.error('request error occurred')

    except rq.HTTPError:
        lg.error('connection error occurred')

    except rq.TooManyRedirects:
        lg.error('too many redirects')

    except rq.Timeout:
        lg.error('connection timeout')

    except RuntimeError:
        lg.error('request failed')


def print_metadata(sitename, html):
    links_count = len(html.find_all('a'))
    images_count = len(html.find_all('img'))
    time = datetime.utcnow().strftime('%a %b %d %Y %H:%M UTC')

    print(f'site: {sitename}')
    print(f'num_links: {links_count}')
    print(f'images: {images_count}')
    print(f'last_fetch: {time}')


def archive_asset(assets_dir, sitename, html, tag, prop, ext):
    for tag in html.find_all(tag):
        tag_prop = tag.get(prop)

        if tag_prop and tag_prop.startswith('/') and tag_prop.endswith(ext):
            response = rq.get('https://' + sitename + tag_prop)

            if response.status_code == 200:
                asset_file = Path(tag_prop).name
                asset_path = assets_dir.joinpath(asset_file)

                if ext in ['.png', '.jpg']:
                    with asset_path.open('wb') as af:
                        for chunk in response:
                            af.write(chunk)
                else:
                    asset_path.write_text(response.text)

                tag[prop] = str(asset_path)


def archive_assets(sitename, html):
    assets_dir = Path(sitename.replace('.', '_') + '_assets')

    if not assets_dir.exists():
        assets_dir.mkdir()

    archive_asset(assets_dir, sitename, html, 'link', 'href', '.css')
    archive_asset(assets_dir, sitename, html, 'script', 'src', '.js')
    archive_asset(assets_dir, sitename, html, 'img', 'src', '.png')
    archive_asset(assets_dir, sitename, html, 'img', 'src', '.jpg')

    return html


def main():
    parser = ArgumentParser()
    parser.add_argument('urls', nargs='+')
    parser.add_argument('-a', '--assets', action='store_true',
                        dest='is_with_assets',
                        help='archive the assets')
    parser.add_argument('-m', '--metadata', action='store_true',
                        dest='is_with_metadata',
                        help='print metadata')
    parser.add_argument('-v', '--version', action='version', version='v1.0.0')
    args = parser.parse_args()

    for url in args.urls:
        if not re.match(r'https://www\..+', url):
            lg.error(f"can't process url format {url}")
            continue

        html_text = get_html_text(url)
        sitename = urlparse(url).netloc

        if html_text:
            html = XMLParser(html_text, 'html.parser')

            if args.is_with_metadata:
                print_metadata(sitename, html)

            if args.is_with_assets:
                html = archive_assets(sitename, html)

            Path(sitename + '.html').write_text(str(html))
        else:
            lg.error(f"can't process url {url}")


if __name__ == '__main__':
    main()
