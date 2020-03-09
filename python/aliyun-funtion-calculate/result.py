def get_node(tar_key, data):
    """

    :param tar_key: 稿定设计导出_354919/第二/1.jpg
    :param data: 稿定设计导出_354919/ or 稿定设计导出_354919/第二/
    :return:
    """
    for key in data.keys():
        if key.startswith(tar_key.rsplit("/", 1)[0]):
            return data[key]
    for value in data.values():
        if isinstance(value, dict):
            return get_node(tar_key, value)


if __name__ == '__main__':
    root_node = {'稿定设计导出_354919/': {
        '稿定设计导出_354919/': {},
        '1': {'file_path': 'τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/Θé╡Σ╝ƒ.jpg', 'file_name': '邵伟.jpg'},
        '2': {'file_path': 'τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/8.jpg',
              'file_name': '8.jpg'}
    }
    }
    data = get_node('稿定设计导出_354919/10.jpg', root_node)
    print(data)
{'稿定设计导出_354919/': {
    '1': {'file_name': '邵伟.jpg', 'key': 'intelligentArt/unzip/1/11175/8ff7109785fa45efa2a6621589f2e96a.jpeg',
          'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287},
    '2': {'file_name': '8.jpg', 'key': 'intelligentArt/unzip/1/11175/4028f6c30e844d208931f538daf38353.jpeg',
          'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287},
    '3': {'file_name': '9.jpg', 'key': 'intelligentArt/unzip/1/11175/a25299e86dec4edfbce0da687b5eea10.jpeg',
          'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287},
    '4': {'file_name': '10.jpg', 'key': 'intelligentArt/unzip/1/11175/69f3ec9efdc34ec6aa8a4140447bf878.jpeg',
          'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287}, '稿定设计导出_354919/第二/': {
        '5': {'file_name': '你好.jpg', 'key': 'intelligentArt/unzip/1/11175/1cc022755ccd43ecbf359db39fb98649.jpeg',
              'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287},
        '6': {'file_name': '8.jpg', 'key': 'intelligentArt/unzip/1/11175/99330fd529464feb9186e7344bb9e0d1.jpeg',
              'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287},
        '7': {'file_name': '9.jpg', 'key': 'intelligentArt/unzip/1/11175/19b8b25f9804482ea4080f99dd65377d.jpeg',
              'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287},
        '8': {'file_name': '12.jpg', 'key': 'intelligentArt/unzip/1/11175/979e0224910841b393b3bd343dad7e07.jpeg',
              'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287},
        '9': {'file_name': '13.jpg', 'key': 'intelligentArt/unzip/1/11175/dd2f560ae25b4388ba1ddf0e17660ae3.jpeg',
              'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287},
        '10': {'file_name': '11.jpg', 'key': 'intelligentArt/unzip/1/11175/633bef0818084d8ba138a6df71cb85c8.jpeg',
               'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287}},
    '11': {'file_name': '4.jpg', 'key': 'intelligentArt/unzip/1/11175/1f56ab772d51447ba28486a6f2d9a30f.jpeg',
           'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287},
    '12': {'file_name': '5.jpg', 'key': 'intelligentArt/unzip/1/11175/3c65f3aabd0d4149958ba46111fbb2ea.jpeg',
           'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287},
    '13': {'file_name': '7.jpg', 'key': 'intelligentArt/unzip/1/11175/020e8244e966425c8f63ccf4d033c34d.jpeg',
           'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287},
    '14': {'file_name': '6.jpg', 'key': 'intelligentArt/unzip/1/11175/7ad85409bcae46749fad102071294515.jpeg',
           'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287},
    '15': {'file_name': '2.jpg', 'key': 'intelligentArt/unzip/1/11175/c786440fbefd4fa88714d781354d30bb.jpeg',
           'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287},
    '16': {'file_name': '1.jpg', 'key': 'intelligentArt/unzip/1/11175/8649b2918ea74e22b12c4886b6d3b0ec.jpeg',
           'width': 790, 'height': 951, 'format': 'JPEG', 'file_size': 560287}}}

{'events': [{'eventName': 'ObjectCreated:PostObject', 'eventSource': 'acs:oss', 'eventTime': '2019-12-02T08:14:03.000Z',
             'eventVersion': '1.0', 'oss': {
        'bucket': {'arn': 'acs:oss:cn-beijing:1376573201505901:ecpro-uploads', 'name': 'ecpro-uploads',
                   'ownerIdentity': '1376573201505901', 'virtualBucket': ''},
        'object': {'deltaSize': 0, 'eTag': 'EBF0126A0DC44D8B0FF6BE4C703978B2',
                   'key': 'tmp/1/e1c56c82-93d4-42d1-979b-f9405a0a5a19.zip', 'size': 5213787}, 'ossSchemaVersion': '1.0',
        'ruleId': 'ecdce3120320d668045893fc85bc467860d4d3ad', 'xVars': {'x:account_id': '1'}}, 'region': 'cn-beijing',
             'requestParameters': {'sourceIPAddress': '106.38.124.243'},
             'responseElements': {'requestId': '5DE4C7C883B4CE3731470C21'},
             'userIdentity': {'principalId': '286847774614784161'}}]}
{'shaowei':
    {
        '稿定设计导出_354919':
            {
                '第二':
                    {
                        11: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/τ¼¼Σ║î/8.jpg', 'file_name': '8.jpg',
                             'key': 'intelligentArt/unzip/1/1/e98c7293e6364da58debbdab48222dd4.jpeg', 'width': 790,
                             'height': 350,
                             'format': 'JPEG', 'file_size': 111217},
                        12: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/τ¼¼Σ║î/Σ╜áσÑ╜.jpg',
                             'file_name': '你好.jpg',
                             'key': 'intelligentArt/unzip/1/1/aeff58a4ca094742baf102891f69d3cb.jpeg', 'width': 790,
                             'height': 350,
                             'format': 'JPEG', 'file_size': 111217},
                        13: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/τ¼¼Σ║î/11.jpg', 'file_name': '11.jpg',
                             'key': 'intelligentArt/unzip/1/1/d34eef8fb0b94fee90e32c838a2406a8.jpeg', 'width': 790,
                             'height': 350,
                             'format': 'JPEG', 'file_size': 111217},
                        14: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/τ¼¼Σ║î/9.jpg', 'file_name': '9.jpg',
                             'key': 'intelligentArt/unzip/1/1/cd969a02eec842be9c73fbd1f31a6324.jpeg', 'width': 790,
                             'height': 350,
                             'format': 'JPEG', 'file_size': 111217},
                        15: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/τ¼¼Σ║î/13.jpg', 'file_name': '13.jpg',
                             'key': 'intelligentArt/unzip/1/1/bb55fa5326034511a626889f3176b121.jpeg', 'width': 790,
                             'height': 350,
                             'format': 'JPEG', 'file_size': 111217},
                        16: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/τ¼¼Σ║î/12.jpg', 'file_name': '12.jpg',
                             'key': 'intelligentArt/unzip/1/1/c9ccb0ed12d44601bd893da56b2c1926.jpeg', 'width': 790,
                             'height': 350,
                             'format': 'JPEG', 'file_size': 111217}},
                1: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/2.jpg', 'file_name': '2.jpg',
                    'key': 'intelligentArt/unzip/1/1/4c9f165a909e4dd9a548afa3a0bd58fd.jpeg',
                    'width': 790, 'height': 350, 'format': 'JPEG', 'file_size': 111217},
                2: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/6.jpg', 'file_name': '6.jpg',
                    'key': 'intelligentArt/unzip/1/1/7fa7e4d2070b4d6087038dd519101df4.jpeg',
                    'width': 790, 'height': 350, 'format': 'JPEG', 'file_size': 111217},
                3: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/8.jpg', 'file_name': '8.jpg',
                    'key': 'intelligentArt/unzip/1/1/244bff03027246fa8ba47bafcf662332.jpeg',
                    'width': 790, 'height': 350, 'format': 'JPEG', 'file_size': 111217},
                4: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/5.jpg', 'file_name': '5.jpg',
                    'key': 'intelligentArt/unzip/1/1/5fa3d88f6a084b5e868fc9ff532b2696.jpeg',
                    'width': 790, 'height': 350, 'format': 'JPEG', 'file_size': 111217},
                5: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/Θé╡Σ╝ƒ.jpg',
                    'file_name': '邵伟.jpg',
                    'key': 'intelligentArt/unzip/1/1/273c4fffa5344832b1bc2d9af400b77d.jpeg',
                    'width': 790, 'height': 350, 'format': 'JPEG', 'file_size': 111217},
                6: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/4.jpg', 'file_name': '4.jpg',
                    'key': 'intelligentArt/unzip/1/1/2fda4f07990c4864bd2416491f26a5e6.jpeg',
                    'width': 790, 'height': 350, 'format': 'JPEG', 'file_size': 111217},
                7: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/7.jpg', 'file_name': '7.jpg',
                    'key': 'intelligentArt/unzip/1/1/6a968863e2254ee4a6eefe338ef3f825.jpeg',
                    'width': 790, 'height': 350, 'format': 'JPEG', 'file_size': 111217},
                8: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/10.jpg', 'file_name': '10.jpg',
                    'key': 'intelligentArt/unzip/1/1/afbc48fac71c4f9abc5d70c68e99d870.jpeg',
                    'width': 790, 'height': 350, 'format': 'JPEG', 'file_size': 111217},
                9: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/9.jpg', 'file_name': '9.jpg',
                    'key': 'intelligentArt/unzip/1/1/3930c6e704a4467691ba5bec900fcd39.jpeg',
                    'width': 790, 'height': 350, 'format': 'JPEG', 'file_size': 111217},
                10: {'file_path': '/tmp/shaowei/τ¿┐σ«ÜΦ«╛Φ«íσ»╝σç║_354919/1.jpg', 'file_name': '1.jpg',
                     'key': 'intelligentArt/unzip/1/1/7a36363c46d448248bc5e40fb30e28cf.jpeg',
                     'width': 790, 'height': 350, 'format': 'JPEG', 'file_size': 111217}}}}
