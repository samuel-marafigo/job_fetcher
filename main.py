import asyncio
from flask import Flask, request, jsonify
from fetcher import fetcherResult 

app = Flask(__name__)

@app.route("/")
def home():
    return asyncio.run(main())

async def main():
    print("entrei")
    job_titles = ["estagiario", "estagio", "junior", "desenvolvedor", "developer", "java", "python", "react", "backend", "fullstack", "intern", "suporte", "support"]
    merged_results = await fetcherResult(job_titles)
    return jsonify(merged_results)

if __name__ == "__main__":
    app.run(debug=True)