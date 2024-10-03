import os
from openai import OpenAI
from dotenv import load_dotenv
from classes.utils import pick_random

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

print('THE API KEY: ', api_key)

topics = ['Life Lessons', 'Health & Wellness', 'Relationships', 'Mindfulness & Meditation', 'Success & Motivation', 'Happiness & Positivity', 'Courage & Fear', 'Gratitude & Appreciation', 'Wisdom & Knowledge', 'Change & Adaptability']
values = ['uplifting', 'empowering', 'reflective', 'humorous']

class StoryEngine:
    def generate_prompt(self):
        print('Creating prompt!')

        prompt = f"""
            Generate motivational quotes based story focused on {pick_random(topics)}. Set a tone that is {pick_random(values)}, 
            ensuring it resonates with the intended audience of all ages. Draw inspiration from famous quotes that motivates people, 
            while infusing a touch of unique style. Prioritize quotes that are concise, impactful, and filled with actionable advice. 
            Emphasize values and encourage positivity.

            Keeping the above in mind, the story should be around 300 characters. Only output the actual story and 
            do not respond with any header of footer note.
        """
        return prompt

    def generate_story(self):
        prompt = self.generate_prompt()
        print('Generating story!')
        
        client = OpenAI(api_key=api_key)

        conversation = []
        conversation.append({'role': 'system', 'content': "You are an AI that generates original, thought-provoking, and inspiring quotes. Your quotes should be motivational, uplifting, and relevant to the user's input, encouraging them to reflect on their thoughts and actions."})
        conversation.append({'role': 'user', 'content': prompt})
        response = client.chat.completions.create(messages=conversation, model="gpt-3.5-turbo")

        result = response.choices[0].message.content
        return result
