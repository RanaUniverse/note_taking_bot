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


tg_api_formatting = f"""
HTML style
To use this mode, pass HTML in the parse_mode field. The following tags are currently supported:

<b>bold</b>, <strong>bold</strong>
<i>italic</i>, <em>italic</em>
<u>underline</u>, <ins>underline</ins>
<s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
<span class="tg-spoiler">spoiler</span>, <tg-spoiler>spoiler</tg-spoiler>
<b>bold <i>italic bold <s>italic bold strikethrough <span class="tg-spoiler">italic bold strikethrough spoiler</span></s> <u>underline italic bold</u></i> bold</b>
<a href="http://www.example.com/">inline URL</a>
<a href="tg://user?id=123456789">inline mention of a user</a>

"""


extra_info_with_question = f" " f"Use appropriate lot of emoji in the answer."


def answer_question_from_ai(question: str) -> str | None:
    """
    I will call this function in need time
    which will allow a output a which i will use later
    """

    what_to_ask = question + extra_info_with_question

    response = client.models.generate_content(  # type: ignore
        model=GEMINI_MODEL_NAME,
        contents=what_to_ask,
    )

    if not response.text:
        return None

    answer = f"{response.text}" f"\n\n\n" f"-RanaUniverse"

    if len(answer) > 4000:
        answer = answer[0:4000]
    return answer


if __name__ == "__main__":

    question = "What is ai say in 10 word?"

    ai_response = answer_question_from_ai(question)
    print(ai_response)
    print("Thanks")
