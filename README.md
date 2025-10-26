## 1. Introduction to the Project Idea:

AI agent as a coach to evalaute the perforamce of the other AI agents, We are trying to assess the performce of the each agent by self evaluation at intermediate level.

## 2 . How to run / Setup Steps:

1) clone the repo: https://github.com/Rrp10157/Agents.git
2) Navigate into it: cd Agents
3) create virtual environemt: python -m venv myvenv
4) activate the virtual env: myvenv\Sceripts\activate
5) Install dependencies: pip install -r requirements.txt
6) add your api key in .env file: GROQ_API_KEY=your_api_key_here
7) add your redis URL in .env file: REDIS_URL= your redis url
8) Run the main.py file: python main.py
9) Which provides the URL in the terminal and when click on it, it redirects to the borwser and when you type /doc in the search bar at the end of the URL it navigate to the fastapi service
10) you can provide the input in the json formate at the fastapi service interface and get the answer along with the confidence score and intermediate reasoning


## 3 . Examples of the output when input is provided through the fastapi service:

POST /ask
{
  "query": "Explain PCA in simple terms."
}

Response:
{
  "answer": "PCA reduces dimensions by finding directions of maximum variance...",
  "confidence": 0.92
}


## Instrcutions:

1) Create .env file to store the Groq llm API key and Redis URL
2) Create virtual environmet to store the dependencies metioned in the requirements.txt file
3) Run the local_run.py file to check the performance on the hardcoded inputs 
4) Run main.py file which redirect to the Fastatapi by using the URL provided in the output, where you can enter the input and gets result realted to the input along with the confidence score etc.
5) you can find a architecture.pdf file in the repo.






