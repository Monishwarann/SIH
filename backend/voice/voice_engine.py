import time
import threading
import queue
import logging

logger = logging.getLogger("ASTRA-HAR.VoiceAlertManager")

class VoiceAlertManager:
    """Offline Voice Alert Engine with priority queueing and cooldown logic."""

    def __init__(self, cooldown_sec: float = 3.0):
        self.cooldown_sec = cooldown_sec
        self.last_spoken_time = 0.0
        self.last_message = ""
        self.msg_queue = queue.Queue()
        self.engine = None
        self.is_running = True

        # Initialize pyttsx3 in worker thread
        self._thread = threading.Thread(target=self._speech_worker, daemon=True)
        self._thread.start()

    def _speech_worker(self):
        """Worker thread executing TTS synthesis asynchronously."""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", 150)
            self.engine.setProperty("volume", 1.0)
        except Exception as e:
            logger.warning(f"pyttsx3 TTS initialization warning: {e}. Voice synthesis fallback active.")

        while self.is_running:
            try:
                msg = self.msg_queue.get(timeout=0.5)
                if msg:
                    logger.info(f"VOICE SPEAKING: '{msg}'")
                    if self.engine:
                        try:
                            self.engine.say(msg)
                            self.engine.runAndWait()
                        except Exception as ex:
                            logger.error(f"TTS synthesis error: {ex}")
            except queue.Empty:
                pass

    def speak(self, message: str, force: bool = False):
        """Queue message for speaking if cooldown period has elapsed."""
        now = time.time()
        if force or (now - self.last_spoken_time >= self.cooldown_sec and message != self.last_message):
            self.last_spoken_time = now
            self.last_message = message
            self.msg_queue.put(message)

    def warning(self, message: str):
        self.speak(f"Warning. {message}", force=True)

    def guidance(self, message: str):
        self.speak(message, force=False)

    def success(self, message: str):
        self.speak(message, force=True)

# Global voice manager instance
voice_manager = VoiceAlertManager()
