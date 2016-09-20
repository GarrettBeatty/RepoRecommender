from github import Github
import heapq
from collections import defaultdict

topX = 50

apikey = open("apikey.txt", "r").read()
g = Github(apikey)

userName = input("Enter username: ")

#get topX of repos the user has starred

repos = g.get_user(userName).get_starred()[:topX]

repoStarDic = defaultdict(list)

#gets all of users starred repos the user has starred
for repo in repos:
	repoStarDic[repo.full_name] = []
	for user in repo.get_stargazers()[:topX]:
		repoStarDic[repo.full_name].append(user.login)

userCount = {}
#finds users with most overlaps
for key, values in repoStarDic.items():
	for v in values:
		if not v in userCount:
			userCount[v] = 1
		else:
			userCount[v] = userCount[v] + 1

topXUsers = heapq.nlargest(topX, userCount, key=userCount.get)

repoCount = {}

#gets the repos that that they starred and find ones with most overlaps
for user in topXUsers:
	repos = g.get_user(user).get_starred()[:topX]
	for repo in repos:
		if not repo.full_name in repoCount:
			repoCount[repo.full_name] = 1
		else:
			repoCount[repo.full_name] = repoCount[repo.full_name] + 1

#suggests those repos
topXRepos = heapq.nlargest(5, repoCount, key=repoCount.get)

print(topXRepos)