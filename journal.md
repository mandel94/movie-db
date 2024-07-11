THIS IS A STILL UNEDITED JOURNAL OF THE MOVIE PROJECT. 

IT HELPS ME KEEP TRACK OF EVERYTHING, AND WHO KNOWS, MAYBE SOMEDAY I COULD SHARE IT OUT. 

'SCRIPTA MANENT' IS LATIN FOR 'WRITE IT DOWN TO TESTIFY THAT IT HAPPENED'. THIS JOURNAL IS A TESTIMONY TO THAT SPIRIT, AND TO THE SUFFERINGS THAT I HAD TO ENDURE TO CREATE MY ARTISANAL MOVIE DB. (*takes off the snooty socratic hat*)

CAVUEAT: I HAVE A PROBLEMATIC TENDENCY TO IRONY. HOPE THIS DOES NOT COMPROMISE THE QUALITY OF WHAT'S BELOW. 

## Why this project?
The idea is to create a big database of movies, by stitching together different sources extracted from the Great Sea of the Internet. 

I can store for each single movie, 



## Data collection approach
The idea is to create a `compose.yml` file to create an orchestrated suite of programs that, plain and simple, does it all for me, or for any other human being in this world that hates monkey-stitching data from some alieniating platform of the bore kind.



## Architecture

I am implementing a micro-services architecture, mainly because:
- From what I heard, delevoping new skills relating to microservices and service orchestration is paramount;
- Undoubtedly, it seems to me that combining services that are developed in complete isolation has clear advantages that overcome any of the sweating -- and swearing -- of going up the learning path -- the walls of my room must have heard a swearing or two, I apologetically have to admit.


