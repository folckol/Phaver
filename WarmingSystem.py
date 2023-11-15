import random
import sqlite3
import threading

from utils.logger import logger
from PhaverModel import *


class WarmingModel(PhaverAccount):

    def __init__(self, gqlID, username, refresh_token, proxy):

        self.gqlID = gqlID
        # print(gqlID)
        self.username = username
        self.refreshToken = refresh_token
        self.session = self._make_scraper
        self.session.proxies = {
            "http": f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}",
            "https": f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"}
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        self.session.headers.update({"x-client-version": self.generate_special_XClientVersion,
                                     "x-ios-bundle-identifier": "com.phaver.mobile",
                                     "x-firebase-gmpid": self.generate_firebase_gmpid,
                                     "user-agent": self.generate_user_agent,
                                     'content-type': 'application/json'})

    def UpdateDB(self, param):

        if param == 'Post':
            acc = session.query(Account).filter_by(username=self.username).first()
            acc.postsCount += 1
        elif param == 'Follow':
            acc = session.query(Account).filter_by(username=self.username).first()
            acc.followings += 1
        elif param == 'Like':
            acc = session.query(Account).filter_by(username=self.username).first()
            acc.likesCount += 1
        elif param == 'Retweet':
            acc = session.query(Account).filter_by(username=self.username).first()
            acc.retweetsCount += 1

        session.commit()

    def Authorization(self):

        payload = {
            "grantType": "refresh_token",
            "refreshToken": self.refreshToken
        }

        with self.session.post(
                'https://securetoken.googleapis.com/v1/token?key=',
                json=payload) as response:
            self.token = response.json()["id_token"]
            self.session.headers.update({'authorization': f'Bearer {response.json()["id_token"]}'})

    def Warming(self):

        posts = self.GetPosts()['data']['sortedPosts']

        actionsCount = random.randint(3, 7)
        for i in range(actionsCount):
            post = random.choice(posts)

            self.Like(post['id'])
            self.AddLog('Like')

            if random.randint(0, 100) > 85:
                self.Retweet(post['id'])
                self.AddLog('Retweet')

            posts.remove(post)
            time.sleep(random.randint(100, 350) / 100)

        actionsCount = random.randint(2, 10)
        for i in range(actionsCount):
            post = random.choice(posts)
            self.Follow(post['post']['profile']['id'])
            self.AddLog('Follow')

            posts.remove(post)
            time.sleep(random.randint(100, 350) / 100)

        conn_ = sqlite3.connect(
            r'',
            check_same_thread=False)
        cursor_ = conn_.cursor()

        cursor_.execute("""SELECT * FROM posts""")
        posts = cursor_.fetchall()

        random_text = random.choice(posts)

        self.CreatePost(text=random_text[1], imageId=self.UploadPhoto(random_text[-1]))
        self.AddLog('NewPost')

        conn_.close()

        self.UpdateFollowers()

    def UpdateFollowers(self):

        data = self.GetAccountInfo(self.gqlID)
        followers = data['data']['profile']['hasFollowed']['aggregate']['count']
        acc = session.query(Account).filter_by(username=self.username).first()
        acc.followers = followers
        session.commit()

    def AddLog(self, text):

        with open(f'Logs/UserLogs/{self.username}.txt', 'a+') as file:
            file.write(f'{datetime.datetime.utcnow()} | ' + text + '\n')

    @property
    def generate_special_XClientVersion(self) -> str:
        platform = "iOS"
        sdk_version = "FirebaseSDK/10.7.0"
        library = "FirebaseCore-iOS"

        version = ".".join(str(random.randint(0, 9)) for _ in range(3))
        return f"{platform}/{sdk_version}/{version}/{library}"

    @property
    def generate_firebase_gmpid(self) -> str:
        random_hex = "".join(random.choice("0123456789abcdef") for _ in range(24))
        return f"1:451272859150:ios:{random_hex}"

    @property
    def generate_user_agent(self) -> str:
        return f"FirebaseAuth.iOS/10.7.0 com.phaver.mobile/6.8.2 iPhone/16.{random.randint(1, 6)}.{random.randint(1, 3)} hw/iPhone{random.choice(['11', '12', '13', '14'])}_3"

    @property
    def _make_scraper(self):
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

        return cloudscraper.create_scraper(
            debug=False,
            ssl_context=ssl_context
        )


def Start(list, delay):
    while len(list) != 0:

        try:
            randomAcc = random.choice(list)

            model = WarmingModel(randomAcc.gqlID, randomAcc.username, randomAcc.refresh_token, randomAcc.proxy)
            model.Authorization()
            model.Warming()
            logger.success(model.username + ' - Прогрев успешно завершен')

        except Exception as e:

            logger.error(model.username + f' - Ошибка ({str(e)})')

        list.remove(randomAcc)
        time.sleep(delay)


def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return list(lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


if __name__ == '__main__':

    while True:
        day_time = 86400 / 2
        account_time = 30

        accounts = session.query(Account2).all()
        threading_count = int(len(accounts) // (day_time / 30) + 1)
        lists = split_list(accounts, threading_count)

        print(lists)

        logger.info(f'\nАккаунтов в базе: {len(accounts)}\n'
                    f'Потоков: {threading_count}\n'
                    f'Задержка: {day_time / len(lists[0]) - account_time}')

        threads = []
        for list in lists:
            delay = day_time / len(list) - account_time
            thread = threading.Thread(target=Start, args=(list, delay))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()



