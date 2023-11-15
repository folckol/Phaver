
import ssl


import cloudscraper

from bs4 import BeautifulSoup

import random

from fake_useragent import UserAgent


def Ava():
    def _make_scraper():
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers(
            "ECDH-RSA-NULL-SHA:ECDH-RSA-RC4-SHA:ECDH-RSA-DES-CBC3-SHA:ECDH-RSA-AES128-SHA:ECDH-RSA-AES256-SHA:"
            "ECDH-ECDSA-NULL-SHA:ECDH-ECDSA-RC4-SHA:ECDH-ECDSA-DES-CBC3-SHA:ECDH-ECDSA-AES128-SHA:"
            "ECDH-ECDSA-AES256-SHA:ECDHE-RSA-NULL-SHA:ECDHE-RSA-RC4-SHA:ECDHE-RSA-DES-CBC3-SHA:ECDHE-RSA-AES128-SHA:"
            "ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-NULL-SHA:ECDHE-ECDSA-RC4-SHA:ECDHE-ECDSA-DES-CBC3-SHA:"
            "ECDHE-ECDSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA:AECDH-NULL-SHA:AECDH-RC4-SHA:AECDH-DES-CBC3-SHA:"
            "AECDH-AES128-SHA:AECDH-AES256-SHA"
        )
        ssl_context.set_ecdh_curve("prime256v1")
        ssl_context.options |= (ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3 | ssl.OP_NO_TLSv1_3 | ssl.OP_NO_TLSv1)
        ssl_context.check_hostname = False

        # print('sad')

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )

    session = _make_scraper()

    session.proxies = {'http': '',
                       'https': ''}
    session.user_agent = UserAgent().chrome


    collections = [ ['0xbd3531da5cf5857e7cfaa92426877b022e612cf8', 8888],
                    ['0xed5af388653567af2f388e6224dc7c4b3241c544', 10000],
                    ['0xacf63e56fd08970b43401492a02f6f38b6635c91', 7535],
                    ['0x394e3d3044fc89fcdd966d3cb35ac0b32b0cda91', 8495],
                    ['0x80336ad7a747236ef41f47ed2c7641828a480baa', 5556],
                    ['0x77372a4cc66063575b05b44481f059be356964a4', 9246],
                    ['0x364c828ee171616a39897688a831c2499ad972ec', 10000],
                    ['0x09cad840984ecb9f10b337a923665e66d5e54495', 2222],
                    ['0xaad35c2dadbe77f97301617d82e661776c891fa9', 15000],
                    ['0xc99c679c50033bbc5321eb88752e89a93e9e83c5', 3333],
                    ['0x83b070e842adba2397113c4bca70c00d7df00729', 9998],
                    ['0x4db1f25d3d98600140dfc18deb7515be5bd293af', 8192],
                    ['0xbcd1a163dee3ac31342eb6626f28e45d637dd091', 6000],
                    ['0x231d3559aa848bf10366fb9868590f01d34bf240', 9000],
                    ['0x09233d553058c2f42ba751c87816a8e9fae7ef10', 8888],
                    ['0xdfde78d2baec499fe18f2be74b6c287eed9511d7', 500],
                    ['0x209e639a0ec166ac7a1a4ba41968fa967db30221', 9998],
                    ['0x0eed0a2b4df338fc1bca6115e4100592632d14cd', 3497],
                    ['0x6325439389e0797ab35752b4f43a14c004f22a9c', 12727],
                    ['0x19b86299c21505cdf59ce63740b240a9c822b5e4', 8888],
                    ['0xaaf03a65cbd8f01b512cd8d530a675b3963de255', 47892],
                    ['0xfa969c60a78195c631787d4585ba15a07578c979', 9998],
                    ['0x68bd8b7c45633de6d7afd0b1f7b86b37b8a3c02a', 7777],
                    ['0x3903d4ffaaa700b62578a66e7a67ba4cb67787f9', 5000],
                    ['0x845a007d9f283614f403a24e3eb3455f720559ca', 24445],
                    ['0xe785e82358879f061bc3dcac6f0444462d4b5330', 10000],
                    ['0x2976084061bb4c97aa41a69ede695a824511d972', 3333],
                    ['0x1cb1a5e65610aeff2551a50f76a87a7d3fb649c6', 7015],
                    ['0xdf0f0a5508aa4f506e5bdc8c45c8879e6e80d3e4', 855],
                    ['0x0c2e57efddba8c768147d1fdf9176a0a6ebd5d83', 9999],
                    ['0x2acab3dea77832c09420663b0e1cb386031ba17b', 9999],
                    ['0x6fc355d4e0ee44b292e50878f49798ff755a5bbc', 10000],
                    ['0x40cf6a63c35b6886421988871f6b74cc86309940', 5000],
                    ['0xbd3531da5cf5857e7cfaa92426877b022e612cf8', 8888],
                    ['0x1a92f7381b9f03921564a437210bb9396471050c', 9960],
                    ['0x0b0b186841c55d8a09d53db48dc8cab9dbf4dbd6', 5000],
                    ['0x8cae61967466ebbf15c12dc802b29594bc04efc6', 8888],
                    ['0x354634c4621cdfb7a25e6486cca1e019777d841b', 7204],
                    ['0xba30e5f9bb24caa003e9f2f0497ad287fdf95623', 9627],
                    ['0xcde8f5008c313820b558addfcd8628e20cc1c2fe', 10000],
                    ['0xfe8c6d19365453d26af321d0e8c910428c23873f', 11111],
                    ['0xa4d5fb4ff0fa1565fb7d8f5db88e4c0f2f445046', 10000],
                    ['0x7ea3cca10668b8346aec0bf1844a49e995527c8b', 14879],
                    ['0x306b1ea3ecdf94ab739f1910bbda052ed4a9f949', 19950],
                    ['0xd774557b647330c91bf44cfeab205095f7e6c367', 19929],
                    ['0xfc8bb028ddcd01961d24085166378001092fca72', 510],
                    ['0x8d609bd201beaea7dccbfbd9c22851e23da68691', 9999],
                    ['0x09f66a094a0070ebddefa192a33fa5d75b59d46b', 2998],
                    ['0x2de0f6e3b931a56d34434835582abc779e2f944d', 4998],
                    ['0xd3d9ddd0cf0a5f0bfb8f7fceae075df687eaebab', 9169],
                    ['0x0fcbd68251819928c8f6d182fc04be733fa94170', 6969],
                    ['0x5d949a57a4dfc1fa0dc63e992fa28175f4b9c094', 3333],
                    ['0xca7ca7bcc765f77339be2d648ba53ce9c8a262bd', 20000],
                    ['0xf880b2a16f257d0b9b8ab64351a07a4137527c82', 8888],
                    ['0xe5c93b6692c03d4279d1a3098e4321254b560f47', 4421],
                    ['0xf793a77e32a0e5c0cd28383e1e04bbc66ee52438', 8888],
                    ['0xc0f799a176e10d45fa56c7298d54f813b51fd151', 8887],
                    ['0xe2e27b49e405f6c25796167b2500c195f972ebac', 9999],
                    ['0x5f076e995290f3f9aea85fdd06d8fae118f2b75c', 6628],
                    ['0x20d93d65ada7ee46235f95f5995ae5c5dc5ac44c', 1627],
                    ['0x2c0d708c6e82dc6c427ce6a96ba5ff2ea09be272', 6997],
                    ['0x10cdcb5a80e888ec9e9154439e86b911f684da7b', 10648],
                    ['0xc9d198089d6c31d0ca5cc5b92c97a57a97bbfde2', 8888],
                    ['0xd2df37a48162eeb6520e0be975d7693fd72d5316', 3333],
                    ['0x2868dd9abf1a88d5be7025858a55180d59bb1689', 6963],
                    ['0x24aa93b7abe09b5e55c5b29758282d05799ecea5', 7777],
                    ['0xe41bea6888f771a0c16d7188284522b76c135252', 7934],
                    ['0xb6c9a4e8ae1ccf33c2dc3d8c4ab322e4529233e2', 2816],
                    ['0xc6210509389fdac176d68a35d021c095ba657b82', 9990],
                    ['0xbfe47d6d4090940d1c7a0066b63d23875e3e2ac5', 5555],
                    ['0xa65ba71d653f62c64d97099b58d25a955eb374a0', 2222],
                    ['0x2de0f6e3b931a56d34434835582abc779e2f944d', 4998],
                    ['0x29652c2e9d3656434bc8133c69258c8d05290f41', 4444],
                    ['0xf1268733c6fb05ef6be9cf23d24436dcd6e0b35e', 10000],
                    ['0x9401518f4ebba857baa879d9f76e1cc8b31ed197', 5556],
                    ['0x1dc454ee1fd63f3d792aeee9d331c05d9c62b20a', 888],
                    ['0x12b180b635dd9f07a78736fb4e43438fcdb41555', 5553],
                    ['0xd774557b647330c91bf44cfeab205095f7e6c367', 19929],
                    ['0xfc8bb028ddcd01961d24085166378001092fca72', 510],
                    ['0x8d609bd201beaea7dccbfbd9c22851e23da68691', 9999],
                    ['0x09f66a094a0070ebddefa192a33fa5d75b59d46b', 2998],
                    ['0x2de0f6e3b931a56d34434835582abc779e2f944d', 4998],
                    ['0xd3d9ddd0cf0a5f0bfb8f7fceae075df687eaebab', 9169],
                    ['0x0fcbd68251819928c8f6d182fc04be733fa94170', 6969],
                    ['0x5d949a57a4dfc1fa0dc63e992fa28175f4b9c094', 3333],
                    ['0xca7ca7bcc765f77339be2d648ba53ce9c8a262bd', 20000],
                    ['0xf880b2a16f257d0b9b8ab64351a07a4137527c82', 8888],
                    ['0xe5c93b6692c03d4279d1a3098e4321254b560f47', 4421],
                    ['0xf793a77e32a0e5c0cd28383e1e04bbc66ee52438', 8888],
                    ['0xc0f799a176e10d45fa56c7298d54f813b51fd151', 8887],
                    ['0xe2e27b49e405f6c25796167b2500c195f972ebac', 9999],
                    ['0x5f076e995290f3f9aea85fdd06d8fae118f2b75c', 6628],
                    ['0x20d93d65ada7ee46235f95f5995ae5c5dc5ac44c', 1627],
                    ['0x2c0d708c6e82dc6c427ce6a96ba5ff2ea09be272', 6997],
                    ['0x10cdcb5a80e888ec9e9154439e86b911f684da7b', 10648],
                    ['0xc9d198089d6c31d0ca5cc5b92c97a57a97bbfde2', 8888],
                    ['0xd2df37a48162eeb6520e0be975d7693fd72d5316', 3333],
                    ['0x2868dd9abf1a88d5be7025858a55180d59bb1689', 6963],
                    ['0x24aa93b7abe09b5e55c5b29758282d05799ecea5', 7777],
                    ['0xe41bea6888f771a0c16d7188284522b76c135252', 7934],
                    ['0xb6c9a4e8ae1ccf33c2dc3d8c4ab322e4529233e2', 2816],
                    ['0xc6210509389fdac176d68a35d021c095ba657b82', 9990],
                    ['0xbfe47d6d4090940d1c7a0066b63d23875e3e2ac5', 5555],
                    ['0xa65ba71d653f62c64d97099b58d25a955eb374a0', 2222],
                    ['0x2de0f6e3b931a56d34434835582abc779e2f944d', 4998],
                    ['0x29652c2e9d3656434bc8133c69258c8d05290f41', 4444],
                    ['0xf1268733c6fb05ef6be9cf23d24436dcd6e0b35e', 10000],
                    ['0x9401518f4ebba857baa879d9f76e1cc8b31ed197', 5556],
                    ['0x1dc454ee1fd63f3d792aeee9d331c05d9c62b20a', 888],
                    ['0x12b180b635dd9f07a78736fb4e43438fcdb41555', 5553],
                    ['0x5af0d9827e0c53e4799bb226655a1de152a425a5', 9825],
                    ['0x495f947276749ce646f68ac8c248420045cb7b5e', 10000],
                    ['0x8821bee2ba0df28761afff119d66390d594cd280', 8705],
                    ['0xd0318da435dbce0b347cc6faa330b5a9889e3585', 9197],
                    ['0xb4a7d131436ed8ec06ad696fa3bf8d23c0ab3acf', 6943],
                    ['0xb668beb1fa440f6cf2da0399f8c28cab993bdd65', 2085],
                    ['0x2c889a24af0d0ec6337db8feb589fa6368491146', 271],
                    ['0x3fd36d72f05fb1af76ee7ce9257ca850faba91ed', 7000],
                    ['0xafe12842e3703a3cc3a71d9463389b1bf2c5bc1c', 6881],
                    ['0x9e8ea82e76262e957d4cc24e04857a34b0d8f062', 14224],
                    ['0xa6cd272874ee7c872eb66801eff62784c0b13285', 7572],
                    ['0x94638cbf3c54c1f956a5f05cbc0f9afb6822020d', 10778],
                    ['0xedeaeeafb386e293952fc5f77c3424bc18753cdf', 6666],
                    ['0xeb2dfc54ebafca8f50efcc1e21a9d100b5aeb349', 8214],
                    ['0x6dc6001535e15b9def7b0f6a20a2111dfa9454e2', 7839],
                    ['0xa4057dada9217a8e64ee7d469a5a7e7c40b7380f', 10000],
                    ['0xabeca79f4eb1d6cc7a98a8bf3c7fb769ea0e4c77', 5555],
                    ['0xc379e535caff250a01caa6c3724ed1359fe5c29b', 10725],
                    ['0xa3aee8bce55beea1951ef834b99f3ac60d1abeeb', 10247],
                    ['0x86cc280d0bac0bd4ea38ba7d31e895aa20cceb4b', 12292],
                    ['0xefed2a58cc6a5b81f9158b231847f005cf086c01', 1000],
                    ['0x12787526c03d626aac88e6edc4d0fb930d86c631', 2000],
                    ['0x6184facb1850c8f7160cc2f7be8d2bc5192d3b70', 5555],
                    ['0x46fdfcb3cd89a1c54d36ee83a4adc184747b40d9', 9713],
                    ['0xe6d48bf4ee912235398b96e16db6f310c21e82cb', 5022],
                    ['0x4ea8972d6dca586baf22dfbe727f31c3274765ae', 3580],
                    ['0x7bd29408f11d2bfc23c34f18275bbf23bb716bc7', 19947],
                    ['0xe012baf811cf9c05c408e879c399960d1f305903', 5386],
                    ['0x8fa600364b93c53e0c71c7a33d2ade21f4351da3', 4999],
                    ['0x3e55d389d352f4905961a6b32ca53b2f229fed73', 5555],
                    ['0x23581767a106ae21c074b2276d25e5c3e136a68b', 10000],
                    ['0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb', 9997],
                    ['0x39cd103414106b922eb09c7d45df89608b59e887', 6969],
                    ['0x1d20a51f088492a0f1c57f047a9e30c9ab5c07ea', 12284],
                    ['0xad9fd7cb4fc7a0fbce08d64068f60cbde22ed34c', 8886],
                    ['0x11450058d796b02eb53e65374be59cff65d3fe7f', 9992],
                    ['0x1792a96e5668ad7c167ab804a100ce42395ce54d', 9994],
                    ['0xd70f41dd5875eee7fa9dd8048567bc932124a8d2', 3074],
                    ['0x59325733eb952a92e069c87f0a6168b29e80627f', 8888],
                    ['0x03c993a0af31c953d98b22e2f1825a6ac191fcc1', 10000],
                                    ]

    p = random.choice(collections)
    with session.get(f'https://opensea.io/assets/ethereum/{p[0]}/{random.randint(1,p[1])}', timeout=15) as response:
        soup = BeautifulSoup(response.text, 'html.parser')

        link = str(soup).split('"imageStorageUrl":"')[-1].split('","tokenId"')[0]

        response = session.get(link)
        open(f"Images/image.{link.split('.')[-1]}", "wb").write(response.content)


    return f"image.{link.split('.')[-1]}"

