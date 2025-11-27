"""Facial recognition package for PolitelySecureDevice."""

from __future__ import annotations

from facial_recognition.alerts import EmailClient
from facial_recognition.capture import capture_headshots
from facial_recognition.recognition import FaceRecognitionEngine
from facial_recognition.speech import VoiceGenerator
from facial_recognition.training import save_encodings, train_model

__all__ = [
    "EmailClient",
    "FaceRecognitionEngine",
    "VoiceGenerator",
    "capture_headshots",
    "save_encodings",
    "train_model",
]
