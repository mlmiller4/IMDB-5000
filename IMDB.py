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

def top10(top10df, colNames, aggColumn, aggFunction):
    """
    Returns data frame with the top 10 values of the specified column named aggregated and ranked

    :param top10df: Input dataframe
    :param colNames: Names of columns to be used to group the input dataframe
    :param aggColumn: The name of the column which will be used for aggregation
    :param aggFunction: The function which will be used for aggregation (e.g. 'sum', 'mean', etc.)
    :return: dataframe with top 10 rows of the grouped input dataframe
    """

    # Notify user of any improper paramters
    if not isinstance(top10df, pd.DataFrame):
        print('\nInput does not contains a dataframe')
        return None
    if aggColumn not in top10df.columns:
        print('\nAggregating column not found in dataframe')
        return None
    if aggFunction not in ['sum','mean','min','max']:
        print('\nUnknown aggregating function specified')
        return None

    # Group the input data frame by the column names and aggregate by the specified aggColumn and aggFunction
    grouped = top10df.groupby(colNames).agg({aggColumn: [aggFunction]})

    # Name aggregated column '<aggColumn>_<aggFunction>' and reset index
    grouped.columns = [aggFunction + '_' + aggColumn]
    grouped = grouped.reset_index()

    # Sort in descending order by the '<aggFunction>_<aggColumn> column
    grouped.sort_values(by=[aggFunction + '_' + aggColumn], ascending=False, inplace=True)

    # return top 10 rows
    return grouped[:10]


def printResultsDF(resultsDF):
    """
    Prints results contained in dataframe, formats values to monetary standard if needed.

    :param resultsDF:
    :return: nothing
    """

    if ('mean_imdb_score' in resultsDF.columns):        # Actor/Director with highest IMDB score
        for index, row in resultsDF.iterrows():
            print(row['director_name'] + ' & ' + row['actor_1_name'] + ' : ' + str(row['mean_imdb_score']))

    elif ('actor_1_name' in resultsDF.columns and 'director_name' in resultsDF.columns and 'mean_imdb_score' not in resultsDF.columns):  # actor/director pairs
        for index, row in resultsDF.iterrows():
            print(row['director_name'] + ' & ' + row['actor_1_name'] + ' : $' + '{:,}'.format(int(row['sum_profit'])))

    elif ('director_name' in resultsDF.columns and 'actor_1_name' not in resultsDF.columns):    # director only
        for index, row in resultsDF.iterrows():
            print(row['director_name'] + ' : $' + '{:,}'.format(int(row['sum_profit'])))

    elif ('actor_1_name' in resultsDF.columns and 'director_name' not in resultsDF.columns):    # actor only
        for index, row in resultsDF.iterrows():
            print(row['actor_1_name'] + ' : $' + '{:,}'.format(int(row['sum_profit'])))

    elif ('genre' in resultsDF.columns):            # genre
        for index, row in resultsDF.iterrows():
            print(row['genre'] + ' : $' + '{:,}'.format(int(row['total_profit'])))


""" Calculate profit by 'gross' - 'budget' and profit margin by ('gross' - 'budget')/'budget'   """
def calculateProfit(profitDF):
    profitDF['profit'] = profitDF['gross'] - profitDF['budget']
    #profitDF['profit_margin'] = (profitDF['profit'] / profitDF['budget']) * 100
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
    actorsDF = get_columns(df, ['actor_1_name','profit'])
    top10actors = top10(actorsDF, 'actor_1_name', 'profit', 'sum')
    print("Top 10 actors with highest profitability:")
    printResultsDF(top10actors)

    ''' Top 10 directors'''
    print("")
    directorsDF = get_columns(df, ['director_name','profit'])
    top10directors = top10(directorsDF, 'director_name', 'profit', 'sum')
    print("Top 10 directors with highest profitability:")
    printResultsDF(top10directors)

    ''' Top 10 profitable director/actor pairs'''
    print("")
    profitablePairsDF = get_columns(df, ['actor_1_name','director_name','profit'])
    top10pairs = top10(profitablePairsDF, ['director_name','actor_1_name'], 'profit', 'sum')
    print("Top 10 director/actor pairs with highest profitability:")
    printResultsDF(top10pairs)

    ''' Top 10 director/actor pairs with highest IMDB score'''
    print("")
    pairsIMDBscoreDF = get_columns(df, ['actor_1_name', 'director_name', 'imdb_score'])
    top10pairsIMDB = top10(pairsIMDBscoreDF, ['actor_1_name', 'director_name'], 'imdb_score', 'mean')
    print("Top 10 director/actor pairs with highest IMDB score:")
    printResultsDF(top10pairsIMDB)



    

