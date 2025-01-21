import os
from openai import OpenAI
from dotenv import load_dotenv
from classes.utils import separate_title_and_story

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

topics = [
    'Overcoming Challenges and Adversity',
    'The Power of Kindness and Compassion',
    'Finding Inner Peace and Mindfulness',
    'The Value of Honesty and Integrity',
    'Wisdom from Famous Historical Figures',
    'The Importance of Gratitude and Contentment',
    'Learning from Failures and Mistakes',
    'The Role of Love and Relationships in Life',
    'The Value of Time and Patience',
    'The Ripple Effect of Small Good Deeds',
    'Finding Strength in Vulnerability',
    'Learning Patience in a Fast-Paced World',
    'The Power of Self-Discipline and Commitment',
    'Life Lessons from Ancient Wisdom',
    'Leadership through Compassion',
    'Acts of Forgiveness and Letting Go',
    'The Beauty of Simplicity',
    'Navigating the Digital World with Integrity',
    'Understanding Empathy and Emotional Intelligence',
    'Learning to Let Go of Control',
    'Embracing Failure as a Step Toward Success',
    ]

class StoryEngine:
    def generate_prompt(self):
        print('Generating prompt!')
        # topic = pick_random(topics)
        # print('Writing prompt on topic: ', topic)
        prompt = f"""
                You are an expert storyteller and educator specializing in cryptocurrency, with the ability to simplify complex concepts for beginners. Create a unique, engaging, and beginner-friendly script for a short YouTube video (20–35 seconds) about cryptocurrency. The script should:

                Start with a Hook: Begin with a surprising fact, a thought-provoking question, or a relatable analogy to immediately grab the viewer's attention.
                Explain the Concept: Dive straight into the main topic, explaining it in simple, approachable terms using creative analogies, examples, or relatable comparisons. Assume the audience knows nothing about the subject.
                Conclude with Curiosity: End with a thought, comparison, or question that leaves viewers intrigued and wanting to learn more.
                Maintain a Fun-Professional Tone: Blend professionalism with lightness to keep it both educational and entertaining.
                Guidelines:
                Avoid intros or outros; start directly with the hook.
                Keep jargon to a minimum and always explain terms in simple language.
                Be concise yet descriptive, balancing information with creativity.
                Cover a variety of topics such as specific cryptocurrencies (Bitcoin, Ethereum, Dogecoin), technical concepts (blockchain, mining, NFTs), market phenomena (volatility, meme coins), or real-world applications (smart contracts, DeFi).
                Examples of Output Style:
                Bitcoin: The Digital Gold Rush
                "Did you know Bitcoin is like digital gold? Precious, scarce, but instead of being mined with shovels, it’s mined with computers solving puzzles. These puzzles make Bitcoin secure, and that's why some call it the 'gold of the internet.' Would you trade your shovel for a supercomputer?"

                Blockchain: The Future's Unchangeable Diary
                "Imagine a diary that everyone can see, but no one can alter—sounds futuristic, right? That’s what a blockchain is! It’s like a shared diary that keeps track of transactions, making sure everything is fair and secure. So, who’s ready to write in the future’s diary?"

                NFTs: The Era of Digital Collectibles
                "Think of NFTs as digital collectibles, like rare baseball cards, but online. Unlike regular files you can copy, NFTs are one-of-a-kind, with proof of ownership recorded on the blockchain. Would you trade a paper card for a virtual masterpiece?"

                Cryptocurrency Volatility: The Rollercoaster of Digital Wealth
                "Why do cryptocurrencies rise and fall like a rollercoaster? It’s all about hype, demand, and memes. Take Dogecoin—it started as a joke but skyrocketed when the internet couldn’t stop talking about it. Ready for the ride?"
                """
        return prompt

    def generate_story(self):
        prompt = self.generate_prompt()
        print('Generating story!')
        
        client = OpenAI(api_key=api_key)

        conversation = []
        conversation.append({'role': 'user', 'content': prompt})
        story_response = client.chat.completions.create(messages=conversation, model="gpt-3.5-turbo")
        text = story_response.choices[0].message.content
        # conversation.append({
        #     'role': 'user', 
        #     'content': """
        #                 Create a title for this story followed by relevant hashtags, without using any quotation marks, 
        #                 special characters, or additional text. The output should be formatted as: "Title [space] #Hashtag1 #Hashtag2 #Hashtag3". 
        #                 Make sure the title and hashtags are on the same line, with no quotation marks or additional formatting. 
        #                 Only include the title and hashtags.
        #                 """
        #             })
        # title_response = client.chat.completions.create(messages=conversation, model="gpt-3.5-turbo")
        # title = title_response.choices[0].message.content
        
        print('The original text: ', text)
        title, story = separate_title_and_story(text)
        
        return {
            "story": story,
            "title": title
        }
