# UniMate
Over half of young Australians, those aged 16-25, experience stress and concern due to loneliness, which increases the risk of mental health issues and sleeping 
problems. UniMate is an app designed to address this issue by connecting new university students with like-minded peers and recommending relevant uni events using AI. 
Through UniMate, students are encouraged to take part in campus and off-campus events, meeting new people in the process. Our business model is B2B, where we sell our white-labeled solution to campuses across Australia, so they can create a unique orientation experience and foster a connected campus community.

## Running the app locally
1. Clone this repository using `git clone`
2. Create virtual environments using `python -m venv .venv`
3. Activate venv `source .venv/bin/activate`
4. Install all dependencies through `pip install -r requirements.txt`
4. Ensure you have the correct environment variables in your `.env` file located at the root of the project
5. Run `make dev` and the app should run on your local machine

## Containerizing and Running the app with Docker
1. Clone this repository using `git clone`
2. Ensure you have Docker Engine and Docker Daemon installed on your machine
3. Build Docker Image using `docker build . --file ./Dockerfile --tag unimate-api`
4. Run container from image using Docker Desktop or on CLI: `docker run -it unimate-api`
5. Your app should be up and running!