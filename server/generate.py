from langchain import PromptTemplate, FewShotPromptTemplate
from langchain.llms import OpenAI


llm = OpenAI(model_name="text-davinci-003", n=1, best_of=1)

# TODO: experiment with different prompts to see results

example_formatter_template = """
Characters: {character_first},{character_second}
Context: {context}\n
Output: {output}
"""

character_first_1 = "Yasmin"
character_first_2 = "Raj"
output1 = """
Verse 1:
Under the moonlight, we met on the terrace
Hand in hand, our love was a sweet embrace
We talked of forever, and all that we dreamed
But now we must part, our love it seems

Chorus:
Our love was pure, our hearts true
But now we're forced to bid adieu
To the memories we hold so dear
And the love that will forever be here

Verse 2:
Yasmin you'll leave, with your family in tow
To start a new life, in Amritsar you'll go
While Raj remains, to visit the pain
Of the places that have broken his heart in vain

Chorus:
Our love was pure, our hearts true
But now we're forced to bid adieu
To the memories we hold so dear
And the love that will forever be here

Bridge:
Time will flow, we'll both move on
New lives we'll make, our love we'll carry on
But the memories, of our time together
Will always stay with us, now and forever

Chorus:
Our love was pure, our hearts true
But now we're forced to bid adieu
To the memories we hold so dear
And the love that will forever be here

Outro:
Yasmin, my love, we'll meet again
In this world or the next, our love will remain
For you, my love, will always be
The one my heart beats for, eternally.
"""

context1 = """
The two lovers, Yasmin and Raj, are separated due to the partition of India. 
Yasmin is forced to leave her home and town along with her family to start a new life in Amritsar. 
Meanwhile, Raj remains behind. They meet for the last time on the terrace where they used to meet under the moonlight, 
but their world has already crumbled. They both leave with heavy hearts, unsure if they will ever meet again. 
Yasmin is resigned to the fact that she will have to get married soon, while Raj is left behind to visit the places 
that have broken his heart. Time will flow and both of them will move on and make new lives for themselves, 
but the memories of their time together will always stay with them.
"""

character_second_1 = "Tom"
character_second_2 = "Jerry"

output2 = """
Verse 1:
Tom and Jerry, always in a race
One a mouse, the other with grace
They may fight, they may brawl
But deep down, they love it all

Chorus:
Together they roam, hand in paw
Their love shines bright, never a flaw
They may be different, but that's just fine
Tom and Jerry, love will always be thine

Verse 2:
Jerry's quick, Tom's always sly
Their love story, never will die
They dance and sing, through the night
Their love, a beautiful sight

Chorus:
Together they roam, hand in paw
Their love shines bright, never a flaw
They may be different, but that's just fine
Tom and Jerry, love will always be thine

Bridge:
They say that love is just a game
But with each other, it will always remain
Through thick and thin, they'll stand by
Tom and Jerry, till the day they die

Chorus:
Together they roam, hand in paw
Their love shines bright, never a flaw
They may be different, but that's just fine
Tom and Jerry, love will always be thine

Outro:
Tom and Jerry, two hearts entwine
Their love, a beautiful sign
Together forever, side by side
Tom and Jerry, love will always abide.
"""


context2 = """
The story is about the relationship between Tom and Jerry, a cat and a mouse who live in the same house and are always at odds with each other. Jerry finds a delicious cheese and Tom tries to claim it as his own, leading to a comical chase. However, their chase attracts the attention of a group of stray cats and they end up working together to escape the situation. Through this experience, Tom and Jerry realize that working together is more fulfilling than constantly fighting and they become the best of friends. Tom is sarcastic and likes to play tricks, while Jerry is clever and always one step ahead.
"""

examples = [
    {
        "character_first": character_first_1,
        "character_second": character_first_2,
        "context": context1,
        "output": output1,
    },
    {
        "character_first": character_second_1,
        "character_second": character_second_2,
        "context": context2,
        "output": output2,
    },
]


def generate_love_song(character_first: str, character_second: str, context: str):
    try:
        example_prompt = PromptTemplate(
            input_variables=[
                "character_first",
                "character_second",
                "context",
                "output",
            ],
            template=example_formatter_template,
        )

        few_shot_prompt = FewShotPromptTemplate(
            examples=examples,
            example_prompt=example_prompt,
            prefix="Write a love between the characters given the context",
            suffix="Characters: {character_first} and {character_second}\nContext: {context}\nOutput:",
            input_variables=["character_first", "character_second", "context"],
            example_separator="\n\n",
        )

        final_prompt = few_shot_prompt.format(
            character_first=character_first,
            character_second=character_second,
            context=context,
        )
        print(final_prompt)
        # call API with prompt
        return llm(final_prompt)
    except Exception as e:
        print("Error generating completion: ", e)
        raise e
