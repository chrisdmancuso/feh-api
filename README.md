# feh-api-project-v1

A [FastAPI](https://fastapi.tiangolo.com/) project, designed to serve users game information pertaining to the [Nintendo](https://www.nintendo.com/) mobile game, [Fire Emblem: Heroes](https://fire-emblem-heroes.com/en/).
Utilizes [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for web scraping 
and [FireBase](https://firebase.google.com/) noSQL Realtime Database for data storage.
Cloud hosting by [Deta](https://www.deta.sh/).

See the project in action [here](https://feh-api.deta.dev/docs).
## The Project:

Using BeautifulSoup, data was scraped from [here](https://feheroes.fandom.com/wiki/Level_40_stats_table) and 
[here](https://feheroes.fandom.com/wiki/Hero_skills_table) and then pushed to the FireBase DB
by using [fehSoup.py](fehSoup.py).

Then, using FastAPI, [endpoints](main.py) were created that allow users to retrieve requested data from the DB.

## Endpoint Examples:

#### Search By Name:
![feh-api-example](https://user-images.githubusercontent.com/31321037/179052384-c7943783-08ea-4264-9160-ab9dab583590.png)

#### Retrieve Unit Info By Name:
![feh-api-example2](https://user-images.githubusercontent.com/31321037/179052919-cd672c86-7090-4eb1-ba4c-d26e09c32f87.JPG)
