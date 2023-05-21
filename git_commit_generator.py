"""
Git Commit Generator
This script generates random git commits with random messages between specified dates.
"""

import random
import datetime
import subprocess
from typing import List, Tuple

class GitCommitGenerator:
    def __init__(self):
        # List of common commit message templates
        self.commit_templates = [
            "Update {file} with {action}",
            "Fix {issue} in {component}",
            "Add {feature} to {component}",
            "Refactor {component} for better {quality}",
            "Optimize {component} performance",
            "Implement {feature} in {component}",
            "Fix bug in {component}",
            "Update documentation for {component}",
            "Add tests for {component}",
            "Clean up {component} code"
        ]
        
        # Components and features for random generation
        self.components = [
            "database", "API", "frontend", "backend", "authentication",
            "user interface", "data processing", "file handling",
            "error handling", "logging system"
        ]
        
        self.actions = [
            "improvements", "bug fixes", "new features", "optimizations",
            "refactoring", "updates", "enhancements", "modifications"
        ]
        
        self.issues = [
            "performance issue", "memory leak", "race condition",
            "null pointer", "type error", "validation error"
        ]
        
        self.features = [
            "user authentication", "data validation", "error handling",
            "logging", "caching", "search functionality", "filtering"
        ]
        
        self.qualities = [
            "readability", "maintainability", "scalability",
            "reliability", "efficiency", "security"
        ]
        
        self.files = [
            "main.py", "config.py", "utils.py", "models.py",
            "views.py", "database.py", "api.py", "tests.py"
        ]

    def generate_commit_message(self) -> str:
        """Generate a random commit message using templates and random components."""
        template = random.choice(self.commit_templates)
        
        # Replace placeholders with random values
        message = template.format(
            file=random.choice(self.files),
            action=random.choice(self.actions),
            issue=random.choice(self.issues),
            component=random.choice(self.components),
            feature=random.choice(self.features),
            quality=random.choice(self.qualities)
        )
        
        return message

    def generate_random_date(self, start_date: datetime.datetime, end_date: datetime.datetime) -> datetime.datetime:
        """Generate a random datetime between start_date and end_date."""
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_days)
        return random_date

    def create_commit(self, date: datetime.datetime, message: str) -> bool:
        """Create a git commit with the specified date and message."""
        try:
            # Set the git commit date
            date_str = date.strftime("%Y-%m-%d %H:%M:%S")
            env = {
                "GIT_AUTHOR_DATE": date_str,
                "GIT_COMMITTER_DATE": date_str
            }
            
            # Create an empty commit with the message
            subprocess.run(
                ["git", "commit", "--allow-empty", "-m", message],
                env=env,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error creating commit: {e}")
            return False

    def generate_commits(self, start_date: str, end_date: str, num_commits: int) -> None:
        """
        Generate random commits between start_date and end_date.
        
        Args:
            start_date (str): Start date in format 'YYYY-MM-DD'
            end_date (str): End date in format 'YYYY-MM-DD'
            num_commits (int): Number of commits to generate
        """
        try:
            # Parse dates
            start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            
            if end < start:
                raise ValueError("End date must be after start date")
            
            # Generate commits
            successful_commits = 0
            for _ in range(num_commits):
                commit_date = self.generate_random_date(start, end)
                commit_message = self.generate_commit_message()
                
                if self.create_commit(commit_date, commit_message):
                    successful_commits += 1
                    print(f"Created commit: {commit_message} on {commit_date.strftime('%Y-%m-%d')}")
            
            print(f"\nSuccessfully created {successful_commits} out of {num_commits} commits")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def main():
    # Create generator instance
    generator = GitCommitGenerator()
    
    # Get user input
    print("Git Commit Generator")
    print("-------------------")
    
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    
    while True:
        try:
            num_commits = int(input("Enter number of commits to generate: "))
            if num_commits > 0:
                break
            print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")
    
    # Generate commits
    generator.generate_commits(start_date, end_date, num_commits)

if __name__ == "__main__":
    main() 