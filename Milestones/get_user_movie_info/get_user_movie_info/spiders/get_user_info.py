import scrapy

"""
To get movie-related info from http://128.2.204.215:8080/user/userID, run following command in get_user_movie_info (outer) folder.
    scrapy crawl userInfo
This generates user_info.txt, each line contains info about one user.
"""


class UserInfoSpider(scrapy.Spider):
    name = "userInfo"

    def start_requests(self):
        with open('users.txt', 'r') as file:
            users = [user.strip('\n') for user in file.readlines()]
        prefix = 'http://128.2.204.215:8080/user/'
        urls = [prefix + user for user in users]
        for i, url in enumerate(urls):
            if i % 1000 == 0:
                print(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        with open('user_info.txt', 'a') as f:
            f.write(response.text + '\n')