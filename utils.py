# load utils.py
import os
import sys
#sys.path.append(os.path.abspath("capstone1/utils.py"))


#standard imports
import pandas as pd
import numpy as np
import seaborn as sns
import contextlib
import pandas.io.formats.format as pf
import matplotlib.pyplot as plt

#to be able to count within columns
from collections import Counter

# to be able to count genres since movies may fall under several genres
from sklearn.feature_extraction.text import CountVectorizer


bayes_df = pd.read_csv('data/bayes_df.csv')
# -----------------------------#


# This plots a histogram of movies by Decade
def plot_decade(df,group,measure):
    sns.set(font_scale=2.1)
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

    
## function to test if import is working    
def testing():
    return 'test good'