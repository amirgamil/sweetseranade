from langchain import PromptTemplate, FewShotPromptTemplate
from langchain.llms import OpenAI



example_formatter_template = """
Characters: {character_first},{character_second}
Style: {style}
Context: {context}
Output: {output}
"""

character_first_1 = "Yasmin"
character_first_2 = "Raj"
style_1 = "Indian bollywood rap by Eminem"
output1 = """
Verse 1:
Listen up people, this story's real
Of two hearts in love that's beyond the steel
Yasmin and Raj, they fell so fast
But they were separated, torn apart at last

Chorus:
They met on the terrace under the moonlight
Their love was strong, but their world took flight
They both had to leave, their fate was sealed
But Yasmin and Raj, their love was revealed

Verse 2:
Raj stayed behind, with a broken heart
Places that he loved, now falling apart
But he said with pride, with a smile so bright
"Even if our bodies are apart, our hearts will always beat as one, with all our might"

Chorus:
They met on the terrace under the moonlight
Their love was strong, but their world took flight
They both had to leave, their fate was sealed
But Yasmin and Raj, their love was revealed

Verse 3:
Yasmin left with tears, with a heavy heart
Her home, her town, they were falling apart
But she had to go, she had to start
"I am but a bird forced to leave its nest, but I will carry your love with me wherever I go, that's a fact"

Chorus:
They met on the terrace under the moonlight
Their love was strong, but their world took flight
They both had to leave, their fate was sealed
But Yasmin and Raj, their love was revealed

Outro:
They both will move on, make new lives for themselves
But their memories of love, will always stay on the shelves
Yasmin and Raj, their love will endure
For their hearts will always beat, strong and pure.
"""

context1 = """
The two lovers, Yasmin and Raj, are separated due to the partition of India. 
Yasmin is forced to leave her home and town along with her family to start a new life in Amritsar. 
Meanwhile, Raj remains behind. They meet for the last time on the terrace where they used to meet under the moonlight, 
but their world has already crumbled. They both leave with heavy hearts, unsure if they will ever meet again. 
Yasmin is resigned to the fact that she will have to get married soon, while Raj is left behind to visit the places 
that have broken his heart. Time will flow and both of them will move on and make new lives for themselves, 
but the memories of their time together will always stay with them. Quotes to include could be 'Even if our bodies are apart, our hearts will always beat as one' from Raj or
'I am but a bird forced to leave its nest, but I will carry your love with me wherever I go' by Yasmin.
"""

character_second_1 = "Tom"
character_second_2 = "Jerry"
style_2 = "high school musical of a forbidden romance"
output2 = """
Verse 1: Tom
We used to be foes, fighting every day
But now I realize, it's better this way
You always keep me on my toes, never dull
I can't help but fall, for this love is full

Chorus:
We were two hearts at odds, but now we're so much more
Together we can take on the world, and so much more
I never thought I'd see, you and I in harmony
But here we are, in this forbidden love, you and me

Verse 2: Jerry
I used to think we'd never get along
But you and I, it's where we belong
Our love is like a game, where I'm always one step ahead
But it's worth it all, just to see you smile before I'm in bed

Chorus:
We were two hearts at odds, but now we're so much more
Together we can take on the world, and so much more
I never thought I'd see, you and I in harmony
But here we are, in this forbidden love, you and me

Bridge:
No matter what the world may say, our love will always stay
We'll be each other's ally, and never let each other stray
We'll sing this love song, and dance until the night is gone
Our love will be our light, and we'll always carry on

Chorus:
We were two hearts at odds, but now we're so much more
Together we can take on the world, and so much more
I never thought I'd see, you and I in harmony
But here we are, in this forbidden love, you and me.
"""


context2 = """
The story is about the relationship between Tom and Jerry, a cat and a mouse who live in the same house and are always at odds with each other. Jerry finds a delicious cheese and Tom tries to claim it as his own, leading to a comical chase. However, their chase attracts the attention of a group of stray cats and they end up working together to escape the situation. Through this experience, Tom and Jerry realize that working together is more fulfilling than constantly fighting and they become the best of friends. Tom is sarcastic and likes to play tricks, while Jerry is clever and always one step ahead. Quotes to include could be "You may be fast, Jerry, but I'm always one step ahead" by Tom or "Don't worry, Tom. I'll always be here to keep you on your toes" by Jerry. 
"""

examples = [
    {
        "character_first": character_first_1,
        "character_second": character_first_2,
        "style": style_1,
        "context": context1,
        "output": output1,
    },
    {
        "character_first": character_second_1,
        "character_second": character_second_2,
        "style": style_2,
        "context": context2,
        "output": output2,
    },
]


def generate_love_song(character_first: str, character_second: str, context: str, style: str, openai_api_key: str):
    try:
        if openai_api_key:
          llm_complete = OpenAI(model_name="text-davinci-003", n=1, best_of=1, openai_api_key=openai_api_key)
        else:
          llm_complete = OpenAI(model_name="text-davinci-003", n=1, best_of=1)
        example_prompt = PromptTemplate(
            input_variables=[
                "character_first",
                "character_second",
                "style",
                "context",
                "output",
            ],
            template=example_formatter_template,
        )

        few_shot_prompt = FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix="Write a love song between the characters given the context",
            suffix="Characters: {character_first},{character_second}\nStyle:{style}\nContext: {context}\nOutput:",
            input_variables=["character_first", "character_second", "style", "context"],
            example_separator="\n\n",
        )

        final_prompt = few_shot_prompt.format(
            character_first=character_first,
            character_second=character_second,
            style=style,
            context=context.strip(),
        )
        # call API with prompt
        return llm_complete(final_prompt)
    except Exception as e:
        print("Error generating completion: ", e)
        raise e
