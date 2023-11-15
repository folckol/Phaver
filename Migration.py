from DB import *

pr = []
with open('InputData/Proxies.txt', 'r') as file:
    for i in file:
        pr.append(i.rstrip())

accounts = session.query(Account).all()

count = 0
for i in accounts:
    l = Account2(gqlID = i.gqlID,
                owner = i.owner,
                refresh_token = i.refresh_token,
                email = i.email,
                password = i.password,
                email_password = i.email_password,
                username = i.username,
                name = i.name,
                proxy = pr[count],
                credLevel = i.credLevel,
                createdAt = i.createdAt,
                postsCount = i.postsCount,
                followings = i.followings,
                followers = i.followers,
                likesCount = i.likesCount,
                retweetsCount = i.retweetsCount)
    session.add(l)
    session.commit()
    count+=1




