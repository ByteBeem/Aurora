from datetime import datetime
from core.memory import Memory
from core.emotion_recognition import EmotionRecognition

class DecisionMaking:
    def __init__(self):
        self.tasks = []  # Stores all tasks
        self.memory = Memory()  # Integrates with memory for context-aware decisions
        self.emotion_recognition = EmotionRecognition()  # Integrates emotions into decision-making

    def add_task(self, description, priority=0, context=None, deadline=None, emotion=None):
        """
        Add a task to the decision-making queue.
        :param description: The task description.
        :param priority: The priority level of the task (default: 0).
        :param context: Contextual information or related tasks.
        :param deadline: Optional deadline for the task.
        :param emotion: Optional associated emotion for the task.
        """
        if not emotion:
            emotion = self.emotion_recognition.dominant_emotion(description)["label"]

        task = {
            "description": description,
            "priority": priority,
            "context": context or [],
            "deadline": deadline,
            "emotion": emotion,
            "added_at": str(datetime.now())
        }
        self.tasks.append(task)
        self.memory.remember(f"task_{len(self.tasks)}", task)

    def prioritize_tasks(self):
        """
        Sort tasks based on a combination of priority, deadlines, and emotional influence.
        :return: A sorted list of tasks.
        """
        def calculate_priority(task):
            # Base priority
            priority_score = task["priority"]

            # Boost tasks with imminent deadlines
            if task["deadline"]:
                deadline_diff = (datetime.fromisoformat(task["deadline"]) - datetime.now()).total_seconds()
                if deadline_diff < 3600:  # Less than 1 hour
                    priority_score += 5
                elif deadline_diff < 86400:  # Less than 1 day
                    priority_score += 3

            # Adjust priority based on associated emotion
            if task["emotion"] in ["fear", "urgency"]:
                priority_score += 2
            elif task["emotion"] in ["joy", "interest"]:
                priority_score += 1

            return priority_score

        self.tasks.sort(key=calculate_priority, reverse=True)
        return self.tasks

    def decide_next_action(self):
        """
        Decide the next action based on prioritized tasks and human-like factors.
        :return: The next task or None if no tasks are available.
        """
        if not self.tasks:
            return None

        # Prioritize tasks before making a decision
        self.prioritize_tasks()
        next_task = self.tasks.pop(0)  # Take the highest priority task

        # Record the decision in memory for future context
        self.memory.remember("last_decision", next_task)
        return next_task

    def reflect_and_learn(self, outcome, context=None):
        """
        Reflect on the outcome of a decision to improve future decision-making.
        :param outcome: Outcome of the last decision (e.g., "success", "failure").
        :param context: Additional context or reasons for the outcome.
        """
        reflection = {
            "outcome": outcome,
            "context": context,
            "timestamp": str(datetime.now())
        }
        self.memory.remember("decision_reflection", reflection)
