import logging
import pytest
import requests
from colorama import Fore, Back, Style

url_main = 'http://127.0.0.1:8000/'
path_delete = 'delete'
path_add = 'add'
path_get = 'get'
test_path_short = 'http://127.0.0.1:8000/test_case'
test_path_long = 'http://www.facebook.com'


def test_connect_and_delete_previous():
    params = {'url_short': test_path_short}
    r = requests.delete(url_main + path_delete, params=params)
    print('\n'+Back.GREEN+'-Delete test {} successful!'.format(test_path_short)+Back.RESET)


def test_crear_url_transaltion():
    payload = {
        'url_short': test_path_short,
        'url_long': test_path_long
    }
    url_to_add = url_main + path_add
    try:
        response = requests.post(url_to_add, json=payload)
    except requests.exceptions.ConnectionError as e:
        print(Fore.RED + "\n-Connection error" + Fore.RESET)
        assert False

    if response.status_code == 500:
        print('\n' + Fore.RED + response.text)
        print(Fore.RESET)
        assert False
    print('\n' + Back.GREEN + '-Creation test {} successful!'.format(payload) + Back.RESET)


def test_consultar_url_transaltion():
    url_to_add = url_main + path_get
    try:
        response = requests.get(url_to_add, params=test_path_short)
    except requests.exceptions.ConnectionError as e:
        print(Fore.RED + "\n-Connection error" + Fore.RESET)
        assert False

    if response.status_code == 500:
        print('\n' + Fore.RED + response.text)
        print(Fore.RESET)
        assert False
    print('\n'+Back.GREEN + '-Get test {} successfully!'.format(test_path_short) + Back.RESET)


def test_consultar_translate():
    url_to_translate = test_path_short
    try:
        response = requests.get(url_to_translate)
    except requests.exceptions.ConnectionError as e:
        print(Fore.RED + "\n-Connection error" + Fore.RESET)
        assert False

    if response.status_code == 500:
        print('\n' + Fore.RED + response.text)
        print(Fore.RESET)
        assert False
    print('\n'+Back.GREEN + '-Translate test {} to {} successfully!'.format(test_path_short, test_path_long) + Back.RESET)
