import pandas as pd
import sys


def display(df):
    """Displays relevant tables

    Args:
        df (pandas.DataFrame): Pandas DataFrame
    """
    list_categories = ["Protective", "Risky", "Neutral", "Potential misinformed claims"]
    list_themes = [
        "Vaping tricks", 
        "Marketing", 
        "Harmful health consequences", 
        "Promotion/Celebration", 
        "Comparative health effects with smoking", 
        "News report", 
        "N.A."
    ]
    list_rows_category = []
    for category in list_categories:
        df_temp = df[df["category"].str.contains(category, na=False)]
        count = len(df_temp.index)
        list_rows_category.append([category, count])
    list_rows_theme = []
    for theme in list_themes:
        df_temp = df[df["theme"].str.contains(theme, na=False)]
        count = len(df_temp.index)
        list_rows_theme.append([theme, count])
    df_category = pd.DataFrame(list_rows_category, columns=["category", "count"])
    df_category = df_category.append({
        "category": "Total",
        "count": df_category["count"].sum()
    },
    ignore_index=True
    )
    df_theme = pd.DataFrame(list_rows_theme, columns=["theme", "count"])
    df_theme = df_theme.append({
        "theme": "Total",
        "count": df_theme["count"].sum()
    },
    ignore_index=True
    )
    print(f"Number of tagged videos: {len(df[df['category'].notnull()].index)}/{len(df.index)}")
    print(df_category)
    print(df_theme)
    return

if(__name__ == "__main__"):
    filepath = sys.argv[1]
    df = pd.read_csv(filepath, index_col=False)
    display(df)