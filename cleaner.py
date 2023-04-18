import pandas as pd
import numpy as np

bitval={'Documentary':0 ,  'Short':1 ,  'Animation':2, 'Comedy':3, 'Romance':4 ,'Sport':5, 'News':6,
 'Drama':7, 'Fantasy':8, 'Horror':9, 'Biography':10, 'Music':11, 'War':12, 'Crime':13, 'Western':14,
 'Family':15, 'Adventure':16, 'Action':17, 'History':18 ,'Mystery':19,  'Sci-Fi':20,
 'Musical':21, 'Thriller':22, 'Film-Noir':23, 'Talk-Show':24, 'Game-Show':25, 'Reality-TV':26,
 'Adult':27,'nan':28}


def genres_to_list(x):
    if x != None :
        result = 0

        for num in x:
            if num in bitval:
                # Use bitwise OR to set the corresponding bit to 1
                result |= 1 << bitval[num]

# Make sure the result is a 32-bit int
        result &= 0xFFFFFFFF

        return result
    else :
        result = 0
        result &= 0xFFFFFFFF
        return result

# def convert_to_int(x):
#     if x.isdigit():
#         return int(x)
#     else:
#         return 100000000
    
def convert_to_int(val):
    originalval=val
    # Check if the string contains only digits and at most one decimal point
    if val.isdigit() or (val.count('.') == 1 and val.replace('.', '').isdigit()):
        # Check if the string contains decimal digits
        if(originalval.count('.') == 1):
            return int(originalval.split(".")[0])
        else :
            return int(originalval)
    else:
        return None
    
def trunc(x):
    if x.dtype== "float":
        return int(x)
    else :
        return x
dtypes = {
    'tconst': 'str',
    'titleType': 'str',
    'primaryTitle': 'str',
    'originalTitle': 'str',
    'isAdult' : 'str',
    'startYear' : 'str',
    'endYear' : 'str',
    'runtimeMinutes' : 'str',
    'genres' : 'str'
    # and so on
}

# Read in the raw TSV file
df = pd.read_csv('data.tsv', sep='\t',na_values=['\\N'])
# df=df.fillna('NULL')


# float_cols = df.select_dtypes(include=['float'])
# float_cols = float_cols.replace([np.inf, -np.inf], -1)
# # df[float_cols.columns] = float_cols.astype(int)
# df[float_cols.columns] = float_cols.fillna(-1).astype(int)
# Remove leading/trailing whitespace from all columns
# df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df = df.rename(columns={'tconst': 'titleId','runtimeMinutes':'runtime'})
# TitleHasGenre = df.loc[:,['titleId','genres']]
# df=df.drop(['runtimeMinutes'],axis=1)
# print(df.loc[4178927,'runtimeMinutes'])

# print(df.loc[2306457,'runtimeMinutes'])
# print(df.loc[1097512,'runtimeMinutes'])
# print(df.loc[4178926,7])
# df.at[2306457,'runtimeMinutes']='1000.0'
# df.at[1097512,'runtimeMinutes']='1000.0'
# print(df.iloc[4178927,7])
# mask = df == 'Reality-TV'
# row_indices, col_indices = mask.index[mask.any(axis=1)].tolist(), mask.columns[mask.any(axis=0)].tolist()
# print(row_indices,col_indices)
# print(df['runtime'][1:100])
df['runtime']=df['runtime'].astype('str')
df['endYear']=df['endYear'].astype('float')
df['startYear']=df['startYear'].astype('float')
df['isAdult']=df['isAdult'].astype('bool')
df['genres']=df['genres'].astype('str')
df['genres']=df['genres'].apply(lambda x: x.split(','))
df['genres'] = df['genres'].apply(genres_to_list)
df['runtime']=df['runtime'].apply(convert_to_int)
print((df['isAdult']).dtype)

        
# dtypes = {
#     'tconst': 'str',
#     'titleType': 'str',
#     'primaryTitle': 'str',
#     'originalTitle': 'str',
#     'isAdult' : 'str',
#     'startYear' : 'str',
#     'endYear' : 'str',
#     'runtimeMinutes' : 'str',
#     'genres' : 'str'
#     # and so on
# }

# print(type(df['genres']).dtype)

# df['genres'] = df['genres'].apply(format_array)
# # df = df.apply(trunc)


df.to_csv('my_file_final2.csv', index=False,sep='\t',float_format='%.0f')
# TitleHasGenre.to_csv('title_genre.csv', index=False,sep='\t',float_format='%.0f')



 
# # Read in the raw TSV file
# df = pd.read_csv('name.basics.tsv', sep='\t',na_values=['\\N'])
# # df=df.fillna('NULL')


# # float_cols = df.select_dtypes(include=['float'])
# # float_cols = float_cols.replace([np.inf, -np.inf], -1)
# # # df[float_cols.columns] = float_cols.astype(int)
# # df[float_cols.columns] = float_cols.fillna(-1).astype(int)
# # Remove leading/trailing whitespace from all columns
# # df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
# df = df.rename(columns={'nconst': 'personId'})
# personkt = df.loc[:,['personId','knownForTitles']]
# personkt = personkt.rename(columns={'knownForTitles': 'titleId'})
# df=df.drop(['primaryProfession','knownForTitles'],axis=1)
# # print(df.loc[4178927,'runtimeMinutes'])

# # print(df.loc[2306457,'runtimeMinutes'])
# # print(df.loc[1097512,'runtimeMinutes'])
# # print(df.loc[4178926,7])
# # df.at[2306457,'runtimeMinutes']='1000.0'
# # df.at[1097512,'runtimeMinutes']='1000.0'
# # print(df.iloc[4178927,7])
# # mask = df == 'Reality-TV'
# # row_indices, col_indices = mask.index[mask.any(axis=1)].tolist(), mask.columns[mask.any(axis=0)].tolist()
# # print(row_indices,col_indices)
# df['birthYear']=df['birthYear'].astype('float')
# df['deathYear']=df['deathYear'].astype('float')
# # df['isAdult']=df['isAdult'].astype('bool')
# personkt['titleId']=personkt['titleId'].astype('str')
# personkt['titleId']=personkt['titleId'].apply(lambda x: x.split(','))
# personkt = personkt.explode('titleId')
# # print((df['isAdult']).dtype)

# # print(type(df['genres']).dtype)

# # df['genres'] = df['genres'].apply(format_array)
# # # df = df.apply(trunc)

# df.to_csv('person.csv', index=False,sep='\t',float_format='%.0f')
# personkt.to_csv('personKnownForTitle.csv', index=False,sep='\t',float_format='%.0f')
# print("Hello")
# df = pd.read_csv('title.principals.tsv', sep='\t',na_values=['\\N'])
# df.fillna('NULL')
# print("Hello2")
# df=df.drop(['ordering','job'],axis=1)
# df = df.rename(columns={'tconst': 'titleId','nconst':'personId','characters':'characterName'})
# # print(df)
# df['characterName']=df['characterName'].fillna('[]').astype('str')
# df['characterName']=df['characterName'].apply(lambda s: s.strip("[]"))
# df['characterName']=df['characterName'].apply(lambda x: x.split(','))
# df['characterName']=df['characterName'].apply(lambda x: x[0] if((len(x))>0) else x)


# df=df.explode('characterName')
# df['episodeNumber']=df['episodeNumber'].astype('float')
# # df['averageRating']=df['averageRating'].astype('float')
# df['seasonNumber']=df['seasonNumber'].astype('float')
# print("Hello3")

# df.to_csv('principals.csv', index=False,sep='\t',float_format='%.0f')