## ⚔️Challenges 
I know I'll face challenges over challenges. Some of them will resemble the dreadful final boss of a [Soulslike game](https://en.wikipedia.org/wiki/Soulslike#:~:text=to%20the%20player.-,Common%20themes,spark%20players'%20desire%20to%20explore.); others will just semi-innocous creatures, little prickly stuff to smash like a real [Mario maniac](https://www.youtube.com/watch?v=rLl9XBg7wSs). you meet at the beginning of a Super Mario Bros level. Whatever the enemy, here is my diary.

I am writing it as the story unfolds. Let's hope it resembles a Zelda more than a Dante's Inferno (I promise I'll stop with the videogames analogies from now on).


### Get the list of movies
Who's telling the program which movie to look for. Of course I am not doing anything manually, despicably lazy me!
I need a list of movies, just to begin with. I decided that [JustWatch](https://www.justwatch.com/) maybe be for me. For those who don't know, JustWatch is like a TV guide, but for streaming. It's like a north star for the zeroed-eyed average man who is confortably zapping his life away on the couch. 
The website gives access to very long list of movies, partitioned by providers. I search for one of such lists, and this is how I encountered [this big list of movies](https://www.justwatch.com/us/provider/max/movies). It a very long gallery of movies that are being streamed in the [Max](https://www.max.com/) streaming provider. It is quite simple to change the provider section of the url -- the script does not change of a bit -- in order to get the same gallery but for another streaming provider. 
I decide that the url for Max is a good starting point.  
So the first challenge is:

> Create a spider that takes that takes the an url as input that has a gallery of movies inside. That gallery is converted into a json-formatted string. That json-formatted string is mocking a user who is explicitly telling the suite of programs what movie to scrape information for.


## The Contract
Communication is the transmission of information, based on some coding system that allow to express that information through a commonly accepted form of message. It is a gaming of encoding and decoding. I say something (encode phase), you have to understand it (decode phase). Ok, away with the self-concerning hat of I-know-it-all. This is just to say that because our micro-services are just a bunch of lone pieces of software, each with its own identity, each unawaringly playing a role in the bigger game of scraping a database, we must teach them how to talk, so they can coordinate.   
I decide to implement a common interfaces: A simple JSON object carrying a shared ground of knowledge over the network that our happy containers are connected to. Each container must know the properties of the JSON object, and what each property contains and how to deal with them -- that is, the **the rules of communication**.

If I break the JSON object, I break the communication system, and I must teach it over again to the containers.

STATUS QUO: The system is relying on files shared across containers (see [Volumes](#volumes) for more on this). 

## The Wiki API

The wiki service is a client that connects to Wikimedia [API Portal(https://api.wikimedia.org/wiki/Main_Page), by sending requests to a [Flask](https://flask.palletsprojects.com/en/3.0.x/) server. 
The (still-in-development) API Portal open access to Wikimedia content. The portal's website is raw as a freshman, but still educated enough to give me access to Wikipedia articles using Python. Exactly what I needed. 

I built a base `WikiClient` class, whose methods are to be encapsulated by any inheriting wiki client. Like a caring mother, the `WikiClient` deals with such basic things as searching for a page on wikipedia, with any additional logic to be implemented by inheriting classes. 
Presently, the only child class is `MovieWikiClient`, which uses the search functionality of its parent class, wrapping it around movie-specific logic. 

The `MovieWikiClient` class the `self.search_movie` method, which uses the inherited `self.search_page` method under the hood. For example, if the movie client must look for the "Avatar" page on Wikipedia, it first passes the "Avatar" query string to the `self.search_page` method; the result is than parsed out according [The Contract](#the-contract) and dealth with in order to understand which result is actually a movie. 

Calling "Avatar" through the base class `WikiClient` returns lots of results:
```json
{
  "how_many": 10,
  "pages": [
    {
      "description": "Material appearance or incarnation of a god on Earth in Hinduism",
      "excerpt": "or boxes, misplaced vowels or missing conjuncts instead of Indic text. <span class=\"searchmatch\">Avatar</span> (Sanskrit: \u0905\u0935\u0924\u093e\u0930, IAST: Avat\u0101ra; pronounced [\u0250\u028b\u0250t\u032aa\u02d0\u027e\u0250]) is a concept within",
      "id": 100368,
      "key": "Avatar",
      "matched_title": null,
      "thumbnail": {
        "duration": null,
        "height": 85,
        "mimetype": "image/jpeg",
        "url": "//upload.wikimedia.org/wikipedia/commons/thumb/5/57/Vishnu_Avatars.jpg/60px-Vishnu_Avatars.jpg",
        "width": 60
      },
      "title": "Avatar"
    },
    {
      "description": "2022 American film by James Cameron",
      "excerpt": "<span class=\"searchmatch\">Avatar</span>: The Way of Water is a 2022 American epic science fiction film directed and co-produced by James Cameron, who co-wrote the screenplay with Rick",
      "id": 25813358,
      "key": "Avatar:_The_Way_of_Water",
      "matched_title": null,
      "thumbnail": null,
      "title": "Avatar: The Way of Water"
    },
    {
      "description": "American animated television series",
      "excerpt": "<span class=\"searchmatch\">Avatar</span>: The Last Airbender, also known as <span class=\"searchmatch\">Avatar</span>: The Legend of Aang in some regions, is an American animated fantasy action television series created",
      "id": 1620586,
      "key": "Avatar:_The_Last_Airbender",
      "matched_title": null,
      "thumbnail": {
        "duration": null,
        "height": 26,
        "mimetype": "image/svg+xml",
        "url": "//upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Avatar_The_Last_Airbender_logo.svg/60px-Avatar_The_Last_Airbender_logo.svg.png",
        "width": 60
      },
      "title": "Avatar: The Last Airbender"
    },
    // TRUNCATED
  ]
}

```
The `how_many` in the json file key displays 10 results for "Avatar", not all of which are movie. The `MovieWikiClient` knows what a movie is, and parses and processes the json in such a way that only actual movies are returned:
```json
{
  "how_many": 5,
  "movies": [
    {
      "description": "2022 American film by James Cameron",
      "excerpt": "<span class=\"searchmatch\">Avatar</span>: The Way of Water is a 2022 American epic science fiction film directed and co-produced by James Cameron, who co-wrote the screenplay with Rick",
      "id": 25813358,
      "key": "Avatar:_The_Way_of_Water",
      "matched_title": null,
      "thumbnail": null,
      "title": "Avatar: The Way of Water",
      "url": "https://en.wikipedia.org/wiki/Avatar:_The_Way_of_Water"
    },
    {
      "description": "American animated television series",
      "excerpt": "<span class=\"searchmatch\">Avatar</span>: The Last Airbender, also known as <span class=\"searchmatch\">Avatar</span>: The Legend of Aang in some regions, is an American animated fantasy action television series created",
      "id": 1620586,
      "key": "Avatar:_The_Last_Airbender",
      "matched_title": null,
      "thumbnail": {
        "duration": null,
        "height": 26,
        "mimetype": "image/svg+xml",
        "url": "//upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Avatar_The_Last_Airbender_logo.svg/60px-Avatar_The_Last_Airbender_logo.svg.png",
        "width": 60
      },
      "title": "Avatar: The Last Airbender",
      "url": "https://en.wikipedia.org/wiki/Avatar:_The_Last_Airbender"
    },
// TRUNCATED
  ]
}
```

How does it do it is a black box, not in the sense of hiding some secret information that has been classified by *god-knows-which-higher-power*, but for the simpler reason that I don't know what the best solution for flagging movie is -- currently I rely on the rather unfashionable strategy of spotting flags in the `key` and `description` fields to reasonably state that *this is a movie*, but here I see the glitteering chance to flash some AI up, who knows...


I have to say, the Wiki Client is pampering me with gratifications, and everything seems to work blessingly fine for know. But I know that the devil will go after me, it's just a matter of time.

## OpenAPI Specification

When building an API, it's important to remember that we are building a product. The product has users, and those users might want to know how to use it. 

Having no instructions puts the API user is an worse position than an IKEA do-it-yourself drawer assembler who lost the user manual: The latter can do its best to find a solution anyway, the former doesn't even know from where to start. 

The [OpenAPI Specification (OAS)](https://swagger.io/specification/) is a standardized form to produce such an instruction manual. Using a standard format is great in many ways:
* it doesn't depend on any specific programming language;
* the specification can be used as in input for applications that understand the OAS specification, enabling such great functionalities as code generation, testing, automatic documentation and other use cases. 

I decided that all APIs happily stemming from the my movie suite would be based on OpenAPI definitions, in the form of .yaml files. Well, not so happily. I struggled with CORS. What can be worse than CORS? *Cross-origin resource sharing*, you know... do you? Do you?! Well, before my sanity went insane, I actually had never heard of it.


#### What is CORS? 

I present you *Cross-origin resource sharing*. Sure, not the friendliest name, but you'd better make friends with him, because that is what protects us happy-go-lucky internet surfers.
CORS is a way to dictate how web pages can request resources (like data or content) from another domain (website). Resources can include images, styleshets, scripts; but also fonts, video and audio files, iframe content, or the endpoints of an API. 
Resources-sharing is when a domain different from the one hosting those resources asks for them. For example, you might need to access to Spotify API for creating a playlist widget in your website. In that case, the resources are hosted somewhere else over the internet, in the Spotify domain, that's different from your domain. You'll need to ask for those resources to the Spotify server.

When talking CORS, we must be careful not to mix up origin with domain. The latter is contained in the former, being the combination of three components:
1. Scheme (Protocol): This refers to the protocol used to access the resource, such as http, https, ftp, etc.
2. Hostname (Domain): This is the domain name or IP address of a server, like example.com or 192.168.1.1.
3. Port: This is the port number on the server through which the resource is accessed.The default port is 80 for HTTP and 443 for HTTPS, but other ports can be specified.

If a request come from the same domain, it doesn't necessarily come from the same origin -- it might come from a different port on the same domain, or it could use a different communication protocol. 

CORS policies are managed by the server hosting the resources, whose configuration will include specific headers in its responses, and those headers describe which origins can access data from the server. 

According to the CORS security model, requests that might change the data in the web server -- requests other than GET, HEAD and POST with certain MIME types, or requests including custom headers  -- should send a pre-flighted request before, so that the web server can precautiously verify if the request is allowed, and only after successful verification the (state-changing) request is sent. 

On the contrary, when requests include simple GET, HEAD and POST methods, have no exotic `Content-Type` nor exotic custom headers, the browser will send a [simple request](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#simple_requests) to the web server. 

Any information useful for implementing the CORS policy is passed through headers. 
Back to the Spotify example -- incorporate a playlist widget into your website. When you ask Spotify for your music data, the browser will send a request the Spotify server with an Origin header. That Origin will than seep through the web server CORS policy, which will determine is the request is allowed  or disallowed. In the first case, we could hear the music of our future playlist rocking in your head, firstly from a far distance, than clear and loud when we receive a response from the Spotify web server with an Access-Control-Allow-Origin header, triggering the browser to finally deliver the music data we were striving for.  

#### My painful CORS chronicle 

Ok, that's the end of the CORS presentation. Now that we have fed our paranoid with all those security concerns, we can go back to CORS-related issue. In one-liner, our Swagger API origin was not allowed to access the resources from our Wiki API origin. I was CORS-ignorant, and it was not good to see this image:
![cors_error](./images/cors_error.png)

It was indeed a CORS error
![cors_error_indeed](./images/cors_error_indeed.png)

After two afternoons of having my spine refilled with alternating currents of "I did it" and "I hate it", I finally didn't made it. I thought that Flask hated me, because the problem seemed to unexplicably go away when I removed dynamic routes (i.e. urls with named variables) -- in which case the server applied the permissive CORS policy I'd previously set. Only apparently, however, as the web server still continued to ignore those policies in an haphazard fashion, with the CORS error appearing even without dynamic routes on the wiki API web server. 

After a while, I realized that the CORS error might have been the sympton of some deeper flask illness. 

The devil came at last, and it took its toll on me.

At the end of all of it -- two days of scratching my head until it caught fire --  it happened to be an "URL not found error" when calling the `/v1/search/pages` with query string attached. In contrast, when calling the `/v1/search/movies` endpoint everything worked as smooth as Michael Jackson. My final guess is that Flask couldn't route the request to the proper url when calling the pages endpoint, resulting in a response uncompliant with the CORS security model.  
 




📚 Some useful API resources:
* [Best practices in API design](https://swagger.io/resources/articles/best-practices-in-api-design/)  
* [Designing APIs with Swagger and OpenAPI](https://learning.oreilly.com/library/view/designing-apis-with/9781617296284/Text/ch04.htm#sigil_toc_id_61)



## The Crawling Module




## Data Model

The following is a data model of the database. Being a layman of the move industry, I had to do the research homeworks, to understand -- or at least, trying to -- what's more relevant to the average stakeholder of such an indsutry. 

Having no idea of how to start collecting feedbacks from potential users of a platform that does not exist even in my very mind, I tried to imagine what would have been of any use *to me*: 
* What would I like to have access to in a movie database?
* What kind of applications could I build if I designed the database in a specific way instead of another?

### Relational vs Non-relational

I forced myself to use a relational database. Not because I thaught if was a better solution -- in the world of databases, I'd feel unconfortable even stating such dummy things as *according to my experience the sky is bluer than the sun* -- but because of two simpler reasons:
* I heard talking relational more than non-relational;
* (partly related to the previous point) I couldn't wrap my mind around where to start. So I said, let it be relational, and let later be later;

### The DB schema

The following is a an ERM schema of my movie model, with a big WORKING IN PROGRESS sign stating that everything could change, anytime.

If you ever saw Inside Out 2 -- if not, I advise you to do it with lots of handkerchiefs close to you -- you know that anxiety is the master-head of planning. As the master-of-anxiety that I am, I could not keep my self from finding a way to ease things up if I ever had to change the design of my model. 

#### Stating a Source of truth for the schema
The idea was to create a unique source of truth about the database schema. Not only this source of truth needed to be unique for all services speaking to my movie database, but it had to be understandable by all of them, no matter which programming logic those different services implemented.

**TODO** Create a single source of for the database schema.

Back to the communication issue, the schema should be in a format that's standard across services. 
Which containers are directly referring to the database schema?

**Object-relational mapping**: the `movie_db` client refers to the schema for the purpose of mapping python classes to the 
the database engine. If your bubbling your head up and down, this means to following
1. We need to talk to the database to perform database operations (insert, update, delete, etc.);
2. We want to do it in python -- in a word, do it programmagically; 
3. To do it, we need to attach python classes (one for each db entity) to the database, to use those classes as spatial-gateways /
  interdimensional-portals / any other asimovian sci-fi metaphor connecting to the db -- talk to the db in pythonic language.

This is mind-warpely called **Object-relational mapping**, and we can do it with [SQLAlchemy](https://www.sqlalchemy.org/) -- a *don't-asky-why-it-works* magical package that allows you to easily speak SQL in python.
database operations,   

### Overview of the Services

#### Initialize the database
Service name: `init_movie_db`
What does it do?
* uses the [official postgres image](https://hub.docker.com/_/postgres) to initialize the movie_db database if it doesn't exist yet

#### Movie DB Client

Service name: `movie_db_client`
What does it do?
* exposes endpoints for interacting with the movie_db database. This is the suite entrypoint for all database operations;

This service implements ORM mapping using [SQLAlchemy](https://www.sqlalchemy.org/) package.
I decided to implement the [repository pattern](https://www.cosmicpython.com/book/chapter_02_repository.html), which decouples the model layer from the data layer. This meant creating two distinct modules:
* the `data_model` module, that maps python classes to the already initialized movie_db; 
* the `repository` module, which creates an abstract `Repository` class for doing db operations (read, insert, etc.). This module does not directly depend on the storage layer. Instead, it initializes the db_entity instances assuming they are stored directly in-memory. For example

The repository pattern adds an abstraction to the underlying SQL ORM moadule, which would allow in the future to substitue SQLAlchemy for any other ORM implementation; the programming logic wrapping around the specific implementation won't need to change;



#### The Crawling Module
Service name: `crawling_module`
What does it do?
* It scrapes the data all over our data sources;

This services implements a scraping routine based on [Scrapy](https://scrapy.org/), an open-source framework for extracting data from websites. This was an easy choice, as I already used Scrapy multiple times for other scraping projects (specifically, the sadly incompleted projects [building_NBA_database](https://github.com/mandel94/building_NBA_database) and [daXouse](https://github.com/mandel94/daXouse))

This service deploys the following spiders:
* `MovieListSpider`, which spits out the list of movies to be scraped;
* `MovieSpider`, which starts from the list of movies above and scrapes specific movie data across all the sources;


The Dockerfile's ENTRYPOINT is the `run_spiders.py` script, which runs tall the spiders it finds in the folder of the scrapy project using a `scrapy.crawler.CrawlingProcess`. This python script will serve as a sort of orchestration point of the scraping activity. 
P.S. For the sake of honesty, I humbly tried to implement this orchestration using `scrapy.crawler.CrawlerRunner` object, but humbly failed in front of such a soul-devastating event like *a freaking bug that I cannot freaking understand!* 
It was sad, as I understood that [running spiders from a CrawlerRunner](https://stackoverflow.com/questions/39706005/crawlerprocess-vs-crawlerrunner) gives you more flexibility in terms of [thread-safety](https://en.wikipedia.org/wiki/Thread_safety).
 



## Microservices architecture

### Sharing the data
One difficulty with working with containers is to share data across services. The data dies with the container. Docker gives to options to persist data on the host machine: 
* (*legacy solution)* [Bind mounts](https://docs.docker.com/storage/bind-mounts/), which mounts the container to files or directories existing on the host machine; this solution creates a dependency on the host's specific directory structure and operating system, so that -- as explicitly stated by Docker documentation -- volumes are to be preferred;
* [Docker volumes](https://docs.docker.com/storage/volumes/): They are better than bind mounts in so many ways: easier to manage; easier to share across containers; easier to migrate wherever you want; they don't need to reflect a directory structure on the host machine; 



### Volumes
Containers are isolated pieces of software, and volumes are an easy way to share data across containers.

Here is a list of volumes I created for the movie_db suite:
* `movie_db_movie_data`, shared by:
* `movie_db_movie_logs`: This volume persist all the logs produced by the application. This is a one-shop for logs, useful for debugging, and in general for orderly keeping track of the coding process. This volume contains a `movie_list.jsonl` file, with all the movies to be scraped, plus  
* `postgres_data`: This volumes stores the da ta in a [PostgreSQL](https://www.postgresql.org/) database. 

### Combining the services

The docker `compose.yml` file to run our multi-container application is the following:
```yml
name: movie_db

services:
  wiki_api_service:
    build: ./wiki_api
    ports:
      - "5000:5000"
    volumes:
      - ./wiki_api:/app
      - logs:/logs
    networks:
      - crawling_network
  crawling_service:
    build: ./crawling_module
    volumes:
      - movie_data:/movie_data
      - logs:/logs
      - ./crawling_module:/app
    networks:
      - crawling_network
    depends_on:
      - wiki_api_service
  movie_db:
    image: postgres
    container_name: movie_db
    restart: always
    shm_size: 128mb
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 123456789
    volumes:
      - ./db:/var/lib/postgresql/data
    command: postgres >logfile 2>&1 &
    ports:
      - "5432:5432"

networks:
  crawling_network:
    driver: bridge

volumes:
  db:
    driver: local
  movie_data:
    driver: local
  logs:
    driver: local

```



