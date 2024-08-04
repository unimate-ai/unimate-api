import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

file_path = 'Data.csv'
df = pd.read_csv(file_path)

df = df[['Name', 'Interests']]

df['Interests'] = df['Interests'].apply(lambda x: x.split(', '))

mlb = MultiLabelBinarizer()
interest_matrix = mlb.fit_transform(df['Interests'])
interest_df = pd.DataFrame(interest_matrix, columns=mlb.classes_, index=df['Name'])

similarity_matrix = cosine_similarity(interest_df)
similarity_df = pd.DataFrame(similarity_matrix, index=df['Name'], columns=df['Name'])

model_data = {
    "mlb": mlb,
    "interest_df": interest_df,
    "similarity_df": similarity_df
}


joblib.dump(model_data, 'recommendation_model.pkl')

