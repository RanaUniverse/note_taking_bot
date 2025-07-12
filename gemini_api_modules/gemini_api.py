"""
This is my module where i will keep the code realted to
gemini api which i will import later
"""

from google import genai

from my_modules import bot_config_settings


GEMINI_MODEL_NAME = bot_config_settings.GEMINI_MODEL_NAME
GEMINI_API_KEY = bot_config_settings.GEMINI_API_KEY


# prompt = "state pythogorus themorem in math in 15 word"
# response = client.models.generate_content(  # type: ignore
#     model=MODEL_NAME,
#     contents=prompt,
# )
# print(response.text)


client = genai.Client(api_key=GEMINI_API_KEY)


def answer_question_from_ai(question: str) -> str | None:
    """
    I will call this function in need time
    which will allow a output a which i will use later
    """

    response = client.models.generate_content(  # type: ignore
        model=GEMINI_MODEL_NAME,
        contents=question,
    )

    if not response.text:
        return None

    answer = f"{response.text}" f"\n\n\n" f"-RanaUniverse"

    return answer


if __name__ == "__main__":

    question = "What is ai say in 10 word?"

    ai_response = answer_question_from_ai(question)
    print(ai_response)
    print("Thanks")
