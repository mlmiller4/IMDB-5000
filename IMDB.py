import pandas as pd
import numpy as np
import itertools
pd.set_option('display.max_columns',50)

def top_10_genres(genreDF):

    """
    Parse the genres column to create a column for each genre with a 1 or 0 indicating whether
    the movie is in that genre.  So, if the 'genres' column for a movie lists "Action|Adventure|Fantasy"
    then separate columns labelled 'Action', 'Adventure', and 'Fantasy' will have values of 1 and all other
    genres will have values of 0.
    """

    # First, create a list of all genres listed in the 'genres' column by splitting 'genres' by '|' and adding
    # each individual genre to genreList, excluding any that are already in genreList to avoid duplicates
    unparsedGenreList = genreDF['genres'].unique()
    genreList = []

    for genres in unparsedGenreList:
        individualGenres = genres.split('|')    # split on '|'

        for i in range(len(individualGenres)):          # add each genre to genreList if not already there
            if individualGenres[i] not in genreList:
                genreList.append(individualGenres[i])

    genreList.sort()

    # Create new columns labelled with each genre and a default value of 0
    genreDF = genreDF.assign(**dict.fromkeys(genreList, 0))

    # Cycle through genreDF, get values in 'genres' column and place a 1 or 0 in individual genre column depending
    # on whether the movie lists that genre in 'genres'
    for index, row in genreDF.iterrows():
        genres = row["genres"].split('|')

        for i in range(len(genreList)):

            if genreList[i] in genres:
                genreDF.at[index, genreList[i]] = 1
            else:
                genreDF.at[index, genreList[i]] = 0

    # Create dictionaries for profit and profit margin, then calculate the total profit by genre, with genre/profit
    # being key/value pairs
    profitDict = {}
    #profitMarginDict = {}

    for i in range(len(genreList)):
        grouped = genreDF.groupby(genreList[i])
        profit = grouped['profit'].agg(np.sum)
        #profitMargin = grouped['profit_margin'].agg(np.mean)

        profitDict[genreList[i]] = profit.loc[1]
        #profitMarginDict[genreList[i]] = profitMargin.loc[1]

    # Sort genres by profitability in descending order
    sortedProfit = sorted(profitDict.items(), key=lambda x: x[1], reverse=True)

    profitDF = pd.DataFrame.from_dict(sortedProfit)
    profitDF.columns = ['genre', 'total_profit']
    return profitDF[:10]



''' Returns data frame with the top 10 most profitable actors'''
def top_10_actors(actorDF):

    # Group by 'actor_1_name' column, aggregate 'profit' column, sort descending, and return first 10 rows
    grouped = actorDF.groupby(['actor_1_name']).agg({'profit': ['sum']})
    grouped.columns = ['total_profit']
    grouped = grouped.reset_index()
    grouped.sort_values(by=['total_profit'], ascending=False, inplace=True)

    return grouped[:10]

''' Returns data frame with the top 10 most profitable directors'''
def top_10_directors(directorDF):

    # Group by 'director_name' column, aggregate 'profit' column, sort descending, and return first 10 rows
    grouped = directorDF.groupby(['director_name']).agg({'profit': ['sum']})
    grouped.columns = ['total_profit']
    grouped = grouped.reset_index()
    grouped.sort_values(by=['total_profit'], ascending=False, inplace=True)

    return grouped[:10]

''' Returns data frame with the top 10 most profitable actor/director pairs'''
def top_10_pairs(pairDF):

    # Group by 'director_name' & 'actor_1_name', aggregate 'profit' column, sort descending, and return first 10 rows
    grouped = pairDF.groupby(['director_name', 'actor_1_name']).agg({'profit': ['sum']})
    grouped.columns = ['total_profit']
    grouped = grouped.reset_index()
    grouped.sort_values(by=['total_profit'], ascending=False, inplace=True)

    return grouped[:10]

