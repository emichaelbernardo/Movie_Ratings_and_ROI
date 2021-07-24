# load utils.py
import os
import sys
#sys.path.append(os.path.abspath("capstone1/utils.py"))




#standard imports
import pandas as pd
import numpy as np
import seaborn as sns
import contextlib
from scipy import stats
import pandas.io.formats.format as pf
import matplotlib.pyplot as plt

#to be able to count within columns
from collections import Counter

# to be able to count genres since movies may fall under several genres
from sklearn.feature_extraction.text import CountVectorizer

#statistical libraries
from scipy.stats import shapiro


plt.style.use('ggplot')

# data prep ---------------
bayes_df = pd.read_csv('data/movie_aggregate.csv')


# Prep data for test - Using Critics_Choice 
df_good_c = bayes_df[bayes_df['Critics_Choice']==1] #Movies with Critics Score>= 7.5 
df_bad_c = bayes_df[bayes_df['Critics_Choice']==0]  #Movies with Critics Score < 7.5 

data1 = df_good_c.sample(n=300)['Profitable']
data2 = df_bad_c.sample(n=300)['Profitable']

# Prep data for test - Using Users_Pick
df_good_u = bayes_df[bayes_df['Users_Pick']==1] # Movies with User Score>= 7.5 
df_bad_u = bayes_df[bayes_df['Users_Pick']==0]  # Movies with User Score < 7.5 

data3 = df_good_u.sample(n=300)['Profitable']
data4 = df_bad_u.sample(n=300)['Profitable']




# -----------------------------#

# This returns a numbered list of columns of a dataframe
def get_col_indexes(df):
    lst = list(df.columns)
    for i,v in enumerate(lst):
        print(i,v)


# This plots a histogram of movies by Decade
def plot_decade(df,group,measure):
    sns.set(font_scale=1.1)
    g = sns.FacetGrid(df, col=group, height=4,col_wrap=3)
    g = (g.map(plt.hist, measure,bins=np.arange(2,9,0.5)))



# This returns the a dataframe based on csv or tsv. Assign function to new DF name
def read_data(path, filename, sep='None', header=0):
    fullpath = path+filename
    temp_df = pd.read_csv(fullpath, sep=sep, header=header, low_memory=False)
    return temp_df


# This returns genres from a dataframe as an array
def get_genres(temp_df):
    vec = CountVectorizer(token_pattern='(?u)\\b[\\w-]+\\b', analyzer='word').fit(temp_df)
    genre_pile = vec.transform(temp_df)
    unique_genres =  vec.get_feature_names()
    # this is the master list of genres from IMDB
    imdb_genres = np.array(unique_genres)
    return imdb_genres

# This plots genres by count 
def plot_genres():
    df = bayes_df.Genres.copy()
    list_kind = df.str.split(",")
    a = []
    for each in list_kind:
        for i in each:
            a.append(i)
            
    c=[]
    for each in a:
        if each != "":
             c.append(each)        
            
    f= dict(Counter(c))
    
    df3 = pd.DataFrame(list(f.items()),columns = ["ratio","kind"])
    new_index =(df3.kind.sort_values(ascending=False)).index.values
    new = df3.reindex(new_index)
    
    
    
    plt.figure( figsize = (15,15))
    #sns.barplot(x="kind",y="ratio",data=new,palette = sns.cubehelix_palette(len(x)))
    sns.barplot(x="kind",y="ratio",data=new,palette = sns.cubehelix_palette(rot=-.4))
    sns.barplot(x="kind",y="ratio",data=new,palette = 'GnBu_r')
    
    
    
    
    plt.xticks(rotation = 90)
    plt.xlabel("Count",fontsize=15)
    plt.ylabel("Movie Genre",fontsize=15)
    plt.title("Movies per Genre",fontsize = 20)
    plt.savefig(r'images/movies_per_genre.png', bbox_inches = 'tight')
    

    
# Plot financials (Revenue, Budget and Profit)
def plotFinancials(df):
    sns.set_theme(style="white", context="talk")
    rs = np.random.RandomState(8)
    movies_agg = df[['Decade','Budget','Revenue','Profit']].groupby(['Decade']).agg(['sum'])
    
    # Set up the matplotlib figure
    f, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 5), sharex=True)
    
    # Budget
    x = list(movies_agg.index)
    y1 = list(movies_agg['Budget','sum'])
    sns.barplot(x=x, y=y1, palette="rocket", ax=ax1)
    ax1.axhline(0, color="k", clip_on=False)
    ax1.set_ylabel("Budget")
    
    # Revenue
    y2 = list(movies_agg['Revenue','sum'])
    sns.barplot(x=x, y=y2, palette="vlag", ax=ax2)
    ax2.axhline(0, color="k", clip_on=False)
    ax2.set_ylabel("Revenue")
    
    # Profit
    y3 = list(movies_agg['Profit','sum'])
    sns.barplot(x=x, y=y3, palette="deep", ax=ax3)
    ax3.axhline(0, color="k", clip_on=False)
    ax3.set_ylabel("Profit")
    
    f.suptitle('Movie Finacials by Decade\n', fontweight ="bold")
    
    # Finalize the plot
    sns.despine(bottom=True)
    plt.setp(f.axes, yticks=[])
    plt.tight_layout(h_pad=2)
    
    plt.savefig('images/agg_financials.png')
    

