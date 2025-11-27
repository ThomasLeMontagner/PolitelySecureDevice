from __future__ import annotations

"""Utilities for generating spoken messages."""

import pyttsx3

from pyttsx3.engine import Engine


class VoiceGenerator:
    """Generate spoken greetings using pyttsx3."""

    def __init__(self, engine: Engine | None = None) -> None:
        """Initialize the voice generator."""
        self.engine: Engine = engine or pyttsx3.init()

    def greet(self, name: str) -> None:
        """Speak a greeting to the provided person."""
        self.engine.say(f"Hello, {name}")
        self.engine.runAndWait()
