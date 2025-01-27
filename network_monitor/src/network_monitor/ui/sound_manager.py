import os
import logging

# Try to import sound dependencies, fallback gracefully if not available
SOUND_AVAILABLE = False
try:
    from PyQt6.QtMultimedia import QSoundEffect
    from PyQt6.QtCore import QUrl
    SOUND_AVAILABLE = True
except ImportError:
    logging.warning("Sound system not available - continuing without audio support")

class SoundManager:
    """Manages sound notifications for the network monitor application"""
    
    def __init__(self, sound_dir: str = "sounds"):
        """Initialize the sound manager"""
        self.sound_dir = os.path.abspath(sound_dir)
        self.sounds = {}
        self.sound_enabled = True
        self._init_sounds()
    
    def _init_sounds(self):
        """Initialize sound effects"""
        if not SOUND_AVAILABLE:
            logging.warning("Sound system not available - continuing without audio support")
            self.sound_enabled = False
            return
            
        # Check if we're in a headless environment
        if os.environ.get('QT_QPA_PLATFORM') == 'offscreen':
            logging.warning("Running in headless mode - sound notifications disabled")
            self.sound_enabled = False
            return
            
        try:
            # Create sounds directory if it doesn't exist
            os.makedirs(self.sound_dir, exist_ok=True)
            
            # Define sound effects
            sound_files = {
                'device_offline': 'device_offline.wav',
                'network_storm': 'network_storm.wav',
                'alert': 'alert.wav'
            }
            
            # Load sound effects
            for sound_id, filename in sound_files.items():
                sound_path = os.path.join(self.sound_dir, filename)
                
                if not os.path.exists(sound_path):
                    logging.warning(f"Sound file not found: {sound_path}")
                    continue
                    
                try:
                    # Create QSoundEffect for each sound
                    sound = QSoundEffect()
                    sound.setSource(QUrl.fromLocalFile(sound_path))
                    sound.setVolume(0.5)  # Set volume to 50%
                    
                    if not sound.isLoaded():
                        logging.warning(f"Failed to load sound: {sound_path}")
                        continue
                        
                    self.sounds[sound_id] = sound
                except Exception as e:
                    logging.error(f"Error initializing sound {filename}: {str(e)}")
                    continue
                    
        except Exception as e:
            logging.error(f"Error initializing sound system: {str(e)}")
            self.sound_enabled = False
    
    def play_sound(self, sound_id: str):
        """Play a sound effect by ID"""
        if not self.sound_enabled:
            return
            
        try:
            if sound_id in self.sounds:
                sound = self.sounds[sound_id]
                if sound.isLoaded() and not sound.isPlaying():
                    sound.play()
        except Exception as e:
            logging.error(f"Error playing sound {sound_id}: {str(e)}")
            # Disable sound system if we encounter playback errors
            self.sound_enabled = False
    
    def set_volume(self, volume: float):
        """Set volume for all sounds (0.0 to 1.0)"""
        for sound in self.sounds.values():
            sound.setVolume(volume)
    
    def stop_all(self):
        """Stop all playing sounds"""
        for sound in self.sounds.values():
            if sound.isPlaying():
                sound.stop()
