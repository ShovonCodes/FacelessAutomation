import os
from openai import OpenAI
from dotenv import load_dotenv
from classes.utils import pick_random

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
        print('Creating prompt!')
        topic = pick_random(topics)
        print('Writing prompt on topic: ', topic)
        prompt = f"""
                Create a short, engaging, and inspiring story on the topic "{topic}".
                The story should convey a powerful moral lesson, be easy to understand for viewers of all ages, 
                and evoke a sense of hope and resilience. Use simple language, make the story relatable, 
                and include a strong takeaway that encourages perseverance in the face of difficulties. 
                The response should only include the story, with no additional explanations or notes.
                The story should not be more than 340 characters.
                """
        return prompt

    def generate_story(self):
        prompt = self.generate_prompt()
        print('Generating story!')
        
        client = OpenAI(api_key=api_key)

        conversation = []
        conversation.append({'role': 'system', 'content': "You are an AI that generates original, thought-provoking, and inspiring quotes. Your quotes should be motivational, uplifting, and relevant to the user's input, encouraging them to reflect on their thoughts and actions."})
        conversation.append({'role': 'user', 'content': prompt})
        story_response = client.chat.completions.create(messages=conversation, model="gpt-3.5-turbo")
        story = story_response.choices[0].message.content
        conversation.append({
            'role': 'user', 
            'content': """
                        Create a title for this story followed by relevant hashtags, without using any quotation marks, 
                        special characters, or additional text. The output should be formatted as: "Title [space] #Hashtag1 #Hashtag2 #Hashtag3". 
                        Make sure the title and hashtags are on the same line, with no quotation marks or additional formatting. 
                        Only include the title and hashtags.
                        """
                    })
        title_response = client.chat.completions.create(messages=conversation, model="gpt-3.5-turbo")
        title = title_response.choices[0].message.content
        
        return {
            "story": story,
            "title": title
        }
