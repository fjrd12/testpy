from url_shortener.adapters import url_mapping

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url_obj = url_mapping()
    #url_obj.init_db()
    #url_obj.add('http://127.0.0.1/asjdnao231', 'very_long_url_1')
    Urltranslated = url_obj.get('http://127.0.0.1/asjdnao231')
    print(Urltranslated.url_short, Urltranslated.url_long)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