# Revenue over the decades
def plot_decade(df,group,measure):
    sns.set(font_scale=2.1)
    g = sns.FacetGrid(df, col=group, height=4,col_wrap=3)
    g = (g.map(plt.hist, measure,bins=np.arange(2,9,0.5)))
    

# Given the nature of the distribution, use the Mann Whitnet U test for hypothesis testing    
def MannWhitneyU(d1,d2):
    m_results = stats.mannwhitneyu(data1, data2, alternative = 'two-sided')
    print("Mann-Whitney U Test Results:")
    if m_results[1] > 0.05:
        print(f'p-value is {m_results[1]}, which is greater than 0.05, therefore we reject the null hypothesis')
    else:
        print(f'p-value is {m_results[1]}, which is less than 0.05, therefore we do not reject the null hypothesis ')
    #p-value>0.05 fail to reject null hypothesis

    
    


# This formats numbers to have commas for display 1000 becomes 1,000 etc
@contextlib.contextmanager
def custom_formatting():
    orig_float_format = pd.options.display.float_format
    orig_int_format = pf.IntArrayFormatter

    pd.options.display.float_format = '{:0,.2f}'.format
    class IntArrayFormatter(pf.GenericArrayFormatter):
        def _format_strings(self):
            formatter = self.formatter or '{:,d}'.format
            fmt_values = [formatter(x) for x in self.values]
            return fmt_values
    pf.IntArrayFormatter = IntArrayFormatter
    yield
    pd.options.display.float_format = orig_float_format
    pf.IntArrayFormatter = orig_int_format


df = pd.DataFrame(np.random.randint(10000, size=(5,3)), columns=list('ABC'))
df['D'] = np.random.random(df.shape[0])*10000

## example: with custom_formatting():
##                 print(bayes_adj)    

    
    
    
    
## Statistical Tests


def plot_beta(alpha, beta, ax=None, title="", xlabel="",ylabel="", label=""):
    '''plot the Beta distribution PDF with parameters alpha and beta
    Args
    ----
        alpha (positive number)
        beta (positive number)
    '''
    # Build a beta distribtuion scipy object.
    dist = stats.beta(alpha, beta)

    # The support (always this for the beta dist).
    x = np.linspace(0.0, 1.0, 301)

    # The probability density at each sample support value.
    y = dist.pdf(x)

    # Plot it all.
    if ax is None:
        fig, ax = plt.subplots()
    xticks=[0.0, 0.5, 1.0]
    lines = ax.plot(x, y, label=label)
    ax.fill_between(x, y, alpha=0.2, color=lines[0].get_c())
    if title: 
        ax.set_title(title)
    else:
        ax.set_title(f'Beta distribution alpha={alpha}, beta={beta} ')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.get_yaxis().set_ticks([])
    #ax.get_yaxis().set_ticks([np.max(y)])
    ax.get_xaxis().set_ticks(xticks)
    ax.set_ylim(0.0, min(np.max(y)*1.2,100))

def estimate_beta_params(data):
    """Estimate the alpha & beta parameters of beta distribution by fitting Beta distribution to the conversion data 
    Args
    ----
        data: a list of 0 (miss) or 1 (convert) or a 1-D np.array
    return
    ------
        Alpha: number of successes +1
        Beta: Number of failures +1
        Mean: "success" rate
        num_conversions & total_visitors: used to make labels on graphs 
    
    """
    #array of website conversions... zeros and ones (convert or didnt convert)
    website_samples = np.array(data)
    
    #total number of conversions
    num_conversions = website_samples.sum()
    #total number of datapoints
    total_visitors = len(website_samples)
    
    #plus one to set a and beta as uniform priors...try other numbers to see the changes
    alpha = num_conversions + 1
    beta = (total_visitors - num_conversions) + 1
    
    #mean number of conversions... aka conversion rate
    mean = 1 * num_conversions / total_visitors

    return alpha, beta, mean, num_conversions, total_visitors

def plot_beta_from_data(data, ax=None, label=None):
    """First estimate the Beta distribution parameters from data and then plot the Beta PDF distribution
    Args
    ----
        data: a list of 0 (miss) or 1 (convert)
    
    """
    alpha, beta, mean, num_conversions, total_visitors = estimate_beta_params(data)
    title =  r"Successful {}/{}".format(num_conversions, total_visitors)
    plot_beta(alpha, beta, ax=ax, title=title, xlabel="Success Rate", ylabel="Probability Density", label=label)

def MannWhitneyU(d1,d2):
    m_results = stats.mannwhitneyu(data1, data2, alternative = 'two-sided')
    print("Mann-Whitney U Test Results:")
    if m_results[1] > 0.05:
        print(f'p-value is {m_results[1]}, which is greater than 0.05, therefore we reject the null hypothesis')
    else:
        print(f'p-value is {m_results[1]}, which is less than 0.05, therefore we do not reject the null hypothesis ')
    #p-value>0.05 fail to reject null hypothesis


## function to test if import is working    
def testing():
    return 'test good'