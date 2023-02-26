from argparse import ArgumentParser
from pathlib import Path
from urllib.parse import urlparse

import logging as lg
import re
import requests as rq


def get_html(url):
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


def main():
    parser = ArgumentParser()
    parser.add_argument('urls', nargs='+')
    parser.add_argument('-v', '--version', action='version', version='v1.0.0')
    args = parser.parse_args()

    for url in args.urls:
        if not re.match(r'https?:\/\/www\..+', url):
            lg.error(f"can't process url format {url}")
            continue

        html = get_html(url)

        if html:
            url = urlparse(url)
            filename = url.netloc
            Path(filename + '.html').write_text(html)
        else:
            lg.error(f"can't process url {url}")


if __name__ == '__main__':
    main()
