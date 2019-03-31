# The Bechdel Test & Women in Film
### Capstone Project for Flatiron Data Science Program

## Motivation
The Bechdel Test is a scoring system used to measure how a film and other forms of media represent women. The Bechdel Test [website](https://bechdeltest.com/) contains over 8,000 user-submitted films and their scoring on the test. Users can also challenge a film's score if they believe it was rated incorrectly. Three points are required to pass the test. Points are awarded as follows:
* 1 point for two named female characters 
* 2 points for two named female characters who talk to each other
* 3 points for two named female characters who talk to each other about something other than a man

At first glance, this test may seem easy to pass, but a surprising number of popular and award-winning films do not pass the test - even films with strong female leads. The **Edge of Tomorrow** starring Emily Blunt as a badass, alien-slaughtering warrior, for example, scores one sad point on the test because there is only one other named female character in the movie, and she never speaks to Blunt's character. 

![Emily Blunt and Tom Cruise in a promotional photo for movie Edge of Tomorrow](/images/livedierepeat.jpg)

In comparison, the recently-released **Captain Marvel** starring Brie Larson as a badass, alien-slaughtering ~~warrior~~ noble warrior hero passes the Bechdel Test with flying colors. Besides the obvious fact that **Captain Marvel** had multiple female characters who spoke to each other about something other than a man, I wondered - did these films have other differences? Could a film have certain attributes that make it more likely to pass the Bechdel Test than others? 

![Samuel L. Jackson, Brie Larson, and Jude Law in a promotional photo for Captain Marvel](/images/captainmarvel.jpg)

Note: The Bechdel Test is not meant to identify feminist or even "progressive" films, whatever that may mean. It is simply one of many ways to examine how women are represented in film, and for now, there is more crowdsourced data on films that pass or fail this test than others. **American Pie 2** passed the test because two named female characters talk about clothes with each other. The movie directed by the **first and only female to ever win an Oscar for Best Director** (Kathryn Bigelow for The Hurt Locker) fails the test with zero points because there is only one named female character in the movie - the wife of a soldier. The test is not perfect, nor is it meant to be, but we've got to start somewhere.  

## Methodology
The first data I gathered was from the Bechdel Test website, which I scraped using the Beautiful Soup library for Python and loaded into a Pandas dataframe. Before I scraped the webite, I reviewed their `robots.txt` to see the site's hard limits on bots and scraping. To avoid overloading the site with requests and/or getting banned, I used `sleep` at random intervals for my requests. I grabbed the year, title, score, passing status, imdb id, and imdb link for every entry on the site.

![First five rows of dataframe built with data scraped from Bechdel Test website](/images/bechdel_df_head.jpg)

I downloaded and inspected numerous movie datasets from [data.world](https://data.world/) and [Kaggle](https://www.kaggle.com/datasets) to supplement my data, but I soon encountered a problem which I had never before faced: bad data. As a student, we were often supplied with datasets that required cleaning - whether it be null values or extreme outliers that were obviously the result of a data entry typo with too many zeros. But what should one do when the data they have is just plain *wrong*? 

![Dataframe containing director name, top three actor names, movie title, movie genre, budget, and gross](/images/bad_bond_data.png)

The above movie dataset included the top three actors for each movie. Luckily for me, I happen to love James Bond movies, so I was able to catch that the James Bond movie entry of **Spectre** did not include *the actor who plays James Bond*, Daniel Craig. Immediately burned, I felt that I could not trust this dataset of 5000+ movies, so I set out to collect my own data which I could be sure was trustworthy - or at least more trustworthy than a dataset that doesn't include James Bond as a top actor in a James Bond film. 

I eventually decided that I absolutely needed the data contained in the Wikipedia infoboxes. 
