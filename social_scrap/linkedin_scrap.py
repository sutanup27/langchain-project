from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

import requests


load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url:str, mock:bool=False):
    if mock:
        profile_url="https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json"
        response=requests.get(
            url=profile_url,
            timeout=10
        )
    else:
        scrapin_api_url="https://api.scrapin.io/v1/enrichment/profile"
        params={
        "apikey":os.environ["SCRAPIN_API_KEY"],
        "linkedInUrl":linkedin_profile_url

        }
        response=requests.get(
            url=scrapin_api_url,
            params=params,
            timeout=10
        )

    data = response.json().get("person")
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None) and k not in ["certifications"]
    }

    return data

if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/amrita-chandra-a47b86143/"
        ),
    )