from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

model_data = joblib.load('recommendation_model.pkl')
mlb = model_data['mlb']
interest_df = model_data['interest_df']
similarity_df = model_data['similarity_df']

def recommend_students(student_interests, top_n):
    new_student_matrix = mlb.transform([student_interests])
    new_student_df = pd.DataFrame(new_student_matrix, columns=mlb.classes_)
    new_student_similarity = cosine_similarity(new_student_df, interest_df).flatten()
    new_student_similarity_df = pd.DataFrame(new_student_similarity, index=similarity_df.index, columns=['similarity'])
    sorted_similarity_df = new_student_similarity_df.sort_values(by='similarity', ascending=False)
    top_matches = sorted_similarity_df.head(top_n).index.tolist()
    return top_matches

class RecommendationRequest(BaseModel):
    interests: list[str]
    top_n: int = 5

class RecommendationResponse(BaseModel):
    recommended_students: list[str]

app = FastAPI()

@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest):
    recommended_students = recommend_students(request.interests, request.top_n)
    return RecommendationResponse(recommended_students=recommended_students)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
