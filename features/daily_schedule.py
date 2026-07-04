import os
import json
import webview
import sys
from datetime import datetime, timedelta

print("daily_schudule.py = True")
class TaskManagerAPI:
    def __init__(self):
        self.file_path = "features/schedul.json"
        self.check_and_reset_friday_tasks()

    def load_tasks(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return {"weekly_tasks": [], "last_reset": ""}

    def save_tasks(self, tasks_data):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(tasks_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False

    def check_and_reset_friday_tasks(self):
        """Calculates if a Friday midnight cycle has passed since the last reset."""
        if not os.path.exists(self.file_path):
            return

        data = self.load_tasks()
        last_reset_str = data.get("last_reset", "")
        now = datetime.now()

        # Target the most recent or upcoming Friday deadline
        # now.weekday() -> Monday is 0, Friday is 4
        days_since_friday = (now.weekday() - 4) % 7
        most_recent_friday = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days_since_friday)

        try:
            last_reset_date = datetime.strptime(last_reset_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            # If no valid reset date exists, establish one without resetting yet
            data["last_reset"] = most_recent_friday.strftime("%Y-%m-%d")
            self.save_tasks(data)
            return

        # If the last recorded reset was BEFORE the most recent Friday midnight checkpoint
        if last_reset_date < most_recent_friday:
            print("System Event: Friday Midnight Purge Triggered. Resetting status metrics...")
            
            # Loop through every day and uncheck completed targets
            for day_entry in data.get("weekly_tasks", []):
                for task in day_entry.get("tasks", []):
                    task["completed"] = False

            # Lock in the new reset completion marker
            data["last_reset"] = most_recent_friday.strftime("%Y-%m-%d")
            self.save_tasks(data)

def schudel__main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir) 
    html_path = os.path.join(root_dir, 'UI', 'schudel.html') 

    api = TaskManagerAPI()

    schedule_window = webview.create_window(
        title='DARIUSH - Matrix Controller',
        url=html_path,
        js_api=api,
        width=1000,
        height=680,
        resizable=True,
        background_color='#1e1d1a'
    )

