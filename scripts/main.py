import os
import sys
import configparser
import requests
import click

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
        mess = 'API Key が存在しません。サブコマンド `main.py key [API KEY]` で保存できます。'\
            + '次の URL から取得して入力して下さい。'\
            + 'https://console.cloud.google.com/apis/credentials?project=upheld-rookery-339704&supportedpurview=project'
        click.echo(mess, err=True)
        sys.exit()
    return api_key


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


@main.command(help='API Key を保存するサブコマンド。引数に API Key を指定して下さい。')
@click.argument('key', type=str, required=True)
def key(key: str):
    try:
        config = configparser.ConfigParser()
        config['Default'] = {'key': key}
        with open(ini_file, 'w') as configfile:
            config.write(configfile)
            click.echo(key)
    except Exception:
        # TODO: 例外の幅を広く取りすぎているから検討
        click.echo('failed', err=True)


@main.command(help='検索する場合のサブコマンド。引数にスペースが含まれる場合はダブルクォーテーションで囲って下さい')
@click.argument('keyword', type=str, required=True)
@click.option('--num', type=click.IntRange(1, 50), required=False, default=10,
              help='表示件数を入力して下さい。')
def search(keyword: str, num: int):
    api_key = confirm_key()
    endpoint = 'https://www.googleapis.com/youtube/v3/search'
    # 空白は + に置換して検索する
    params = {
        'key': api_key,
        'part': 'snippet',
        'type': 'video',
        'order': 'viewCount',
        'maxResults': num,
        'q': '+'.join(keyword.split()),
    }
    r = requests.get(endpoint, params=params)
    if r.status_code == 200:
        video_base_url = 'https://www.youtube.com/watch?v='
        for item in r.json()['items']:
            click.echo(video_base_url + item['id']['videoId'] + ' ' + item['snippet']['title'])

    elif r.status_code == 400:
        click.echo('API Key が不正なようです。サブコマンド key を使って下さい。', err=True)
    else:
        click.echo('原因不明のエラー http status code: {0}'.format(r.status_code), err=True)


if __name__ == '__main__':
    main()
