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
### Data Collection & Cleaning
The first data I gathered was from the Bechdel Test website, which I scraped using the Beautiful Soup library for Python and loaded into a Pandas dataframe. Before I scraped the webite, I reviewed their `robots.txt` to see the site's hard limits on bots and scraping. To avoid overloading the site with requests and/or getting banned, I used `sleep` at random intervals for my requests. I grabbed the year, title, score, passing status, imdb id, and imdb link for every entry on the site.

![First five rows of dataframe built with data scraped from Bechdel Test website](/images/bechdel_df_head.jpg)

I downloaded and inspected numerous movie datasets from [data.world](https://data.world/) and [Kaggle](https://www.kaggle.com/datasets) to supplement my data, but I soon encountered a problem which I had never before faced: bad data. As a student, we were often supplied with datasets that required cleaning - whether it be null values or extreme outliers that were obviously the result of a data entry typo with too many zeros. But what should one do when the data they have is just plain *wrong*? 

![Dataframe containing director name, top three actor names, movie title, movie genre, budget, and gross](/images/bad_bond_data.png)

The above movie dataset included the top three actors for each movie. Luckily for me, I happen to love James Bond movies, so I was able to catch that the James Bond movie entry of **Spectre** did not include *the actor who plays James Bond*, Daniel Craig. Immediately burned, I felt that I could not trust this dataset of 5000+ movies, so I set out to collect my own data which I could be sure was trustworthy - or at least more trustworthy than a dataset that doesn't include James Bond as a top actor in a James Bond film. 

The other primary sources of data that I used to supplement my original dataset included:
* Wikidata SPARQL queries
* The Movie Database (TMDb) API

### Film Features
The other data I collected consisted of:
* film budget
* revenue / box office
* whether there was a director of an underrepresented gender (cisgender and transgender females, transgender males, or non-binary)
* screenwriter of an underrepresented gender
* producer of an underrepresented gender

### Exploratory Data Analysis
* Distribution of movies in the dataset
  * Passing & Non-Passing Movies 
  * Movies with a director of an underrepresented gender
  * Movies with a writer of an underrepresented gender
  * Movies with a producer of an underrepresented gender
  * Mean and Median budgets of passing vs. non-passing movies
  * Mean and Median revenues of passing vs. non-passing movies
  
![Bar graph showing the difference between films that pass and fail the Bechdel Test and presence of crew members of an underrepresented gender](/images/crew_gender.png)

The above plot shows the total number of films in the dataset. A film received one point for each role of director, writer, and producer if there was at least one person in that role of an underrepresented gender. The `overall` column is the sum of all those points - the maximum being 3 points per movie. The plot shows that films which received points for a director, writer, and/or producer were more likely to also be films that passed the Test.

![Bar graph showing the mean and median budgets for films that pass the test vs. films that do not pass the test](/images/budgets.png)

![Bar graph showing the mean and median revenues for films that pass the test vs. films that do not pass the test](/images/revenues.png)

The above plots show that there is a greater difference in budgets for films that pass the Test vs. films that do not pass the Test than there is a difference in revenues. To see if these differences were statistically significant, I ran two different hypothesis tests.

## Findings

### Hypothesis Testing

![Null and alternative hypotheses for statistically significant differences in budgets of films that pass the test vs. films that do not pass the test](/images/hypothesis1.png)

![p-value showing that the null for hypothesis 1 can be rejected](/images/hypothesisresult1.png)

With a small p-value of 0.001, the null hypothesis that there is no statistically significant difference between the mean budgets of films that pass the test vs. films that do not pass the test can be rejected.

![Null and alternative hypotheses for statistically significant differences in revenues of films that pass the test vs. films that do not pass the test](/images/hypothesis2.png)

![p-value showing that the null for hypothesis 2 cannot be rejected](/images/hypothesisresult2.png)

With a large p-value of 0.7, the null hypothesis that there is no statistically significant difference between the mean revenues of films that pass the test vs. films that do not pass the test cannot be rejected.

### Conditional Probability with Bayes Theorem
  
Based on visualizations that show films with members on the production team of an underrepresented gender are more likely to also be a film that passes the Bechdel Test, I calculated these probabilities using Bayes Theorem.

P(A|B) = P(A) * P(B|A) / P(B)

P(A) = Probability of a film passing the Bechdel Test for this dataset = 0.57 </br>
P(B) = Probability of a film having a director of an underrepresented gender = 0.1 </br>
P(C) = Probability of a film having a writer of an underrepresented gender = 0.16 </br>
P(D) = Probability of a film having a producer of an underrepresented gender = 0.17 </br>

##### Likelihood

P(B|A) = probability of director of underrepresented gender, given a passing test = 0.14 </br>
P(C|A) = probability of writer of underrepresented gender, given a passing test = 0.22 </br>
P(D|A) = probability of producer of underrepresented gender, given a passing test = 0.19 </br>

#### Final Results

P(A|B) = probability of passing test, given director of underrepresented gender = 0.8 </br> 
P(A|C) = probability of passing test, given writer of underrepresented gender = 0.78 </br>
P(A|D) = probability of passing test, given producer of underrepresented gender = 0.64 </br>

## Conclusions

While the Bechdel Test is not perfect, it does serve as a way to gauge how women are represented onscreen, and a film that passes the test often has one or a combination of the following qualities:
* director of an underrepresented gender
* writer of an underrepresented gender
* producer of an underrepresented gender
* lower average budget than films that do not pass the test
* average revenue that is slightly lower than films that do not pass the test, although not statistically significant

## Dashboard

Another goal of this project was to present data-driven insights for end-users with a dashboard, and also to allow users to explore the data that most interests them. One example of something a user can do with the dashboard is to select movies of their choosing to see crew genders and also to see if that movie passed the Bechdel Test.

![Screenshot of dashboard showing user selection of all Jurassic Park movies](/images/jurassic_park_movies.png)

The above screenshot shows a comparison of all the Jurassic Park and Jurassic World movies, and how a user can customize their search for their favorite movies (or for their favorite franchise, which happens to include their non-favorite films of Jurassic Park II and III).  

## Further Research & Recommendation

In addition to the Bechdel Test data, I'm also interested in adding more information to the dashboard about the Academy Awards and other awards for each year to see how the gender data has changed over time, salary information for actors vs. actresses, and more movie data - particularly around the most popular movies with the highest box office revenues and award recognitions.

### Other Tests for Scoring Movies
Although there is more crowdsourced data right now on the Bechdel Test, other tests have been proposed for scoring movies based on representation of different groups, including:
* The Rees Davies Test - scores a movie based on departments including two or more women
* The Waithe Test - a passing movie requires
  * a black woman in the film
  * who's in a position of power
  * and a healthy relationship
 
* The Villalobos Test - a passing movie requires
  * a Latina in a lead role
  * the leading character or other Latina character who is a professional or college educated, speaks in unaccented English,    and is not sexualized
  
* The Riz Test - a passing movie requires at least one Muslim character, but fails the test if that character
  * talks about, is a victim of, or a perpetrator of terrorism
  * is presented as irrationally angry
  * is presented as superstitious, culturally backwards, or anti-modern
  * is presented as a threat to a Western way of life
  * is presented as misogynistic, if male
  * is presented as oppressed, if female
  
## Other Resources 
Many organizations keep track of, report on, and promote diversity in the film industry, in addition to working on other important women's issues. Some of these organizations include
* Annenberg Inclusion Initiative - University of Southern California based think tank focused on diversity and inclusion in entertainment
* Women's Media Center - Nonpartisan and Non-profit organization founded by Jane Fonda, Robin Morgan and Gloria Steinem to raise awareness and take action on a wide range of issues affecting women and girls
* Geena Davis Institute on Gender & Media - "If she can see it, she can be it" - promotes increased visibility of women in media and in other roles, especially in roles where girls may not have seen much female representation
* Women in Media - Non-profit organization promoting gender balance in media by offering networking for female and female-identifying crew members
