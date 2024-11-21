from transformers import pipeline

class EmotionRecognition:
    def __init__(self):
        """Initialize the emotion recognition pipeline."""
        self.emotion_model = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

    def analyze_text_emotion(self, text):
        """
        Analyze the emotion in the given text.
        :param text: The input text to analyze.
        :return: List of emotions with their confidence scores.
        """
        return self.emotion_model(text)

    def dominant_emotion(self, text):
        """
        Extract the dominant emotion from the analyzed text.
        :param text: The input text to analyze.
        :return: The most probable emotion and its score.
        """
        emotions = self.analyze_text_emotion(text)
        return max(emotions, key=lambda x: x['score'])
