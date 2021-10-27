"""
Adapter module.
"""

class AnAdapter:
    def __init__(self, message: str):
        self.message = message
        
    def speak(self):
        print(self.message)