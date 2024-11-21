# bot/responses.py

def welcome_message(user_name: str) -> str:
    """Personalized welcome message."""
    return f"Hello {user_name}! 🌟 I'm Aurora, your smart forex trading assistant. Let’s dive into the markets today!"

def trading_signal_response(signal: str) -> str:
    """Message for trading signals."""
    return (
        f"Here's what I think: the trend suggests it's a good time to {signal}. "
        "Should I execute the trade for you? 🤔"
    )

def empathy_response() -> str:
    """Supportive message."""
    return "Trading can be tough sometimes, but I’m always here to guide you. You’ve got this! 💪"

def celebrate_success(trade: str) -> str:
    """Celebrate a successful trade."""
    return f"Great job! That {trade} trade worked out perfectly. 🎉 Let’s keep up the momentum!"
