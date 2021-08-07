"""
Analysis related classes and methods
"""
import math
import isodate
import pandas as pd

class Analyze:
    def __init__(self):
        pass

    def likes_to_dislikes(self, likes, dislikes, multiplier=1000):
        """Likes to dislikes ratio for a video

        Args:
            likes (int): Likes
            dislikes (int): Dislikes
            multiplier (int): Multiplier
        """
        if(isinstance(likes, str) or isinstance(dislikes, str)):
            try:
                likes = int(likes)
                dislikes = int(likes)
            except Exception as e:
                print(e)
                return(False)
        if(dislikes == 0):
            dislikes = 1
        return(likes/dislikes * multiplier)
    
    def dislikes_to_likes(self, dislikes, likes, multiplier=1000):
        """Dislikes to likes ratio for a video

        Args:
            dislikes (int): Dislikes
            likes (int): Likes
            multiplier (int): Multiplier
        """
        if(isinstance(likes, str) or isinstance(dislikes, str)):
            try:
                likes = int(likes)
                dislikes = int(likes)
            except Exception as e:
                print(e)
                return(False)
        if(likes == 0):
            likes = 1
        return(dislikes/likes * multiplier)
    
    def get_duration_in_seconds(self, duration_in_ISO_8601):
        """Returns duration in seconds

        Args:
            duration_in_ISO_8601 (str): Duration in ISO 8601
        """
        return(int(isodate.parse_duration(duration_in_ISO_8601).total_seconds()))

    def engagement_score(self, likes, dislikes, comment_count, view_count):
        """A score to understand how much the audience engaged with a video. The more likes or dislikes, the higher is the engagement.

        Args:
            likes (float): Likes
            dislikes (float): Dislikes
            view_count (float): Number of views
        """
        metric = (likes + dislikes + comment_count)/view_count * 1000
        return(metric)
    
    def splice_by_labels(self, df, list_category, list_theme, *functions):
        """Returns tables per category and theme

        Args:
            df (pandas.DataFrame): Pandas DataFrame
            list_categories (list): categories
            list_themes (list): themes
        """
        list_df_category = []
        for category in list_category:
            df_temp = df[df["category"].str.contains(category, na=False)].copy()
            for function in functions:
                name = function.__name__
                df_temp.loc[:, name] = df_temp.apply(function)
            list_df_category.append(df_temp)
        list_df_theme = []
        for theme in list_theme:
            df_temp = df[df["theme"].str.contains(theme, na=False)].copy()
            for function in functions:
                name = function.__name__
                df_temp.loc[:, name] = df_temp.apply(function)
            list_df_theme.append(df_temp)
        return([list_df_category, list_df_theme])

    def describe_df(self, list_df, label_name, list_label, column, is_count=True, is_mean=True, is_std=True, is_median=True):
        """Descriptive statistics of the given dataframe

        Args:
            list_df (list(pandas.DataFrame)): list of dataframes
            list_label (list): list of labels
        """
        list_list_rows = []
        list_columns = [label_name]
        if(is_count):
            list_columns.append("count")
        if(is_mean):
            list_columns.append("mean")
        if(is_std):
            list_columns.append("std")
        if(is_median):
            list_columns.append("median")
        for index, label in enumerate(list_label):
            row_name = label
            list_row = [row_name]
            if(is_count):
                count = list_df[index][column].count()
                list_row.append(count)
            if(is_mean):
                mean = list_df[index][column].mean()
                list_row.append(mean)
            if(is_std):
                std = list_df[index][column].std()
                list_row.append(std)
            if(is_median):
                median = list_df[index][column].median()
                list_row.append(median)
            list_list_rows.append(list_row)
        df = pd.DataFrame(list_list_rows, columns=list_columns)
        return(df)

if(__name__ == "__main__"):
    print(Analyze().get_duration_in_seconds("PT12M41S"))
