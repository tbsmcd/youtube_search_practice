import os
import configparser
import requests
import click


def confirm_key() -> str:
    """API Key を持っているか確認

    scripts/api.ini に API Key を持っていたらそのまま返す。
    持っていなかったら入力してもらう。

    :return: API Key を文字列として返す

    """
    ini_file = os.path.dirname(__file__) + '/api.ini'
    config = configparser.ConfigParser()
    config.read(ini_file)
    config.sections()
    try:
        api_key = config['Default']['key']
    except KeyError:
        print('API Key dose not exist. Please get your API Key.')
        print('https://console.cloud.google.com/apis/credentials?project=upheld-rookery-339704&supportedpurview=project')
        api_key = input('Please type key:')
        config['Default'] = {'key': api_key}
        with open(ini_file, 'w') as configfile:
            config.write(configfile)
    return api_key


@click.command()
@click.option('-k', '--keyword', type=str, prompt=True,
              help='スペースが含まれる場合はダブルクォーテーションで囲って下さい')
def main(keyword: str):
    api_key = confirm_key()
    print(keyword)



if __name__ == '__main__':
    main()
