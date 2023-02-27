# HTML Fetcher

A simple HTML fetcher

## Installation

Install all dependencies required by this script

```shell
$ pip3 install -r requirements.txt
```

You can also use docker if you want. Build the image

```shell
$ docker build . -t fetch
```

## Usage

To download tailwindcss home page, you can do it like this

```shell
$ python3 fetch.py https://www.tailwindcss.com --assets
```

or if you build the image

```shell
$ docker run --rm -it -v $PWD/:/app fetch https://www.tailwindcss.com --assets
```

See help for more detail

```shell
$ python3 fetch.py --help
```

For simplicity, the only accepted URL format is `https://www.sitename.com/path?query=value`.
