# agent_10.py - ScreenshotTakerAgent

import mss
import mss.tools
import datetime
import os

class ScreenshotTakerAgent:
    def take_screenshot(self, filename=None):
        try:
            with mss.mss() as sct:
                # Get information of monitor 1
                monitor = sct.monitors[1]

                # The screen part to capture
                monitor = {
                    "top": monitor["top"],
                    "left": monitor["left"],
                    "width": monitor["width"],
                    "height": monitor["height"],
                }
                
                if filename is None:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"screenshot_{timestamp}.png"
                
                output_path = os.path.join(os.getcwd(), filename)
                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_path)
                
                return f"Screenshot saved to {output_path}"
        except Exception as e:
            return f"An error occurred while taking screenshot: {e}"
