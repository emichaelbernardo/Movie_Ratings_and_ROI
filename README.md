------------------------------
# How Profitable are Good Movies?
-----------------------------

## Introduction:

In 1960, there were over 2,500 movies released in theaters<sup>1</sup>, mostly to screens in the United States. Reviews came mostly from local newspapers, and promotional budgets were almost negligible costs. By the turn of the century this number ballooned to close to 8000 movies a year <sup>2</sup> grossing more than 10.5 Billion US dollars, however, the cost of making movies skyrocketed as well.<sup>3</sup>. 

Gauging the quality of a movie is highly subjective, and with a plethora of online review sites available, reviews now can come from practically anyone and anywhere there is an internet enabled device. I intend to tap into some of this data and use statistical analysis to determine the likelihood of a "Good" movie being "Profitable".<sup>4</sup>

## The Data:

To do this, I have built a new database that combines information from IMDB, TMDB, Rotten Tomatoes, Movie Lens, Box Office Mojo  and the Academy Awards website. 

![The Data](images/thedata.png)

------------------------
## Defining Good
------------------------

Before I can begin any analysis of the data, I have to define some terms.
<br>
A 'good' movie should have: <br>
### An audience or user score/rating of 7.5 or higher. 
![Good Movies](images/Quality_user_score.png)

### A Critics score/rating of 7.5 or higher. 
![Good Movies 2](images/Quality_critic_score.png)

### An oscar win or nomination 
![Awarded Movies](images/nods.png)

A 'Profitable' movie should have: <br>
### A positive net profit and an ROI of 300% or more

![profitable Movies](images/agg_financials.png)

--------------------------


------------------------
## Analysis
------------------------


------------------------
## Setting up Data for Bayesian Test
------------------------


------------------------
## Bayesian Test Results
------------------------


------------------------
## More Observations
------------------------

------------------------
## Further Studies
------------------------

citations:<br>
<sup>1</sup> [imdb.com](https://www.imdb.com/search/title/?year=1960&title_type=feature&) <br>
<sup>2</sup> [imdb.com](https://www.imdb.com/search/title/?year=2010&title_type=feature&) <br>
<sup>3</sup> [natoonline.org](https://www.natoonline.org/data/boxoffice/ )<br>
<sup>4</sup> [Hyunjin-Jo on Quora](https://www.quora.com/How-much-should-a-big-budget-movie-make-at-the-box-office-relative-to-its-production-cost-to-be-considered-to-be-a-likely-financial-success/answer/Hyunjin-Jo)


script outline:
 - intro
 - define good + plot
 - user scores + plot
 - critic scores + plot
 - oscars + plot (probability that you have an oscar if you have high score?)
 - define success + plot (budget vs revenue top 10?)
 - hypothesis test 1
 - revenue over decades
 - further studies
     - inflation adjustment in numbers
     - more data



