import requests
import pandas as pd
headers: {

}
userdf=pd.DataFrame(columns=['username','name','url','location','followers','publicRepositories'])
repodf=[]
def getuser(username):
    url = "https://api.github.com/users/"+str(username)
    response = requests.get(url)

    if (response.status_code == 200):
        uinfo=response.json()
        # df.append({'username':uinfo['login'],
        #            'name':uinfo['name'],
        #            'url':uinfo['html_url'],
        #            'location':uinfo['location'],
        #            'followers':uinfo['followers'],
        #            'publicRepositories':uinfo['public_repos']})
        # print(df)
        print("Username:            " + str(uinfo['login']))
        print("Name:                " + str(uinfo['name']))
        print("Page:                " + str(uinfo['html_url']))
        print("Location:            " + str(uinfo['location']))
        print("Followers:           " + str(uinfo['followers']))
        print("Public repositories: " + str(uinfo['public_repos']))

# def userdf(uinfo):
#
def getrepo(username):
    url= "https://api.github.com/users/%s/repos"%(username)
    response = requests.get(url)

    if (response.status_code == 200):
        repos = response.json()
        for repo in repos:
            repodf.append([repo['language'],repo['id']])
            # print(repo['description'])
            # print(repo['language'])
            repodf2=pd.DataFrame(repodf)
        print(repodf2.sort_values(by=1))


getuser('JakeWharton')
getrepo('JakeWharton')
