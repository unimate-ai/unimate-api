# fastapi_app.py
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

# Load and preprocess the dataset
file_path = 'path/to/Adjusted_Combined_Table.csv'
df = pd.read_csv(file_path)
df = df[['Name', 'Interests']]
df['Interests'] = df['Interests'].apply(lambda x: x.split(', '))

mlb = MultiLabelBinarizer()
interest_matrix = mlb.fit_transform(df['Interests'])
interest_df = pd.DataFrame(interest_matrix, columns=mlb.classes_, index=df['Name'])

similarity_matrix = cosine_similarity(interest_df)
similarity_df = pd.DataFrame(similarity_matrix, index=df['Name'], columns=df['Name'])

def recommend_students(student_interests, top_n=5):
    new_student_matrix = mlb.transform([student_interests])
    new_student_df = pd.DataFrame(new_student_matrix, columns=mlb.classes_)
    new_student_similarity = cosine_similarity(new_student_df, interest_df).flatten()
    new_student_similarity_df = pd.DataFrame(new_student_similarity, index=similarity_df.index, columns=['similarity'])
    sorted_similarity_df = new_student_similarity_df.sort_values(by='similarity', ascending=False)
    top_matches = sorted_similarity_df.head(top_n).index.tolist()
    return top_matches

# Define request and response models
class RecommendationRequest(BaseModel):
    interests: list[str]
    top_n: int = 5

class RecommendationResponse(BaseModel):
    recommended_students: list[str]

# Create FastAPI app
app = FastAPI()

@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest):
    recommended_students = recommend_students(request.interests, request.top_n)
    return RecommendationResponse(recommended_students=recommended_students)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
