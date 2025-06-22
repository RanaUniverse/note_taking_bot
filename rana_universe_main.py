import random
from telegram.constants import ReactionEmoji

random_emoji = random.choice(list(ReactionEmoji))

print(random_emoji.value)





# Select only the specific emojis you want
selected_emojis = [
    ReactionEmoji.THUMBS_UP,
    ReactionEmoji.TROPHY,
    ReactionEmoji.BANANA
]

# Pick one at random
random_emoji = random.choice(selected_emojis)

print(random_emoji.value)