def top_10_IMDB_pairs(pairDF):

    # Group by 'director_name' & 'actor_1_name', aggregate 'profit' column, sort descending, and return first 10 rows
    grouped = pairDF.groupby(['director_name', 'actor_1_name']).agg({'imdb_score': ['mean']})
    #grouped = grouped.groupby('actor_3_name').agg({'imdb_score': ['mean']})

    grouped.columns = ['mean_IMDB_score']
    grouped = grouped.reset_index()
    grouped.sort_values(by=['mean_IMDB_score'], ascending=False, inplace=True)

    return grouped[:10]


''' Prints results contained in a DataFrame, formats values to monetary standard '''
def printResultsDF(resultsDF):

    if ('mean_IMDB_score' in resultsDF.columns):        # Actor/Director with highest IMDB score
        for index, row in resultsDF.iterrows():
            print(row['director_name'] + ' & ' + row['actor_1_name'] + ' : ' + str(row['mean_IMDB_score']))

    elif ('actor_1_name' in resultsDF.columns and 'director_name' in resultsDF.columns and 'mean_IMDB_score' not in resultsDF.columns):  # actor/director pairs
        for index, row in resultsDF.iterrows():
            print(row['director_name'] + ' & ' + row['actor_1_name'] + ' : $' + '{:,}'.format(int(row['total_profit'])))

    elif ('director_name' in resultsDF.columns and 'actor_1_name' not in resultsDF.columns):    # director only
        for index, row in resultsDF.iterrows():
            print(row['director_name'] + ' : $' + '{:,}'.format(int(row['total_profit'])))

    elif ('actor_1_name' in resultsDF.columns and 'director_name' not in resultsDF.columns):    # actor only
        for index, row in resultsDF.iterrows():
            print(row['actor_1_name'] + ' : $' + '{:,}'.format(int(row['total_profit'])))

    elif ('genre' in resultsDF.columns):            # genre
        for index, row in resultsDF.iterrows():
            print(row['genre'] + ' : $' + '{:,}'.format(int(row['total_profit'])))


''' No longer needed '''
# ''' Prints results in List form, formats values to monetary standard '''
# def printResults(results):
#     for i in range(len(results)):
#         g = results[i][0]
#         p = int(results[i][1])
#         print(g + " : $" + '{:,}'.format(p))
''' ---------------------------------------------------------------------------'''

""" Calculate profit by 'gross' - 'budget' and profit margin by ('gross' - 'budget')/'budget'   """
def calculateProfit(profitDF):
    profitDF['profit'] = profitDF['gross'] - profitDF['budget']
    profitDF['profit_margin'] = (profitDF['profit'] / profitDF['budget']) * 100
    return profitDF

''' Get specified columns from the dataset'''
def get_columns(getColumnsDF, cols):
    return pd.DataFrame(getColumnsDF, columns=cols)



if __name__ == "__main__":

    df = pd.read_csv("movie_metadata.csv")
    df = calculateProfit(df)

    ''' Top 10 genres'''
    print("")
    top10genres = top_10_genres(get_columns(df, ['genres','profit','profit_margin']))
    print("Top 10 genres with highest profitability:")
    printResultsDF(top10genres)

    ''' Top 10 actors'''
    print("")
    top10actors = top_10_actors(get_columns(df, ['actor_1_name','profit','profit_margin']))
    print("Top 10 actors with highest profitability:")
    printResultsDF(top10actors)

    ''' Top 10 directors'''
    print("")
    top10directors = top_10_directors(get_columns(df, ['director_name','profit','profit_margin']))
    print("Top 10 directors with highest profitability:")
    printResultsDF(top10directors)

    ''' Top 10 profitable director/actor pairs'''
    print("")
    top10pairs = top_10_pairs(get_columns(df, ['actor_1_name','director_name','profit','profit_margin']))
    print("Top 10 director/actor pairs with highest profitability:")
    printResultsDF(top10pairs)

    ''' Top 10 director/actor pairs with highest IMDB ratings'''
    print("")
    top10pairsIMDB = top_10_IMDB_pairs(get_columns(df, ['actor_1_name','director_name','imdb_score']))
    print("Top 10 director/actor pairs with highest IMDB score:")
    printResultsDF(top10pairsIMDB)




    

