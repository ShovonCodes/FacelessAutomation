import os
import random
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch the OpenAI API key from the environment variables
api_key = os.getenv('OPENAI_API_KEY')

class StoryEngine:
    def __init__(self):
        self.client = OpenAI(api_key=api_key)
        self.topics = [
            "cryptocurrency",
            "blockchain technology",
            "artificial intelligence",
            "green energy solutions",
            "NFTs",
            "smart contracts",
            "financial markets",
            "DeFi applications",
        ]
        self.prompt_styles = [
            "Explain {topic} using a fun analogy, like comparing it to baking a cake or playing a video game.",
            "Show how {topic} affects everyday life by describing a practical scenario.",
            "What’s the future of {topic}? Provide a beginner-friendly prediction in an engaging way.",
            "Why is {topic} so popular? Explain its appeal with a fun story.",
            "Describe a real-world application of {topic} that solves a common problem.",
        ]

    def get_random_topic(self):
        """Randomly selects a topic from the list of topics."""
        return random.choice(self.topics)

    def generate_prompt(self, topic):
        """Generates a unique prompt by combining a random topic and storytelling style."""
        style = random.choice(self.prompt_styles)
        prompt = style.format(topic=topic)
        guidelines = """
        The resulting script should:

        - Start with a Hook: Begin with a surprising fact, a thought-provoking question, or a relatable analogy to immediately grab the viewer's attention.
        - Explain the Concept: Dive into the topic using creative analogies and approachable language.
        - Conclude with Curiosity: Leave viewers intrigued and wanting to learn more.
        - Maintain a Fun-Professional Tone: Blend professionalism with lightness to keep it both educational and entertaining.
        - Limited word: Curate a story that is fun, engaging, and informative within 400 characters.

        Guidelines:
        - Avoid intros or outros; start directly with the hook.
        - Keep jargon to a minimum and always explain terms in simple language.
        - Be concise yet descriptive, balancing information with creativity.
        """
        return f"{prompt}\n\n{guidelines}"

    def generate_story(self):
        """Generates a story and title based on a randomly selected topic and style."""
        topic = self.get_random_topic()
        prompt = self.generate_prompt(topic)

        # Generate story using OpenAI API
        print("Generating story...")
        messages = [
            {
                "role": "system",
                "content": f"You are an expert storyteller and educator specializing in cryptocurrency, with the ability to simplify complex concepts for beginners. Create a unique, engaging, and beginner-friendly script for a short YouTube video (around 25 seconds) about {topic}"
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

# Example usage
if __name__ == "__main__":
    story_engine = StoryEngine()
    result = story_engine.generate_story()
    print("Generated Topic:", result["topic"])
    print("Generated Story:\n", result["story"])
    print("Generated Title:\n", result["title"])
