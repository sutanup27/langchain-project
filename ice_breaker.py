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
from dotenv import load_dotenv

import os
information="""
Jadavpur University (abbr. JU)[5] is a public state funded technical and research university with its main campus located at Jadavpur, Kolkata, West Bengal, India. It was established on 25 July in 1906 as Bengal Technical Institute and was converted into Jadavpur University on 24 December in 1955.[6] As of the 2024 NIRF rankings, Jadavpur University has been ranked 9th among universities, 12th among engineering institutes, and 17th overall in India.[7] Also Nature Index ranked Jadavpur University in 1st among universities in India and 22nd overall in India in terms of research output (2023-2024). The university has been recognized by the UGC as an institute with "Potential for Excellence"[8] and accredited an "A+" grade by the National Assessment and Accreditation Council (NAAC).[9][10]

History

Stamp featuring Jadavpur University
On 25 July 1906, Bengal Technical Institute was founded by Society for the Promotion of Technical Education by at 92, Upper Circular Road. On 7 July 1910, the Society for the Promotion of Technical Education in Bengal was merged with the National Council of Education (NCE).[11] The institute became College of Engineering and Technology, Bengal looked after by NCE.[12][13] After Independence, on 24 December 1955, Jadavpur University was officially established by the Government of West Bengal with the concurrence of the Government of India.[6]
"""

if __name__ == "__main__":
    print("hello langchain")

    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini",api_key=os.getenv("OPENAI_API_KEY"))

    chain = summary_prompt_template | llm
 
    res = chain.invoke(input={"information": information})

    print(res)