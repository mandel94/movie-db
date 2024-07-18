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

I implemented a micro-services architecture, mainly because:
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
> After getting the list of movie, I'll make a call to the another spider, who'll read the list and create the actual entities to populate the database, following all relevant urls for getting the information needed. 


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

Having no instructions puts the API user is an worse position than an IKEA do-it-yourself drawer assembler who lost the user manual: The latter can do its best to find a solution anyway, the former doesn't even know where to start from. 

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

I was lost on research, so I asked the Great Wizard of Oz, modern version, aka chatGPT, what a movie domain expert would
have considered when populating a movie db. I stared at the monitor with the typical expression of a golden fish on choloroform, as 
the AI was pouring business wisdom at me, and realized that some things need not be done by a human, we like it or not.
I received a comprehensive schema of the movie db, with table relationships resolved 
according to their [cardinality](https://www.coursera.org/articles/cardinality) --  *Hail to the Great Wisdom of Oz*


| Field Name                | Data Type       | Description                                                                              |
|---------------------------|-----------------|------------------------------------------------------------------------------------------|
| `movie_id`                | INT (Primary Key, Auto Increment) | Unique identifier for each movie.                                     |
| `title`                   | VARCHAR(255)    | The official title of the movie.                                                          |
| `original_title`          | VARCHAR(255)    | The original title of the movie if different from the official title.                     |
| `tagline`                 | VARCHAR(255)    | The movie's tagline.                                                                      |
| `plot`                    | TEXT            | A brief summary of the movie's plot.                                                      |
| `genre`                   | VARCHAR(255)    | The genre(s) of the movie (e.g., Action, Comedy, Drama).                                  |
| `language`                | VARCHAR(50)     | The primary language of the movie.                                                        |
| `country`                 | VARCHAR(50)     | The country where the movie was produced.                                                 |
| `release_date`            | DATE            | The official release date of the movie.                                                   |
| `runtime`                 | INT             | The runtime of the movie in minutes.                                                      |
| `budget`                  | DECIMAL(15, 2)  | The production budget of the movie.                                                       |
| `box_office`              | DECIMAL(15, 2)  | The total box office earnings.                                                            |
| `rating`                  | DECIMAL(3, 1)   | The average rating of the movie (e.g., from IMDb or Rotten Tomatoes).                      |
| `rating_count`            | INT             | The number of ratings the movie has received.                                             |
| `director_id`             | INT             | Foreign key referencing the Directors table.                                              |
| `writer_id`               | INT             | Foreign key referencing the Writers table.                                                |
| `studio_id`               | INT             | Foreign key referencing the Studios table.                                                |
| `distributor_id`          | INT             | Foreign key referencing the Distributors table.                                           |
| `poster_url`              | VARCHAR(255)    | URL to the movie's poster image.                                                          |
| `trailer_url`             | VARCHAR(255)    | URL to the movie's trailer.                                                               |
| `age_rating`              | VARCHAR(10)     | The movie's age rating (e.g., PG, R).                                                     |
| `imdb_id`                 | VARCHAR(50)     | The IMDb ID for the movie.                                                                |
| `tmdb_id`                 | VARCHAR(50)     | The TMDB ID for the movie.                                                                |
| `homepage`                | VARCHAR(255)    | The official homepage for the movie.                                                      |
| `created_at`              | TIMESTAMP       | Timestamp when the record was created.                                                    |
| `updated_at`              | TIMESTAMP       | Timestamp when the record was last updated.                                               |

### Table: Directors

| Field Name  | Data Type       | Description                             |
|-------------|-----------------|-----------------------------------------|
| `director_id` | INT (Primary Key, Auto Increment) | Unique identifier for each director.  |
| `name`        | VARCHAR(255)    | The name of the director.               |
| `dob`         | DATE            | Date of birth of the director.          |
| `bio`         | TEXT            | Biography of the director.              |
| `nationality` | VARCHAR(50)     | Nationality of the director.            |
| `created_at`  | TIMESTAMP       | Timestamp when the record was created.  |
| `updated_at`  | TIMESTAMP       | Timestamp when the record was last updated. |

### Table: Writers

| Field Name  | Data Type       | Description                             |
|-------------|-----------------|-----------------------------------------|
| `writer_id`   | INT (Primary Key, Auto Increment) | Unique identifier for each writer.    |
| `name`        | VARCHAR(255)    | The name of the writer.                 |
| `dob`         | DATE            | Date of birth of the writer.            |
| `bio`         | TEXT            | Biography of the writer.                |
| `nationality` | VARCHAR(50)     | Nationality of the writer.              |
| `created_at`  | TIMESTAMP       | Timestamp when the record was created.  |
| `updated_at`  | TIMESTAMP       | Timestamp when the record was last updated. |

### Table: Studios

| Field Name  | Data Type       | Description                             |
|-------------|-----------------|-----------------------------------------|
| `studio_id`  | INT (Primary Key, Auto Increment) | Unique identifier for each studio.    |
| `name`       | VARCHAR(255)    | The name of the studio.                 |
| `location`   | VARCHAR(255)    | The location of the studio.             |
| `founded`    | DATE            | The date the studio was founded.        |
| `created_at` | TIMESTAMP       | Timestamp when the record was created.  |
| `updated_at` | TIMESTAMP       | Timestamp when the record was last updated. |

### Table: Distributors

| Field Name  | Data Type       | Description                             |
|-------------|-----------------|-----------------------------------------|
| `distributor_id` | INT (Primary Key, Auto Increment) | Unique identifier for each distributor.|
| `name`           | VARCHAR(255)    | The name of the distributor.           |
| `location`       | VARCHAR(255)    | The location of the distributor.       |
| `created_at`     | TIMESTAMP       | Timestamp when the record was created. |
| `updated_at`     | TIMESTAMP       | Timestamp when the record was last updated.|

### Table: Cast

| Field Name  | Data Type       | Description                             |
|-------------|-----------------|-----------------------------------------|
| `cast_id`     | INT (Primary Key, Auto Increment) | Unique identifier for each cast member. |
| `movie_id`    | INT             | Foreign key referencing the Movies table.|
| `actor_id`    | INT             | Foreign key referencing the Actors table.|
| `role`        | VARCHAR(255)    | The role played by the actor.            |
| `billing_order` | INT           | The order of billing for the actor.      |
| `created_at`  | TIMESTAMP       | Timestamp when the record was created.  |
| `updated_at`  | TIMESTAMP       | Timestamp when the record was last updated. |

### Table: Actors

| Field Name  | Data Type       | Description                             |
|-------------|-----------------|-----------------------------------------|
| `actor_id`   | INT (Primary Key, Auto Increment) | Unique identifier for each actor.     |
| `name`       | VARCHAR(255)    | The name of the actor.                  |
| `dob`        | DATE            | Date of birth of the actor.             |
| `bio`        | TEXT            | Biography of the actor.                 |
| `nationality`| VARCHAR(50)     | Nationality of the actor.               |
| `created_at` | TIMESTAMP       | Timestamp when the record was created.  |
| `updated_at` | TIMESTAMP       | Timestamp when the record was last updated. |

### Table: Ratings

| Field Name  | Data Type       | Description                             |
|-------------|-----------------|-----------------------------------------|
| `rating_id`   | INT (Primary Key, Auto Increment) | Unique identifier for each rating.    |
| `movie_id`    | INT             | Foreign key referencing the Movies table.|
| `source`      | VARCHAR(255)    | The source of the rating (e.g., IMDb, Rotten Tomatoes). |
| `score`       | DECIMAL(3, 1)   | The rating score.                       |
| `created_at`  | TIMESTAMP       | Timestamp when the record was created.  |
| `updated_at`  | TIMESTAMP       | Timestamp when the record was last updated. |

### Table: Genres

| Field Name  | Data Type       | Description                             |
|-------------|-----------------|-----------------------------------------|
| `genre_id`   | INT (Primary Key, Auto Increment) | Unique identifier for each genre.     |
| `name`       | VARCHAR(255)    | The name of the genre.                  |
| `created_at` | TIMESTAMP       | Timestamp when the record was created.  |
| `updated_at` | TIMESTAMP       | Timestamp when the record was last updated. |

### Table: Movie_Genres

| Field Name  | Data Type       | Description                             |
|-------------|-----------------|-----------------------------------------|
| `movie_id`  | INT             | Foreign key referencing the Movies table.|
| `genre_id`  | INT             | Foreign key referencing the Genres table.|

This setup allows for a normalized database design, where related entities like directors, writers, studios, and actors are stored in their respective tables, enabling efficient querying and management of data. The use of foreign keys ensures referential integrity between tables.

*Oz: Could you convert this to sqlalchemy?* 
I spare you the details, but you can now understand how unexpectedly easy it's been to create not ony my first migration 
script, but THE WHOLE DESIGN OF MOVIE DB!  


<!-- If you ever saw Inside Out 2 -- if not, I advise you to do it with lots of handkerchiefs close to you -- you know that anxiety is the master-head of planning. As the master-of-anxiety that I am, I could not keep my self from finding a way to ease things up if I ever had to change the design of my model.  -->




**Useful resources** 📚:
* [How to manage DB migrations](https://nikhilakki.in/what-is-alembic)
 

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

The [movie_db_client](#movie-db-client) carries the weight of talking to the postgres database. As such a duty-bearer, it implements the movie db data model in python. It surely needs to know if some change has occurred in the schema of the movie database:
* A new table was born;
* Some was dropped;
* Some columns has been changed type;
* Etc.

In one word: Schema. The movie_db_client should have visibility on the schema of the database. Always. 
One way to do this is to incorporate the schema directly on the db client package -- in native SQLAlchemy, so to say. In this case, I can manually tweak the client code to implement the changes in the db schema. 
Stil, there is a problem with this solution. What if other packages need to know about the schema? The change in the client db would not reflect on those packages, breaking our devs heart in pieces together with their code. 
<!-- Is there such a dependent package? Of course, the [Crawling module](#the-crawling-module). This module scrapes the very data that will feed the database, so if surely need to have access to the db schema, else it won't know how to build the Scrapy items out of web resources.  -->

<!-- For example, if I decided to add a producer's table to the database, I would change the schema. This would reflect on the movie database through the movie client, that deals with implementing the data model and has always-on visibility on the schema (because the schema is incorporated directly in the client's code). Still, the crawling module would ignore this change, and ignore the need to search for producers information. This is not a problem in itself, because it only means that the newly created producers' table will stay empty, untill I finally add a new crawling sub-module that specifically deals with scraping information about movie producers. The code won't break. But imagine now if the instead of adding a new table I added a new producer column in the movie table, and some business stakeholder required me to make this feature required. This change in the schema means that the database won't accept news movies without producer column.  -->
 


How to get always-on visibility on the schema? 

### Implementing the database design
Once I defined the basic design of the database, I didn't know at first how to 
implement that design. I had two alternative options:
* writing a model.py script within the movie_db_client;
* create a seprate service to perform such structural db operations as table creations, updates, and in general to perform data migrations. 

I read [this](https://stackoverflow.com/questions/30425214/what-is-the-difference-between-creating-db-tables-using-alembic-and-defining-mod), figured it out, and chose for option two -- and had experienced that cosy feeling when you find
the exact stackoverflow comment you needed, on the spot.

Following the stackwoverflow posts, the steps are:
1. Write the model classes;
2. Generate a migration file that peeks into my model and generate the necessary database code.

Alemebic matches what it sees in the model classes with the current schema of the database, automatically bridging any gap, and making sure those schema are reflected in the database, which is thus upgraded to a newer version.  

The same goes for downgrades: If you want to sync your db back to an older version, Alembic gives you a way to automate that process with simple migration scripts. 

The only caveaut is that even the Alembic auto-magic sometimes goes *AzKhazan*, so a manual check add pains but is surely for the best.  

I initialized the Alemebic project as a sub-folder of the `data_model` folder inside the movie_db_client module. 

I first changed the `.ini` file to ensure connectivity to the movie database, adding the address that points to the postgresql engine.
This came with a firts challenge: How to setup alembic configurations when I have multiple databases. I had to add multiple configuration headers in the `.ini` file, in place of the [alembic] section: 

```ini
[movie_db]
script_location = alembic
prepend_sys_path = .
version_path_separator = os  
sqlalchemy.url = postgresql://postgres:123456789@localhost:5432/movie_db


[test_db]
script_location = alembic
prepend_sys_path = .
version_path_separator = os  
sqlalchemy.url = postgresql://postgres:123456789@localhost:5433/test_db
```

After that, I modified the `env.py` file, inspired by [this article](https://learningtotest.com/2021/06/17/managing-alembic-migrations-with-a-single-alembic-ini-env-py/). The function definition for online migration is:


```py
def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # https://learningtotest.com/2021/06/17/managing-alembic-migrations-with-a-single-alembic-ini-env-py/
    
    section = config.get_section(config.config_ini_section)
    # # Inject environment variable values into connection string
    url = section["sqlalchemy.url"]

    section["sqlalchemy.url"] = url
    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )


    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```


I initialized a migration script template to build a first version of the db -- my first revision:
```
>>> alembic revision -m "create db tables"
```

I then populated the migration script's upgrade function ([see here the final migration script](#the-db-schema)). The code material was courtesy of chatGPT (see [how I invoked AI-man to design my database](#the-db-schema))


```python
"""create db tables

Revision ID: a3eaf7723ce5
Revises: 
Create Date: 2024-07-16 15:28:26.478149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3eaf7723ce5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
            'directors',
            sa.Column('director_id', sa.Integer, primary_key=True, autoincrement=True),
            sa.Column('name', sa.String(255), nullable=False),
            sa.Column('dob', sa.Date, nullable=True),
            sa.Column('bio', sa.Text, nullable=True),
            sa.Column('nationality', sa.String(50), nullable=True),
            sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
            sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
        )

    # Create Writers table
    op.create_table(
        'writers',
        sa.Column('writer_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('dob', sa.Date, nullable=True),
        sa.Column('bio', sa.Text, nullable=True),
        sa.Column('nationality', sa.String(50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Studios table
    op.create_table(
        'studios',
        sa.Column('studio_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('founded', sa.Date, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Distributors table
    op.create_table(
        'distributors',
        sa.Column('distributor_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('location', sa.String(255), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Actors table
    op.create_table(
        'actors',
        sa.Column('actor_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('dob', sa.Date, nullable=True),
        sa.Column('bio', sa.Text, nullable=True),
        sa.Column('nationality', sa.String(50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Genres table
    op.create_table(
        'genres',
        sa.Column('genre_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Movies table
    op.create_table(
        'movies',
        sa.Column('movie_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('original_title', sa.String(255), nullable=True),
        sa.Column('tagline', sa.String(255), nullable=True),
        sa.Column('plot', sa.Text, nullable=True),
        sa.Column('language', sa.String(50), nullable=True),
        sa.Column('country', sa.String(50), nullable=True),
        sa.Column('release_date', sa.Date, nullable=True),
        sa.Column('runtime', sa.Integer, nullable=True),
        sa.Column('budget', sa.Numeric(15, 2), nullable=True),
        sa.Column('box_office', sa.Numeric(15, 2), nullable=True),
        sa.Column('rating', sa.Numeric(3, 1), nullable=True),
        sa.Column('rating_count', sa.Integer, nullable=True),
        sa.Column('director_id', sa.Integer, sa.ForeignKey('directors.director_id'), nullable=True),
        sa.Column('writer_id', sa.Integer, sa.ForeignKey('writers.writer_id'), nullable=True),
        sa.Column('studio_id', sa.Integer, sa.ForeignKey('studios.studio_id'), nullable=True),
        sa.Column('distributor_id', sa.Integer, sa.ForeignKey('distributors.distributor_id'), nullable=True),
        sa.Column('poster_url', sa.String(255), nullable=True),
        sa.Column('trailer_url', sa.String(255), nullable=True),
        sa.Column('age_rating', sa.String(10), nullable=True),
        sa.Column('imdb_id', sa.String(50), nullable=True),
        sa.Column('tmdb_id', sa.String(50), nullable=True),
        sa.Column('homepage', sa.String(255), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Ratings table
    op.create_table(
        'ratings',
        sa.Column('rating_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('movie_id', sa.Integer, sa.ForeignKey('movies.movie_id'), nullable=False),
        sa.Column('source', sa.String(255), nullable=False),
        sa.Column('score', sa.Numeric(3, 1), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Cast table
    op.create_table(
        'cast',
        sa.Column('cast_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('movie_id', sa.Integer, sa.ForeignKey('movies.movie_id'), nullable=False),
        sa.Column('actor_id', sa.Integer, sa.ForeignKey('actors.actor_id'), nullable=False),
        sa.Column('role', sa.String(255), nullable=False),
        sa.Column('billing_order', sa.Integer, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)
    )

    # Create Movie_Genres table
    op.create_table(
        'movie_genres',
        sa.Column('movie_id', sa.Integer, sa.ForeignKey('movies.movie_id'), primary_key=True),
        sa.Column('genre_id', sa.Integer, sa.ForeignKey('genres.genre_id'), primary_key=True)
    )


def downgrade() -> None:
    pass
```

I finally run the db migration for both the movie db and the test db:

```>>> alembic --name movie_db upgrade head```
```>>> alembic --name test_db upgrade head```


Where `head` points to the file of the last migration.

Wishful thinking: It would be great to automate those two commands above with docker, so that each time the db client container is run all the last found migrations (referenced by `head`) are automatically executed. 

I have to say, the coding experience sometimes can be the pros of swearing-milker, 
but when code works as expected it's like rolling down a fluffy hill: you can feel 
the nice warmth of a coding day that ended like it *had* to end, and you can go 
doing some sports with a smile on your face. The evening where I successfully did
my first data migration, I had one hour of non-stop cycling, feeling like a happy kid from a 
Stephen King's book having a light-hearted ride -- hoping to stay free from nightmares to come.  


<!-- Helpful resource: https://stackoverflow.com/questions/30425214/what-is-the-difference-between-creating-db-tables-using-alembic-and-defining-mod  -->


#### Load tables in SQLAlchemy
The db had finally born with al its tables. Still, it was empty as the Black Rock Desert. We had to transform those dunes into
the Hollywood Hills, a place brimming with lively directors, ingenious writers, canny producers, and all the other folks of the good old Seventh Art. To do that, we needed SQLAlchemy -- *talk pythonic to db*, remember? 
So I created a data model in SQLAlchemy [autoloading the tables](https://docs.sqlalchemy.org/en/20/core/reflection.html) I previously created with Alembic (by the way, SQLAlchemy and Alembic have a relationship
of the *bread-and-butterly* sort). The secret to tables autoloading is a concept called **reflection**, that is just a word to
say *look in the database, and make python classes out of what you see there*. All that information (primay keys, foreing keys, etc..) is put inside the Metadata, a sort of infobox with everything needed to create the Tables objects in python.  

When creating a table, SQLAlchemy automatically generates new tables out of foreign keys, if there is any. 

This is the code to generate the data model (the set of `Tables` objects we'll use to interact with the movie db)

```py

from sqlalchemy import MetaData, Table
from repository.engine import engine

# Initialize metadata
metadata_obj = MetaData()

# Reflect all table at once in the metadata ("See what's in the provided engine")
metadata_obj.reflect(bind=engine)

# Extract all the table names from the metadata
table_names = metadata_obj.tables.keys()

# Create a dictionary with all the `Table` objects to interact with the database
tables = {table_name: Table(table_name, metadata_obj, autoload_with=engine) for table_name in table_names}

```

I created a `get_table_info` function to print out some pretty table information. 
Everything went Oll Korrect ✅

```
╒══════════════╤═════════════════════════════════════════════════════╕
│ Table        │ movies                                              │
├──────────────┼─────────────────────────────────────────────────────┤
│ Columns      │ NAME            TYPE            NULLABLE    DEFAULT │
│              │ movie_id        INTEGER         False               │
│              │ title           VARCHAR(255)    False               │
│              │ original_title  VARCHAR(255)    True                │
│              │ tagline         VARCHAR(255)    True                │
│              │ plot            TEXT            True                │
│              │ language        VARCHAR(50)     True                │
│              │ country         VARCHAR(50)     True                │
│              │ release_date    DATE            True                │
│              │ runtime         INTEGER         True                │
│              │ budget          NUMERIC(15, 2)  True                │
│              │ box_office      NUMERIC(15, 2)  True                │
│              │ rating          NUMERIC(3, 1)   True                │
│              │ rating_count    INTEGER         True                │
│              │ director_id     INTEGER         True                │
│              │ writer_id       INTEGER         True                │
│              │ studio_id       INTEGER         True                │
│              │ distributor_id  INTEGER         True                │
│              │ poster_url      VARCHAR(255)    True                │
│              │ trailer_url     VARCHAR(255)    True                │
│              │ age_rating      VARCHAR(10)     True                │
│              │ imdb_id         VARCHAR(50)     True                │
│              │ tmdb_id         VARCHAR(50)     True                │
│              │ homepage        VARCHAR(255)    True                │
│              │ created_at      TIMESTAMP       False               │
│              │ updated_at      TIMESTAMP       False               │
├──────────────┼─────────────────────────────────────────────────────┤
│ Primary Key  │ movie_id                                            │
├──────────────┼─────────────────────────────────────────────────────┤
│ Foreign Keys │ distributors.distributor_id                         │
│              │ studios.studio_id                                   │
│              │ writers.writer_id                                   │
│              │ directors.director_id                               │
├──────────────┼─────────────────────────────────────────────────────┤
│ Constraints  │ movies_director_id_fkey                             │
│              │ movies_writer_id_fkey                               │
│              │ movies_pkey                                         │
│              │ movies_studio_id_fkey                               │
│              │ movies_distributor_id_fkey                          │
╘══════════════╧═════════════════════════════════════════════════════╛
```

#### Test the repository

<!-- Some tests on the database:  -->

*Useful resources*: 
* [A guide to database unit testing](https://coderpad.io/blog/development/a-guide-to-database-unit-testing-with-pytest-and-sqlalchemy/)



#### Connect the crawling module to the movie db client

Connection between the crawling module and the movie db client happened through the creation of a shared docker volume, through which containers got access the same piece of data, an `item-list.json` file. That file was written by the crawling service as an output of its scraping, and consumed by the client service as an input for populating the database; 


2. A precise chronological orchestration of containers. I did this by setting the `compose.yml` file so that the movie db client service depended on the crawling service having initialized. This way the client had visibility on the last freshly scraped version of the item list, and could process it in bulk to populate the database. 

This whole process in synchronous, defusing some of the advantages of docker -- that is, indipendent containers that can operate in autonomy through asynchronous communication. I opted for this choice for the following reasons:
1. This whole process has a lower network latency, as the d 


### Overview of the Services

#### Initialize the database
Service name: `movie_db`
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
 
Spiders are communicating through a shared docker volume containing the list of movies. This list is created by the movie-list spider
and consumed by the movie spider to create the items. Items are than converted into a standardized json object, which can be easily 
imported by the movie db client as a python dictionary to insert the each item in the database -- after checking that the item has not been previously uploaded to the db. 


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

<!-- ### Combining the services -->

<!-- The docker `compose.yml` file to run our multi-container application is the following:
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

``` -->



