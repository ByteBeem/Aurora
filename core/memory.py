import json
import datetime
from collections import defaultdict
from typing import Optional, List
from core.emotion_recognition import EmotionRecognition

class Memory:
    def __init__(self, memory_file="memory.json", decay_threshold=30):
        """
        Initializes the memory system.
        :param memory_file: Path to the file where memory is stored.
        :param decay_threshold: Days before a memory starts decaying (default: 30 days).
        """
        self.memory_file = memory_file
        self.decay_threshold = decay_threshold
        self.memory = defaultdict(lambda: {"value": None, "links": [], "priority": "casual", "emotion": None, "last_accessed": None})
        self.emotion_recognition = EmotionRecognition()
        self.load_memory()

    def load_memory(self):
        """Load memory from a file."""
        try:
            with open(self.memory_file, 'r') as file:
                self.memory.update(json.load(file))
        except FileNotFoundError:
            pass

    def save_memory(self):
        """Save memory to a file."""
        with open(self.memory_file, 'w') as file:
            json.dump(self.memory, file, indent=4)

    def remember(self, key: str, value: str, priority: str = "casual", links: Optional[List[str]] = None, emotion: Optional[str] = None):
        """
        Store a memory.
        :param key: The memory key.
        :param value: The content of the memory.
        :param priority: Priority level of the memory ('important', 'casual', etc.).
        :param links: List of related memory keys.
        :param emotion: Emotion associated with the memory.
        """
        if not emotion:
            emotion = self.emotion_recognition.dominant_emotion(value)["label"]

        if key not in self.memory:
            self.memory[key] = {
                "value": value,
                "links": links or [],
                "priority": priority,
                "emotion": emotion,
                "last_accessed": str(datetime.datetime.now())
            }
        else:
            self.memory[key]["value"] = value
            self.memory[key]["priority"] = priority
            self.memory[key]["emotion"] = emotion
            self.memory[key]["links"].extend(links or [])
            self.memory[key]["last_accessed"] = str(datetime.datetime.now())
        self.save_memory()

    def recall(self, key: str, emotion: Optional[str] = None, context: Optional[List[str]] = None) -> str:
        """
        Recall a memory based on key, emotion, or context.
        :param key: The memory key to recall.
        :param emotion: Emotion filter for recall.
        :param context: Additional context to refine recall.
        :return: The value of the memory.
        """
        if key not in self.memory:
            return "I don't remember that."
        
        memory = self.memory[key]
        memory["last_accessed"] = str(datetime.datetime.now())
        self.save_memory()

        if emotion and memory["emotion"] != emotion:
            return f"This memory exists but is linked to a different emotion: {memory['emotion']}."

        if context:
            for ctx in context:
                if ctx in memory["links"]:
                    return f"{memory['value']} (related to {ctx})"
        
        return memory["value"]
