from core.memory import Memory
from core.emotion_recognition import EmotionRecognition
from core.decision_making import DecisionMaking
from core.image_processing import ImageProcessing
from core.speech_processing import SpeechProcessing

class IntegrationHub:
    def __init__(self):
        # Initialize modules
        self.memory = Memory()
        self.emotion_recognition = EmotionRecognition()
        self.decision_making = DecisionMaking()
        self.image_processing = ImageProcessing()
        self.speech_processing = SpeechProcessing()
        
        # Temporary context storage for current session
        self.session_context = {}

    def process_input(self, input_type, data):
        """
        Route input to the appropriate modules based on its type.
        :param input_type: Type of input (text, image, speech).
        :param data: Input data (text string, image file path, or audio file path).
        """
        if input_type == "text":
            emotion = self.emotion_recognition.analyze_text_emotion(data)
            self.session_context["last_emotion"] = emotion
            print(f"Emotion detected: {emotion}")
            return emotion

        elif input_type == "image":
            processed_image = self.image_processing.analyze_image(data)
            self.session_context["last_image_analysis"] = processed_image
            print(f"Image processed: {processed_image}")
            return processed_image

        elif input_type == "speech":
            transcription = self.speech_processing.transcribe_audio(data)
            emotion = self.emotion_recognition.analyze_text_emotion(transcription)
            self.session_context["last_speech_transcription"] = transcription
            self.session_context["last_emotion"] = emotion
            print(f"Speech transcribed: {transcription}")
            print(f"Emotion detected: {emotion}")
            return transcription, emotion

    def decide_action(self, description, priority=0, context=None, deadline=None):
        """
        Add a task to the decision-making system and decide the next action.
        """
        self.decision_making.add_task(description, priority, context, deadline)
        next_action = self.decision_making.decide_next_action()
        print(f"Next action decided: {next_action}")
        return next_action

    def store_context(self):
        """
        Save session-specific context to memory for future recall.
        """
        for key, value in self.session_context.items():
            self.memory.remember(key, value)
        print("Session context stored in memory.")

    def recall_context(self, key):
        """
        Recall specific context from memory.
        :param key: The memory key to retrieve.
        """
        value = self.memory.recall(key)
        print(f"Recalled context: {value}")
        return value

    def reflect_and_learn(self, outcome, context=None):
        """
        Reflect on recent actions and store lessons in memory.
        """
        self.decision_making.reflect_and_learn(outcome, context)
        print("Reflection stored in memory.")
