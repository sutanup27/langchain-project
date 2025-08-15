# from typing import Tuple
# from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
# from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
# from chains.custom_chains import (
#     get_summary_chain,
#     get_interests_chain,
#     get_ice_breaker_chain,
# )
# from third_parties.linkedin import scrape_linkedin_profile
# from third_parties.twitter import scrape_user_tweets, scrape_user_tweets_mock
# from output_parsers import (pip
#     Summary,
#     IceBreaker,
#     TopicOfInterest,
# )


# def ice_break_with(
#     name: str,
# ) -> Tuple[Summary, TopicOfInterest, IceBreaker, str]:
#     linkedin_username = linkedin_lookup_agent(name=name)
#     linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)

#     twitter_username = twitter_lookup_agent(name=name)
#     tweets = scrape_user_tweets_mock(username=twitter_username)

#     summary_chain = get_summary_chain()
#     summary_and_facts: Summary = summary_chain.invoke(
#         input={"information": linkedin_data, "twitter_posts": tweets},
#     )

#     interests_chain = get_interests_chain()
#     interests: TopicOfInterest = interests_chain.invoke(
#         input={"information": linkedin_data, "twitter_posts": tweets}
#     )

#     ice_breaker_chain = get_ice_breaker_chain()
#     ice_breakers: IceBreaker = ice_breaker_chain.invoke(
#         input={"information": linkedin_data, "twitter_posts": tweets}
#     )

#     return (
#         summary_and_facts,
#         interests,
#         ice_breakers,
#         linkedin_data.get("photoUrl"),
#     )

from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from social_scrap.linkedin_scrap import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup
from tools.output_parsers import Summary, summary_parser
from dotenv import load_dotenv
import os


load_dotenv()

def ice_break_with(name: str) -> tuple[Summary,str]:
    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them

     \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template,
        partial_variables={"format_instructions":summary_parser.get_format_instructions()}
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini",api_key=os.environ["OPENAI_API_KEY"])

    chain = summary_prompt_template | llm | summary_parser
    
    linkedin_url=lookup(name)
    linkedin_data=scrape_linkedin_profile(linkedin_url)
    res:Summary = chain.invoke(input={"information": linkedin_data})

    return res, linkedin_data.get("photoUrl")

if __name__ == "__main__":
    print("hello langchain")
    name="Amrita CHandra DUblin"
    res, photo=ice_break_with(name)
    print(res)
    print(photo)