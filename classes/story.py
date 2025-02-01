import os
import random
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch the OpenAI API key from the environment variables
api_key = os.getenv('OPENAI_API_KEY')

class StoryEngine:
    def __init__(self, topics = None, prompt_styles = None, guidelines = None, system_message = None):
        self.client = OpenAI(api_key=api_key)
        self.topics = topics if topics else []
        self.prompt_styles = prompt_styles if prompt_styles else []
        self.guidelines = guidelines if guidelines else ""
        self.system_message = system_message if system_message else []

    def get_random_topic(self):
        """Randomly selects a topic from the list of topics."""
        if not len(self.topics):
            return None
        
        return random.choice(self.topics)

    def generate_prompt(self, topic):
        """Generates a unique prompt by combining a random topic and storytelling style."""
        if not len(self.prompt_styles):
            return None
        
        style = random.choice(self.prompt_styles)
        prompt = style.format(topic=topic)

        return f"{prompt}\n\n{self.guidelines}"

    def generate_story(self):
        """Generates a story and title based on a randomly selected topic and style."""
        topic = self.get_random_topic()
        prompt = self.generate_prompt(topic)

        if not topic or not prompt:
            print("Error: Unable to generate a story. Prompt or topic not found.")
            return {}
        
        print("Generated Topic:", topic)
        print("Generated Prompt:\n", prompt)

        # Generate story using OpenAI API
        print("Generating story...")
        messages = [
            {
                "role": "system",
                "content": self.system_message.format(topic=topic)
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        story_response = self.client.chat.completions.create(messages=messages, model="gpt-4o-mini")
        story = story_response.choices[0].message.content.strip()

        # Generate title and hashtags
        print("Generating title and hashtags...")
        title_prompt = """
        Create a title for this story followed by relevant hashtags, without using any quotation marks, 
        special characters, or additional text. The output should be formatted as: 
        "Title [space] #Shorts #Hashtag1 #Hashtag2 #Hashtag3". Only include the title and hashtags.
        """
        messages.append({"role": "user", "content": title_prompt})
        title_response = self.client.chat.completions.create(messages=messages, model="gpt-4o-mini")
        title = title_response.choices[0].message.content.strip()
        
        print("Topic: ", topic)
        print("Story: ", story)
        print("Title: ", title)
        

        return {
            "story": story,
            "title": title,
        }
