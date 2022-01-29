import os
import sys
import configparser
import requests
import click

import pprint

ini_file = os.path.dirname(__file__) + '/api.ini'


def confirm_key() -> str:
    """API Key を持っているか確認

    scripts/api.ini に API Key を持っていたらそのまま返す。
    持っていなかったら入力してもらう。

    :return: API Key を文字列として返す

    """
    config = configparser.ConfigParser()
    config.read(ini_file)
    config.sections()
    try:
        api_key = config['Default']['key']
    except KeyError:
        print('API Key が存在しません。サブコマンド `main.py key [API KEY]` で保存できます。')
        print('下記リンクから取得して入力して下さい。')
        print('https://console.cloud.google.com/apis/credentials?project=upheld-rookery-339704&supportedpurview=project')
        sys.exit()
    return api_key


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


@main.command(help='API Key を保存するサブコマンド。引数に API Key を入力して下さい。')
@click.argument('key', type=str, required=True)
def key(key: str) -> str:
    config = configparser.ConfigParser()
    config['Default'] = {'key': key}
    with open(ini_file, 'w') as configfile:
        config.write(configfile)


@main.command(help='検索する場合のサブコマンド。引数にスペースが含まれる場合はダブルクォーテーションで囲って下さい')
@click.argument('keyword', type=str, required=True)
def search(keyword: str):
    api_key = confirm_key()
    print(keyword)
    endpoint = 'https://www.googleapis.com/youtube/v3/search'
    # 空白は + に置換して検索する
    params = {
        'key': api_key,
        'part': 'snippet',
        'type': 'video',
        'order': 'viewCount',
        'q': '+'.join(keyword.split()),
    }
    print(params)
    r = requests.get(endpoint, params=params)
    if r.status_code == 400:
        # API Key が不正
        print('API Key が不正なようです。')
        # 再帰的に処理しても良いが単純なコマンドなので終了する
        sys.exit()


if __name__ == '__main__':
    main()
