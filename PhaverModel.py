import base64
import datetime
import pickle
import random
import re
import shutil
import ssl
import string
import time
import traceback
from uuid import uuid4

import capmonster_python
import cloudscraper
import requests
from GenerateImage import Ava
import warnings
from utils.logger import logger
from DB import *


warnings.filterwarnings("ignore", category=DeprecationWarning)



class PhaverAccount:

    def __init__(self, email, proxy, capKey=None):

        self.token = None
        self.refresh_token = None
        self.gqlID = None

        self.sitekey = '6LdAUmQfAAAAAK7cFboDQx2teLP3Tu2QxKk9jwB4'
        self.email, self.password, self.capKey = email, self.generate_password, capKey
        self.session = self._make_scraper
        self.session.proxies = {"http": f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}",
                                "https": f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"}
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        self.session.headers.update({"x-client-version": self.generate_special_XClientVersion,
                                     "x-ios-bundle-identifier": "com.phaver.mobile",
                                     "x-firebase-gmpid": self.generate_firebase_gmpid,
                                     "user-agent": self.generate_user_agent,
                                     'content-type': 'application/json'})

    def Registration(self):

        payload = {"email": self.email,
                   "password": self.password,
                   "returnSecureToken": True}

        with self.session.post(
                'https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=AIzaSyABU16fMP_LH45JHdtXM_N-wDtxuSgBkmE',
                json=payload) as response:

            self.token = response.json()['idToken']
            self.refresh_token = response.json()['refreshToken']
            self.gqlID = response.json()['localId']

            return response.json()


    def SyncTokenMutation(self):

        payload = {
          "operationName": "SyncTokenMutation",
          "variables": {
            "token": self.token,
            "inviteCode": None,
            "captchaResponse": self.SolveCaptcha},
          "query": "mutation SyncTokenMutation($token: String!, $inviteCode: String, $captchaResponse: String) { syncToken( token: $token inviteCode: $inviteCode captchaResponse: $captchaResponse ) { forceRefresh isProfileSetupDone requireCaptcha __typename } }"
        }

        with self.session.post('https://gql.next.phaver.com/v1/graphql/', json=payload) as response:
            pass

    def RefreshToken(self):
        payload = {
            "grantType": "refresh_token",
            "refreshToken": self.refresh_token
        }

        with self.session.post('https://securetoken.googleapis.com/v1/token?key=AIzaSyABU16fMP_LH45JHdtXM_N-wDtxuSgBkmE', json=payload) as response:
            self.token = response.json()['id_token']
            print(self.token)
            self.session.headers.update({'authorization': f'Bearer {self.token}'})

    def UploadPhotoOnServer(self):

        filename = ''
        while '.png' not in filename:
            try:
                filename = Ava()
            except:
                pass

        with open('Images/image.png', 'rb') as f:
            data = f.read()

        boundary = "--{0}".format(uuid4().hex).encode('utf-8')
        body = [
            boundary,
            b'Content-Disposition: form-data; name="model"',
            b'',
            b'profile',
            boundary,
            b'Content-Disposition: form-data; name="file"; filename="image.png"',
            b'Content-Type: application/octet-stream',
            b'',
            data,
            boundary + b'--'
        ]
        body_data = b'\r\n'.join(body)


        self.session.headers.update({'content-type': 'multipart/form-data; boundary={0}'.format(
            boundary.decode('utf8')[2:]
        )})

        with self.session.post('https://api.next.phaver.com/api/upload', data=body_data, timeout=60) as response:

            return response.json()

    def UploadPhoto(self, name):

        if name == None:
            return None

        with open(f'Images/{name}', 'rb') as f:
            data = f.read()

        boundary = "--{0}".format(uuid4().hex).encode('utf-8')
        body = [
            boundary,
            b'Content-Disposition: form-data; name="model"',
            b'',
            b'profile',
            boundary,
            b'Content-Disposition: form-data; name="file"; filename="image.png"',
            b'Content-Type: application/octet-stream',
            b'',
            data,
            boundary + b'--'
        ]
        body_data = b'\r\n'.join(body)


        self.session.headers.update({'content-type': 'multipart/form-data; boundary={0}'.format(
            boundary.decode('utf8')[2:]
        )})

        with self.session.post('https://api.next.phaver.com/api/upload', data=body_data, timeout=60) as response:

            return response.json()

    def UpdateProfileMutation(self, media_id, nickname):

        names = []
        with open('InputData/genereg_names.txt', 'r') as file:
            for i in file:
                names.append(i.rstrip())

        self.name = random.choice(names)
        payload = {
          "operationName": "UpdateProfileMutation",
          "variables": {
            "id": self.gqlID,
            "values": {
              "imageId": media_id,
              "name": self.name,
              "username": nickname
            }
          },
          "query": "mutation UpdateProfileMutation($id: String!, $values: profiles_set_input!) { update_profiles_by_pk(pk_columns: {id: $id}, _set: $values) { ...ProfileFieldsFragment __typename } } fragment ProfileFieldsFragment on profiles { ...ProfileBasicFieldsFragment ...ProfileSocialMediaFieldsFragment __typename } fragment ProfileBasicFieldsFragment on profiles { id name username description credLevel image { ...ImageFieldsFragment __typename }coverImage { ...ImageFieldsFragment __typename } createdAt updatedAt lensProfile { ...LensProfileFieldsFragment __typename } phaverFrens timeoutUntil verified nft { ...NFTFieldsFragment __typename } ccProfiles { id handle __typename } __typename } fragment ImageFieldsFragment on images { id profileId size bucket createdAt updatedAt filename width height blurhash contentType pages source_url __typename } fragment LensProfileFieldsFragment on lens_profiles { id lensProfileId lensHandle status txId ownerAddress followModule image { ...ImageFieldsFragment __typename } __typename } fragment NFTFieldsFragment on connected_nfts { id profileId nftName nft_description nftTokenId contractAddress createdAt updatedAt image { ...ImageFieldsFragment __typename } __typename } fragment ProfileSocialMediaFieldsFragment on profiles { instagram facebook youtube twitter pinterest snapchat linkedin tiktok website telegram discord __typename } "
        }

        with self.session.post('https://gql.next.phaver.com/v1/graphql/',json=payload) as response:
            return response.json()

    def UpsertFlagMutation(self):

        payload = {
          "operationName": "UpsertFlagMutation",
          "variables": {
            "accountId": self.gqlID,
            "flagType": "profileSetupDone",
            "enabled": True
          },
          "query": "mutation UpsertFlagMutation($accountId: String!, $enabled: Boolean!, $flagType: flag_types_enum!) { flag: insert_flags_one( object: {accountId: $accountId, flagType: $flagType, enabled: $enabled} on_conflict: {constraint: flags_pkey, update_columns: enabled} ) { ...FlagFieldsFragment __typename } } fragment FlagFieldsFragment on flags { flagType enabled accountId createdAt updatedAt __typename }"
        }

        with self.session.post('https://gql.next.phaver.com/v1/graphql/',json=payload) as response:
            return response.json()

    def CheckUsername(self, username):
        payload = {
          "operationName": "ProfileIdByUsernameQuery",
          "variables": {
            "username": username
          },
          "query": "query ProfileIdByUsernameQuery($username: String!) { profileByUsername(username: $username) { id __typename } }"
        }

        with self.session.post('https://gql.next.phaver.com/v1/graphql/', json=payload) as response:
            return response.json()

    def GetAccountInfo(self, gqlID):
        payload = {
            "operationName": "CurrentUserDetailsQuery",
            "variables": {
                "accountId": gqlID
            },
            "query": "query CurrentUserDetailsQuery($accountId: String!) { profile: profiles_by_pk(id: $accountId) { ...CurrentUserProfileFieldsFragment __typename } } fragment CurrentUserProfileFieldsFragment on profiles { ...ProfileFieldsFragment ...ProfileGeoFieldsFragment branchLink account { ...AccountFieldsFragment userFlags: flags { enabled flagType __typename } notificationSettings { enabled eventType __typename } __typename } memberships: communityMembers { ...TopicSubscribersFragment __typename } lensProfile { ...CurrentUserLensProfileFragment __typename } hasFollowed: followedBy_aggregate(limit: 1) { aggregate { count __typename } __typename } phaverFrens timeoutUntil credLevel __typename } fragment ProfileFieldsFragment on profiles { ...ProfileBasicFieldsFragment ...ProfileSocialMediaFieldsFragment __typename } fragment ProfileBasicFieldsFragment on profiles { id name username description credLevel image { ...ImageFieldsFragment __typename } coverImage { ...ImageFieldsFragment __typename } createdAt updatedAt lensProfile { ...LensProfileFieldsFragment __typename } phaverFrens timeoutUntil verified nft { ...NFTFieldsFragment __typename } ccProfiles { id handle __typename } __typename } fragment ImageFieldsFragment on images { id profileId size bucket createdAt updatedAt filename width height blurhash contentType pages source_url __typename } fragment LensProfileFieldsFragment on lens_profiles { id lensProfileId lensHandle status txId ownerAddress followModule image { ...ImageFieldsFragment __typename } __typename } fragment NFTFieldsFragment on connected_nfts { id profileId nftName nft_description nftTokenId contractAddress createdAt updatedAt image { ...ImageFieldsFragment __typename } __typename } fragment ProfileSocialMediaFieldsFragment on profiles { instagram facebook youtube twitter pinterest snapchat linkedin tiktok website telegram discord __typename } fragment ProfileGeoFieldsFragment on profiles { city { ...CityFieldsFragment __typename } __typename } fragment CityFieldsFragment on cities { id nameEn subdivision { id nameEn country { id nameEn isoCode continent { nameEn id __typename } __typename } __typename } __typename } fragment AccountFieldsFragment on accounts { id type email unverifiedEmail lang notificationsReadAt createdAt updatedAt deletedAt __typename } fragment TopicFieldsFragment on communities { ...TopicBasicFieldsFragment description imageId language profileId isMember createdAt updatedAt deletedAt publishedAt image { ...ImageFieldsFragment __typename } __typename } fragment TopicBasicFieldsFragment on communities { id name pointCost __typename } fragment TopicSubscribersFragment on community_members { profileId communityId userRole lastVisited createdAt community { ...TopicFieldsFragment __typename } __typename } fragment CurrentUserLensProfileFragment on lens_profiles { dispatcherAddress ...LensProfileFieldsFragment custodial_account_address lensApiRefreshTokens { tokenExpirationTime: token_expiration_time __typename } __typename }"
        }

        with self.session.post('https://gql.next.phaver.com/v1/graphql/', json=payload) as response:
            return response.json()

    def GetPosts(self):

        payload = {
          "operationName": "SortedPostsQuery",
          "variables": {
            "limit": 25,
            "offset": 0,
            "topicIds": [],
            "initialQueryTimestamp": self.reformat_timestamp(),
            "mode": "recommended",
            "filters": [
              "none"  #"followedOnly" посты только с каналов на которые подписан
            ],
            "timeRange": "ALL_TIME"
          },
          "query": "query SortedPostsQuery($limit: Int!, $offset: Int!, $initialQueryTimestamp: timestamptz!, $mode: SortedPostsMode!, $topicIds: [String!]!, $filters: [SortedPostsFilter!], $timeRange: TimeRangeOption!) { sortedPosts( offset: $offset limit: $limit initialQueryTimestamp: $initialQueryTimestamp mode: $mode topicIds: $topicIds filters: $filters timeRange: $timeRange ) { id sorting post { ...PostFieldsFragment __typename } __typename } } fragment PostFieldsFragment on recommendations { lensPost { ...LensPostsFieldsFragment __typename } ...PostBasicFieldsFragment mirroredPost: postPointed { ...PostBasicFieldsFragment lensPost { ...LensPostsFieldsFragment __typename } __typename } __typename } fragment PostBasicFieldsFragment on recommendations { id description affiliateLink affiliateDisplayLink communityContentId createdAt deletedAt discountCode imageId itemId profileId publishedAt userHasStaked userVoteScore communityContent { id type topic: community { ...TopicBasicFieldsFragment __typename } __typename } profile { ...ProfileBasicFieldsFragment __typename } image { ...ImageFieldsFragment __typename } links { ...LinkFieldsFragment __typename } medias { ...MediaFragment __typename } ...PostAggregateFieldsFragment __typename } fragment ImageFieldsFragment on images { id profileId size bucket createdAt updatedAt filename width height blurhash contentType pages source_url __typename } fragment ProfileBasicFieldsFragment on profiles { id name username description credLevel image { ...ImageFieldsFragment __typename } coverImage { ...ImageFieldsFragment __typename } createdAt updatedAt lensProfile { ...LensProfileFieldsFragment __typename } phaverFrens timeoutUntil verified nft { ...NFTFieldsFragment __typename } ccProfiles { id handle __typename } __typename } fragment LensProfileFieldsFragment on lens_profiles { id lensProfileId lensHandle status txId ownerAddress followModule image { ...ImageFieldsFragment __typename } __typename } fragment NFTFieldsFragment on connected_nfts { id profileId nftName nft_description nftTokenId contractAddress createdAt updatedAt image { ...ImageFieldsFragment __typename } __typename } fragment LinkFieldsFragment on links { id postId: recommendationId description imageId title url createdAt updatedAt image { ...ImageFieldsFragment __typename } __typename } fragment TopicBasicFieldsFragment on communities { id name pointCost __typename } fragment MediaFragment on medias { id videoId audioId imageId video { ...VideoFragment __typename } __typename } fragment VideoFragment on videos { createdAt dash duration errorReasonCode errorReasonText height hls id mimeType preview readyToStream size sourceUrl state thumbnail uid updatedAt width __typename } fragment PostAggregateFieldsFragment on recommendations { postAggregates { id collects mirrors dailyStakes votes comments __typename } __typename } fragment PostVoteFieldsFragment on recommendation_votes { profileId postId: recommendationId value __typename } fragment CommentFieldsFragment on recommendation_comments { id profileId postId: recommendationId content createdAt publishedAt parentId userVoteScore commentAggregates { votes __typename } lensComment { id status __typename } profile { ...ProfileFieldsFragment __typename } deletedAt __typename } fragment ProfileFieldsFragment on profiles { ...ProfileBasicFieldsFragment ...ProfileSocialMediaFieldsFragment __typename } fragment ProfileSocialMediaFieldsFragment on profiles { instagram facebook youtube twitter pinterest snapchat linkedin tiktok website telegram discord __typename } fragment CommentVoteFieldsFragment on comment_votes { profileId commentId value __typename } fragment LensPostsFieldsFragment on lens_posts { id postId lensPubId lensProfileId collectModule status collectModuleReturnData isCollected lensDaId __typename } "
        }

        with self.session.post('https://gql.next.phaver.com/v1/graphql/',json=payload) as response:
            return response.json()

    def Like(self, postId):

        payload = {
              "operationName": "VotePostMutation",
              "variables": {
                "id": postId,
                "vote": "upvote"
              },
              "query": "mutation VotePostMutation($id: String!, $vote: Vote!) { votePost(postId: $id, vote: $vote) { vote postId post { ...PostFieldsFragment __typename } __typename } } fragment PostFieldsFragment on recommendations { lensPost { ...LensPostsFieldsFragment __typename } ...PostBasicFieldsFragment mirroredPost: postPointed { ...PostBasicFieldsFragment lensPost { ...LensPostsFieldsFragment __typename } __typename } __typename } fragment PostBasicFieldsFragment on recommendations { id description affiliateLink affiliateDisplayLink communityContentId createdAt deletedAt discountCode imageId itemId profileId publishedAt userHasStaked userVoteScore communityContent { id type topic: community { ...TopicBasicFieldsFragment __typename } __typename } profile { ...ProfileBasicFieldsFragment __typename } image { ...ImageFieldsFragment __typename } links { ...LinkFieldsFragment __typename } medias { ...MediaFragment __typename } ...PostAggregateFieldsFragment __typename } fragment ImageFieldsFragment on images { id profileId size bucket createdAt updatedAt filename width height blurhash contentType pages source_url __typename } fragment ProfileBasicFieldsFragment on profiles { id name username description credLevel image { ...ImageFieldsFragment __typename } coverImage { ...ImageFieldsFragment __typename } createdAt updatedAt lensProfile { ...LensProfileFieldsFragment __typename } phaverFrens timeoutUntil verified nft { ...NFTFieldsFragment __typename } ccProfiles { id handle __typename } __typename } fragment LensProfileFieldsFragment on lens_profiles { id lensProfileId lensHandle status txId ownerAddress followModule image { ...ImageFieldsFragment __typename } __typename } fragment NFTFieldsFragment on connected_nfts { id profileId nftName nft_description nftTokenId contractAddress createdAt updatedAt image { ...ImageFieldsFragment __typename } __typename } fragment LinkFieldsFragment on links { id postId: recommendationId description imageId title url createdAt updatedAt image { ...ImageFieldsFragment __typename } __typename } fragment TopicBasicFieldsFragment on communities { id name pointCost __typename } fragment MediaFragment on medias { id videoId audioId imageId video { ...VideoFragment __typename } __typename } fragment VideoFragment on videos { createdAt dash duration errorReasonCode errorReasonText height hls id mimeType preview readyToStream size sourceUrl state thumbnail uid updatedAt width __typename } fragment PostAggregateFieldsFragment on recommendations { postAggregates { id collects mirrors dailyStakes votes comments __typename } __typename } fragment PostVoteFieldsFragment on recommendation_votes { profileId postId: recommendationId value __typename } fragment CommentFieldsFragment on recommendation_comments { id profileId postId: recommendationId content createdAt publishedAt parentId userVoteScore commentAggregates { votes __typename } lensComment { id status __typename } profile { ...ProfileFieldsFragment __typename } deletedAt __typename } fragment ProfileFieldsFragment on profiles { ...ProfileBasicFieldsFragment ...ProfileSocialMediaFieldsFragment __typename } fragment ProfileSocialMediaFieldsFragment on profiles { instagram facebook youtube twitter pinterest snapchat linkedin tiktok website telegram discord __typename } fragment CommentVoteFieldsFragment on comment_votes { profileId commentId value __typename } fragment LensPostsFieldsFragment on lens_posts { id postId lensPubId lensProfileId collectModule status collectModuleReturnData isCollected lensDaId __typename }"
            }

        with self.session.post('https://gql.next.phaver.com/v1/graphql/',json=payload) as response:
            return response.json()

    def Follow(self, userId):

        payload = {
          "operationName": "FollowUserMutation",
          "variables": {
            "followedProfileId": userId,
            "followType": "phaver"
          },
          "query": "mutation FollowUserMutation($followedProfileId: String!, $followType: FollowType) { setFollow(profileId: $followedProfileId, follow: true, followType: $followType) { status profileId profile { ...ProfileDetailedFieldsFragment __typename } lensQuota { ...LensQuotaFollowsFieldsFragment __typename } __typename } } fragment ProfileDetailedFieldsFragment on profiles { isUserFollowing ...ProfileFieldsFragment __typename } fragment ProfileFieldsFragment on profiles { ...ProfileBasicFieldsFragment ...ProfileSocialMediaFieldsFragment __typename } fragment ProfileBasicFieldsFragment on profiles { id name username description credLevel image { ...ImageFieldsFragment __typename } coverImage { ...ImageFieldsFragment __typename } createdAt updatedAt lensProfile { ...LensProfileFieldsFragment __typename } phaverFrens timeoutUntil verified nft { ...NFTFieldsFragment __typename } ccProfiles { id handle __typename } __typename } fragment ImageFieldsFragment on images { id profileId size bucket createdAt updatedAt filename width height blurhash contentType pages source_url __typename } fragment LensProfileFieldsFragment on lens_profiles { id lensProfileId lensHandle status txId ownerAddress followModule image { ...ImageFieldsFragment __typename } __typename } fragment NFTFieldsFragment on connected_nfts { id profileId nftName nft_description nftTokenId contractAddress createdAt updatedAt image { ...ImageFieldsFragment __typename } __typename } fragment ProfileSocialMediaFieldsFragment on profiles { instagram facebook youtube twitter pinterest snapchat linkedin tiktok website telegram discord __typename } fragment LensQuotaFollowsFieldsFragment on LensQuotaFollows { available maximum monthlyAvailable monthlyMaximum __typename }"
        }

        with self.session.post('https://gql.next.phaver.com/v1/graphql/',json=payload) as response:
            return response.json()


    def Retweet(self, postId):

        payload = {
              "operationName": "MirrorPostMutation",
              "variables": {
                "postId": postId,
                "topicName": None,
                "broadcastToLens": False
              },
              "query": "mutation MirrorPostMutation($postId: String!, $topicName: String, $broadcastToLens: Boolean!) { mirrorPost( postId: $postId topicName: $topicName broadcastToLens: $broadcastToLens ) { postId post { ...PostFieldsFragment __typename } __typename } } fragment PostFieldsFragment on recommendations { lensPost { ...LensPostsFieldsFragment __typename } ...PostBasicFieldsFragment mirroredPost: postPointed { ...PostBasicFieldsFragment lensPost { ...LensPostsFieldsFragment __typename } __typename } __typename } fragment PostBasicFieldsFragment on recommendations { id description affiliateLink affiliateDisplayLink communityContentId createdAt deletedAt discountCode imageId itemId profileId publishedAt userHasStaked userVoteScore communityContent { id type topic: community { ...TopicBasicFieldsFragment __typename } __typename } profile { ...ProfileBasicFieldsFragment __typename } image { ...ImageFieldsFragment __typename } links { ...LinkFieldsFragment __typename } medias { ...MediaFragment __typename } ...PostAggregateFieldsFragment __typename } fragment ImageFieldsFragment on images { id profileId size bucket createdAt updatedAt filename width height blurhash contentType pages source_url __typename } fragment ProfileBasicFieldsFragment on profiles { id name username description credLevel image { ...ImageFieldsFragment __typename } coverImage { ...ImageFieldsFragment __typename } createdAt updatedAt lensProfile { ...LensProfileFieldsFragment __typename } phaverFrens timeoutUntil verified nft { ...NFTFieldsFragment __typename } ccProfiles { id handle __typename } __typename } fragment LensProfileFieldsFragment on lens_profiles { id lensProfileId lensHandle status txId ownerAddress followModule image { ...ImageFieldsFragment __typename } __typename } fragment NFTFieldsFragment on connected_nfts { id profileId nftName nft_description nftTokenId contractAddress createdAt updatedAt image { ...ImageFieldsFragment __typename } __typename } fragment LinkFieldsFragment on links { id postId: recommendationId description imageId title url createdAt updatedAt image { ...ImageFieldsFragment __typename } __typename } fragment TopicBasicFieldsFragment on communities { id name pointCost __typename } fragment MediaFragment on medias { id videoId audioId imageId video { ...VideoFragment __typename } __typename } fragment VideoFragment on videos { createdAt dash duration errorReasonCode errorReasonText height hls id mimeType preview readyToStream size sourceUrl state thumbnail uid updatedAt width __typename } fragment PostAggregateFieldsFragment on recommendations { postAggregates { id collects mirrors dailyStakes votes comments __typename } __typename } fragment PostVoteFieldsFragment on recommendation_votes { profileId postId: recommendationId value __typename } fragment CommentFieldsFragment on recommendation_comments { id profileId postId: recommendationId content createdAt publishedAt parentId userVoteScore commentAggregates { votes __typename } lensComment { id status __typename } profile { ...ProfileFieldsFragment __typename } deletedAt __typename } fragment ProfileFieldsFragment on profiles { ...ProfileBasicFieldsFragment ...ProfileSocialMediaFieldsFragment __typename } fragment ProfileSocialMediaFieldsFragment on profiles { instagram facebook youtube twitter pinterest snapchat linkedin tiktok website telegram discord __typename } fragment CommentVoteFieldsFragment on comment_votes { profileId commentId value __typename } fragment LensPostsFieldsFragment on lens_posts { id postId lensPubId lensProfileId collectModule status collectModuleReturnData isCollected lensDaId __typename } "
            }

        with self.session.post('https://gql.next.phaver.com/v1/graphql/',json=payload) as response:
            return response.json()

    def CreatePost(self,text, topicName=None, imageId=None):

        payload = {
          "operationName": "CreatePostMutation",
          "variables": {
            "post": {
              "description": text,
              "topicName": topicName,
              "imageId": imageId
            },
            "link": None,
            "broadcastToLens": False
          },
          "query": "mutation CreatePostMutation($post: PostInput!, $link: LinkInput, $broadcastToLens: Boolean!, $videoId: String) { createPost( post: $post link: $link broadcastToLens: $broadcastToLens videoId: $videoId ) { status postId post { ...PostFieldsFragment __typename } __typename } } fragment PostFieldsFragment on recommendations { lensPost { ...LensPostsFieldsFragment __typename } ...PostBasicFieldsFragment mirroredPost: postPointed { ...PostBasicFieldsFragment lensPost { ...LensPostsFieldsFragment __typename } __typename } __typename } fragment PostBasicFieldsFragment on recommendations { id description affiliateLink affiliateDisplayLink communityContentId createdAt deletedAt discountCode imageId profileId publishedAt userHasStaked userVoteScore communityContent { id type topic: community { ...TopicBasicFieldsFragment __typename } __typename } profile { ...ProfileBasicFieldsFragment __typename } image { ...ImageFieldsFragment __typename } links { ...LinkFieldsFragment __typename } medias { ...MediaFragment __typename } ...PostAggregateFieldsFragment __typename } fragment ImageFieldsFragment on images { id profileId size bucket createdAt updatedAt filename width height blurhash contentType pages source_url __typename } fragment ProfileBasicFieldsFragment on profiles { id name username description credLevel image { ...ImageFieldsFragment __typename } coverImage { ...ImageFieldsFragment __typename } createdAt updatedAt lensProfile { ...LensProfileFieldsFragment __typename } phaverFrens timeoutUntil verified nft { ...NFTFieldsFragment __typename } ccProfiles { id handle __typename } __typename } fragment LensProfileFieldsFragment on lens_profiles { id lensProfileId lensHandle status txId ownerAddress followModule image { ...ImageFieldsFragment __typename } __typename } fragment NFTFieldsFragment on connected_nfts { id profileId nftName nft_description nftTokenId contractAddress createdAt updatedAt image { ...ImageFieldsFragment __typename } __typename } fragment LinkFieldsFragment on links { id postId: recommendationId description imageId title url createdAt updatedAt image { ...ImageFieldsFragment __typename } __typename } fragment TopicBasicFieldsFragment on communities { id name pointCost __typename } fragment MediaFragment on medias { id videoId audioId imageId video { ...VideoFragment __typename } __typename } fragment VideoFragment on videos { createdAt dash duration errorReasonCode errorReasonText height hls id mimeType preview readyToStream size sourceUrl state thumbnail uid updatedAt width __typename } fragment PostAggregateFieldsFragment on recommendations { postAggregates { id collects mirrors dailyStakes votes comments __typename } __typename } fragment PostVoteFieldsFragment on recommendation_votes { profileId postId: recommendationId value __typename } fragment CommentFieldsFragment on recommendation_comments { id profileId postId: recommendationId content createdAt publishedAt parentId userVoteScore commentAggregates { votes __typename } lensComment { id status __typename } profile { ...ProfileFieldsFragment __typename } deletedAt __typename } fragment ProfileFieldsFragment on profiles { ...ProfileBasicFieldsFragment ...ProfileSocialMediaFieldsFragment __typename } fragment ProfileSocialMediaFieldsFragment on profiles { instagram facebook youtube twitter pinterest snapchat linkedin tiktok website telegram discord __typename } fragment CommentVoteFieldsFragment on comment_votes { profileId commentId value __typename } fragment LensPostsFieldsFragment on lens_posts { id postId lensPubId lensProfileId collectModule status collectModuleReturnData isCollected lensDaId __typename }"
        }

        with self.session.post('https://gql.next.phaver.com/v1/graphql/',json=payload) as response:
            return response.json()


    def reformat_timestamp(self, timestamp=time.time()) -> str:
            # Преобразуем строку timestamp в объект datetime
            dt = datetime.datetime.fromtimestamp(int(timestamp))
            # Преобразуем дату и время в нужный формат
            formatted_dt = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            return formatted_dt

    @property
    def generate_password(self):
        # Определение наборов символов для пароля
        letters = string.ascii_letters  # Английские буквы в обоих регистрах
        digits = string.digits  # Цифры
        special_chars = string.punctuation  # Специальные символы

        # Количество символов в пароле (случайным образом выбираем от 8 до 16)
        password_length = random.randint(8, 16)

        # Гарантированно включаем минимум по одному символу из каждого набора
        password = random.choice(letters.upper())  # 1 символ верхнего регистра
        password += random.choice(letters.lower())  # 1 символ нижнего регистра
        password += random.choice(digits)  # 1 цифра
        # password += random.choice(special_chars)  # 1 специальный символ

        # Генерируем остальные символы пароля
        for _ in range(password_length - 3):
            password += random.choice(letters + digits)

        # Перемешиваем символы пароля, чтобы обеспечить случайность
        password_list = list(password)
        random.shuffle(password_list)
        password = random.choice(letters.upper()) + ''.join(password_list)

        return password

    @property
    def SolveCaptcha(self):
        self.cap = capmonster_python.RecaptchaV2Task(self.capKey)
        tt = self.cap.create_task("https://phaver.com", self.sitekey)
        # print(f"Created Captcha Task {tt}")
        captcha = self.cap.join_task_result(tt)
        # print(captcha)
        captcha = captcha["gRecaptchaResponse"]
        return captcha

    @property
    def CheckAccount(self):
        payload = {"email": self.email,
                   "password": self.password,
                   "returnSecureToken": True}
        # print(1)
        with self.session.post('https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyABU16fMP_LH45JHdtXM_N-wDtxuSgBkmE', json=payload) as response:
            return response.json()

    @property
    def generate_username(self) -> str:

        array = []
        with open('InputData/genereg_nicks.txt', 'r') as file:
            for i in file:
                array.append(i.rstrip())

        return random.choice(array)

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

