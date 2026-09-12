import pyttsx3
import threading
import queue
import logging

logger = logging.getLogger("ASTRA-HAR.VoiceEngine")

class OfflineTTSEngine:
    """
    Offline Text-to-Speech Voice Engine using pyttsx3.
    Processes audio prompts asynchronously on a background worker thread.
    """

    def __init__(self, rate=160, volume=1.0):
        self.rate = rate
        self.volume = volume
        self.queue = queue.Queue()
        self.is_running = True

        self.worker_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.worker_thread.start()

    def speak(self, text: str):
        """Enqueue spoken voice message."""
        if not text:
            return
        self.queue.put(text)

    def guidance(self, text: str):
        self.speak(text)

    def warning(self, text: str):
        self.speak(f"Warning! {text}")

    def success(self, text: str):
        self.speak(text)

    def _speech_worker(self):
        """Background thread handling TTS synthesis."""
        engine = None
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", self.rate)
            engine.setProperty("volume", self.volume)
        except Exception as e:
            logger.warning(f"Failed to initialize pyttsx3 engine ({e}). Voice outputs will be muted.")

        while self.is_running:
            try:
                text = self.queue.get(timeout=0.5)
                if engine is not None:
                    engine.say(text)
                    engine.runAndWait()
                else:
                    logger.info(f"[VOICE MUTE]: {text}")
                self.queue.task_done()
            except queue.Empty:
                pass
            except Exception as e:
                logger.error(f"Error in TTS speech worker: {e}")

offline_tts = OfflineTTSEngine()
