import scrapy

"""
To get movie-related info from http://128.2.204.215:8080/movie/movieID, run following command in get_user_movie_info (outer) folder.
    scrapy crawl movieInfo
This generates movie_info.txt, each line contains info about one movie.
"""

class MovieInfoSpider(scrapy.Spider):
    name = "movieInfo"

    def start_requests(self):
        with open('movies.txt', 'r') as file:
            movies = [movie.strip('\n') for movie in file.readlines()]
        prefix = 'http://128.2.204.215:8080/movie/'
        urls = [prefix + movie for movie in movies]
        for i, url in enumerate(urls):
            if i % 1000 == 0:
                print(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        with open('movie_info.txt', 'a') as f:
            f.write(response.text + '\n')