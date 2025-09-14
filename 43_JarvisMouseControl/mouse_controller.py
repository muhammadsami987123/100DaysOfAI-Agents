"""
Mouse controller for JarvisMouseControl
Handles all mouse automation using pyautogui
"""

import pyautogui
import time
from typing import Dict, Any, Optional, Tuple
from config import CONFIG

class MouseController:
    """Controls mouse actions using pyautogui"""
    
    def __init__(self):
        """Initialize mouse controller with safety settings"""
        # Configure pyautogui safety settings
        pyautogui.FAILSAFE = CONFIG.ENABLE_SAFETY
        pyautogui.PAUSE = CONFIG.CLICK_DELAY
        
        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Update safety bounds with actual screen size
        CONFIG.SAFETY_BOUNDS["max_x"] = self.screen_width
        CONFIG.SAFETY_BOUNDS["max_y"] = self.screen_height
        
        print(f"🖥️  Screen detected: {self.screen_width}x{self.screen_height}")
    
    def execute_action(self, action_data: Dict[str, Any]) -> bool:
        """
        Execute a mouse action based on parsed command data
        
        Args:
            action_data: Dictionary containing action details
            
        Returns:
            True if action was executed successfully, False otherwise
        """
        try:
            action = action_data.get("action")
            distance = action_data.get("distance", "medium")
            
            if not action:
                return False
            
            # Get movement distance
            move_distance = CONFIG.MOVE_DISTANCES.get(distance, 100)
            
            # Execute the action
            if action == "move_up":
                return self._move_up(move_distance)
            elif action == "move_down":
                return self._move_down(move_distance)
            elif action == "move_left":
                return self._move_left(move_distance)
            elif action == "move_right":
                return self._move_right(move_distance)
            elif action == "click":
                return self._click()
            elif action == "double_click":
                return self._double_click()
            elif action == "right_click":
                return self._right_click()
            elif action == "scroll_up":
                return self._scroll_up()
            elif action == "scroll_down":
                return self._scroll_down()
            elif action == "drag":
                return self._drag()
            elif action == "stop":
                return self._stop()
            else:
                print(f"❌ Unknown action: {action}")
                return False
                
        except Exception as e:
            print(f"❌ Error executing action: {e}")
            return False
    
    def _move_up(self, distance: int) -> bool:
        """Move mouse cursor up"""
        try:
            current_x, current_y = pyautogui.position()
            new_y = max(0, current_y - distance)
            
            if self._is_safe_position(current_x, new_y):
                pyautogui.moveTo(current_x, new_y, duration=CONFIG.MOUSE_DURATION)
                print(f"🖱️  Moved up {distance}px to ({current_x}, {new_y})")
                return True
            else:
                print("🛑 Safety stop: Position would be outside screen bounds")
                return False
        except Exception as e:
            print(f"❌ Error moving up: {e}")
            return False
    
    def _move_down(self, distance: int) -> bool:
        """Move mouse cursor down"""
        try:
            current_x, current_y = pyautogui.position()
            new_y = min(self.screen_height - 1, current_y + distance)
            
            if self._is_safe_position(current_x, new_y):
                pyautogui.moveTo(current_x, new_y, duration=CONFIG.MOUSE_DURATION)
                print(f"🖱️  Moved down {distance}px to ({current_x}, {new_y})")
                return True
            else:
                print("🛑 Safety stop: Position would be outside screen bounds")
                return False
        except Exception as e:
            print(f"❌ Error moving down: {e}")
            return False
    
    def _move_left(self, distance: int) -> bool:
        """Move mouse cursor left"""
        try:
            current_x, current_y = pyautogui.position()
            new_x = max(0, current_x - distance)
            
            if self._is_safe_position(new_x, current_y):
                pyautogui.moveTo(new_x, current_y, duration=CONFIG.MOUSE_DURATION)
                print(f"🖱️  Moved left {distance}px to ({new_x}, {current_y})")
                return True
            else:
                print("🛑 Safety stop: Position would be outside screen bounds")
                return False
        except Exception as e:
            print(f"❌ Error moving left: {e}")
            return False
    
    def _move_right(self, distance: int) -> bool:
        """Move mouse cursor right"""
        try:
            current_x, current_y = pyautogui.position()
            new_x = min(self.screen_width - 1, current_x + distance)
            
            if self._is_safe_position(new_x, current_y):
                pyautogui.moveTo(new_x, current_y, duration=CONFIG.MOUSE_DURATION)
                print(f"🖱️  Moved right {distance}px to ({new_x}, {current_y})")
                return True
            else:
                print("🛑 Safety stop: Position would be outside screen bounds")
                return False
        except Exception as e:
            print(f"❌ Error moving right: {e}")
            return False
    
    def _click(self) -> bool:
        """Perform left click"""
        try:
            pyautogui.click()
            print("🖱️  Left click executed")
            return True
        except Exception as e:
            print(f"❌ Error clicking: {e}")
            return False
    
    def _double_click(self) -> bool:
        """Perform double click"""
        try:
            pyautogui.doubleClick()
            print("🖱️  Double click executed")
            return True
        except Exception as e:
            print(f"❌ Error double clicking: {e}")
            return False
    
    def _right_click(self) -> bool:
        """Perform right click"""
        try:
            pyautogui.rightClick()
            print("🖱️  Right click executed")
            return True
        except Exception as e:
            print(f"❌ Error right clicking: {e}")
            return False
    
    def _scroll_up(self) -> bool:
        """Scroll up"""
        try:
            pyautogui.scroll(CONFIG.SCROLL_AMOUNT)
            print(f"🖱️  Scrolled up {CONFIG.SCROLL_AMOUNT} units")
            return True
        except Exception as e:
            print(f"❌ Error scrolling up: {e}")
            return False
    
    def _scroll_down(self) -> bool:
        """Scroll down"""
        try:
            pyautogui.scroll(-CONFIG.SCROLL_AMOUNT)
            print(f"🖱️  Scrolled down {CONFIG.SCROLL_AMOUNT} units")
            return True
        except Exception as e:
            print(f"❌ Error scrolling down: {e}")
            return False
    
    def _drag(self) -> bool:
        """Perform drag and drop (simplified version)"""
        try:
            # Get current position
            start_x, start_y = pyautogui.position()
            
            # Move a small distance and drag
            end_x = start_x + 50
            end_y = start_y + 50
            
            # Ensure end position is within bounds
            end_x = min(end_x, self.screen_width - 1)
            end_y = min(end_y, self.screen_height - 1)
            
            if self._is_safe_position(end_x, end_y):
                pyautogui.dragTo(end_x, end_y, duration=CONFIG.MOUSE_DURATION)
                print(f"🖱️  Drag executed from ({start_x}, {start_y}) to ({end_x}, {end_y})")
                return True
            else:
                print("🛑 Safety stop: Drag end position would be outside screen bounds")
                return False
        except Exception as e:
            print(f"❌ Error dragging: {e}")
            return False
    
    def _stop(self) -> bool:
        """Stop/quit action"""
        print("🛑 Stop command received")
        return True
    
    def _is_safe_position(self, x: int, y: int) -> bool:
        """Check if position is within safe bounds"""
        if not CONFIG.ENABLE_SAFETY:
            return True
        
        bounds = CONFIG.SAFETY_BOUNDS
        # Add small margin to prevent edge cases
        margin = 10
        return (bounds["min_x"] + margin <= x <= bounds["max_x"] - margin and 
                bounds["min_y"] + margin <= y <= bounds["max_y"] - margin)
    
    def get_current_position(self) -> Tuple[int, int]:
        """Get current mouse position"""
        return pyautogui.position()
    
    def move_to_position(self, x: int, y: int) -> bool:
        """Move mouse to specific position"""
        try:
            if self._is_safe_position(x, y):
                pyautogui.moveTo(x, y, duration=CONFIG.MOUSE_DURATION)
                print(f"🖱️  Moved to position ({x}, {y})")
                return True
            else:
                print("🛑 Safety stop: Position is outside screen bounds")
                return False
        except Exception as e:
            print(f"❌ Error moving to position: {e}")
            return False
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen dimensions"""
        return self.screen_width, self.screen_height
    
    def enable_failsafe(self, enabled: bool = True):
        """Enable or disable pyautogui failsafe"""
        pyautogui.FAILSAFE = enabled
        print(f"🛡️  Failsafe {'enabled' if enabled else 'disabled'}")
    
    def set_mouse_speed(self, speed: float):
        """Set mouse movement speed"""
        CONFIG.MOUSE_SPEED = speed
        print(f"⚡ Mouse speed set to {speed}")
    
    def set_click_delay(self, delay: float):
        """Set delay between clicks"""
        CONFIG.CLICK_DELAY = delay
        pyautogui.PAUSE = delay
        print(f"⏱️  Click delay set to {delay}s")