# def generate_password():
    # Определение наборов символов для пароля
    # letters = string.ascii_letters  # Английские буквы в обоих регистрах
    # digits = string.digits  # Цифры
    # special_chars = string.punctuation  # Специальные символы
    #
    # # Количество символов в пароле (случайным образом выбираем от 8 до 16)
    # password_length = random.randint(8, 16)
    #
    # # Гарантированно включаем минимум по одному символу из каждого набора
    # password = random.choice(letters.upper())  # 1 символ верхнего регистра
    # password += random.choice(letters.lower())  # 1 символ нижнего регистра
    # password += random.choice(digits)  # 1 цифра
    # # password += random.choice(special_chars)  # 1 специальный символ
    #
    # # Генерируем остальные символы пароля
    # for _ in range(password_length - 3):
    #     password += random.choice(letters + digits)
    #
    # # Перемешиваем символы пароля, чтобы обеспечить случайность
    # password_list = list(password)
    # random.shuffle(password_list)
    # password = random.choice(letters.upper())+''.join(password_list)
    #
    # return password


if __name__ == '__main__':

    # print(generate_password())
    # input()

    proxies = []
    emails = []
    with open('InputData/Emails.txt', 'r') as file:
        for i in file:
            emails.append([i.rstrip().split(':')[0], i.rstrip().split(':')[1]])
    with open('InputData/Proxies.txt', 'r') as file:
        for i in file:
            proxies.append(i.rstrip())

    count = 800
    while True:

        try:
            acc = PhaverAccount(email=emails[count][0],
                                proxy=proxies[count],
                                capKey="")


            # print(acc.SolveCaptcha)
            # input()

            regStatus = False
            info = acc.CheckAccount
            if 'error' in info:
                if info['error']['message'] == 'EMAIL_NOT_FOUND':
                    logger.success(f'{count} - Почта не зарегистрирована, начинаем регистрацию нового пользователя ({acc.email})')
                else:
                    logger.error(f'{count} - Неизвестная ошибка - {info}')
            else:
                logger.success(f'{count} - Аккаунт уже существует, пропускаем почту')
                regStatus = True

            if regStatus:
                count += 1
                continue



            acc.Registration()
            logger.success(f'{count} - Токен сессии сгенерирован, проходим капчу')
            acc.SyncTokenMutation()
            logger.success(f'{count} - Капча пройдена')
            acc.RefreshToken()
            logger.success(f'{count} - Токен сессии обновлен')

            while True:
                nickname = acc.generate_username
                result = acc.CheckUsername(nickname)
                # print(result)
                if result['data']['profileByUsername']['id'] == None:
                    break

                # input()

            logger.success(f'{count} - Свободный никнейм - {nickname}')

            php_data = None
            while True:
                try:
                    php_data = acc.UploadPhotoOnServer()
                    if 'id' in php_data:
                        break
                    logger.success(f'{count} - Не удалось загрузить фото, повторяем попытку')
                except:
                    traceback.print_exc()
                    input()
            logger.success(f'{count} - Аватарка загружена')

            if 'data' in acc.UpdateProfileMutation(php_data['id'], nickname):
                logger.success(f'{count} - Данные профиля успешно сохранены')
            else:
                logger.error(f'{count} - Ошибка загрузки данных')

            print(acc.UpsertFlagMutation())
            logger.success(f'{count} - Данные профиля успешно сохранены')

            model = Account(gqlID = acc.gqlID,
                            owner = '',
                            refresh_token = acc.refresh_token,
                            email = acc.email,
                            password = acc.password,
                            email_password = emails[count][1],
                            username = nickname,
                            name = acc.name,
                            createdAt = datetime.datetime.utcnow())
            session.add(model)
            session.commit()

            logger.success(f'{count} - База данных обновлена\n')
        except Exception as e:
            logger.error(f'{count} - Ошибка - {str(e)}\n')

        count+=1










