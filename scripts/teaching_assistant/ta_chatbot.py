#!/usr/bin/env python3
"""
Teaching Assistant Chatbot

This script provides a simple chatbot interface to interact with the teaching assistant
data using OpenRouter API for LLM responses.
"""

import argparse
import json
import os
import sys
import requests
from typing import Dict, List, Any, Optional
import teaching_assistant as ta

class TeachingAssistantChatbot:
    def __init__(self, api_key: str, model: str = "openai/gpt-3.5-turbo",
                 assessment_data_path: str = "assets/student_data.json",
                 resource_time_data_path: str = "assets/resource_time.json",
                 study_history_data_path: str = "assets/study_history.json"):
        """
        Initialize the Teaching Assistant Chatbot.
        
        Args:
            api_key: OpenRouter API key
            model: Model to use for responses (default: openai/gpt-3.5-turbo)
            assessment_data_path: Path to student assessment data JSON file
            resource_time_data_path: Path to resource time data JSON file
            study_history_data_path: Path to study history data JSON file
        """
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        
        self.assistant = ta.TeachingAssistant(
            assessment_data_path=assessment_data_path,
            resource_time_data_path=resource_time_data_path,
            study_history_data_path=study_history_data_path
        )
        self.context = self._build_initial_context()
        
    def _build_initial_context(self) -> Dict[str, Any]:
        """Build initial context with class data for the LLM."""
        # Get at-risk students (just names and completion percentages)
        at_risk_students = self.assistant.identify_at_risk_students()
        simplified_at_risk = [
            {
                "name": student["name"],
                "completion_percentage": student["completion_percentage"],
                "labs_completed": student["labs_completed"],
                "total_labs": student["total_labs"]
            }
            for student in at_risk_students
        ]
        
        # Get simplified module progress for all modules
        module_progress = {}
        for module in range(1, 7):
            module_data = self.assistant.get_module_progress(module)
            # Simplify student data to reduce context size
            simplified_students = [
                {
                    "name": student["name"],
                    "completion_percentage": student["completion_percentage"],
                    "labs_completed": student["labs_completed"],
                    "total_labs": student["total_labs"]
                }
                for student in module_data["students"][:5]  # Only include top 5 students
            ]
            
            module_progress[f"module_{module}"] = {
                "average_completion": module_data["average_completion"],
                "average_assessment_score": module_data["average_assessment_score"],
                "top_students": simplified_students
            }
        
        # Build context
        return {
            "at_risk_students": simplified_at_risk,
            "module_progress": module_progress,
            "class_size": len(self.assistant.assessment_data.get("students", [])),
            "current_date": "2025-04-28"  # Hardcoded for now, could use datetime
        }
    
    def get_student_data(self, student_name: str) -> Dict[str, Any]:
        """Get detailed data for a specific student."""
        return self.assistant.get_student_insights(student_name)
    
    def query_llm(self, prompt: str, student_context: Optional[Dict[str, Any]] = None) -> str:
        """
        Query the LLM through OpenRouter API.
        
        Args:
            prompt: User's question
            student_context: Optional context for a specific student
            
        Returns:
            LLM response as a string
        """
        # Build the full context
        full_context = self.context.copy()
        if student_context:
            full_context["student_data"] = student_context
        
        # Construct the system message
        system_message = """You are a helpful teaching assistant chatbot. You have access to student data including:
- At-risk students
- Module progress for all modules
- Individual student insights

Answer questions about student progress, provide recommendations, and help identify students who need attention.
Base your answers only on the data provided in the context. If you don't have enough information, say so.
Keep responses concise and focused on helping instructors support their students effectively.
"""

        # Construct the messages for the API
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Here is the context data: {json.dumps(full_context, default=str)}"},
            {"role": "user", "content": prompt}
        ]
        
        # Make the API request
        try:
            print("Sending request to OpenRouter API...")
            
            # Print request details for debugging
            request_data = {
                "model": self.model,
                "messages": messages
            }
            print(f"Request URL: {self.base_url}/chat/completions")
            print(f"Request Model: {self.model}")
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=request_data
            )
            
            print(f"Response Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("Response received successfully")
                print(f"Response JSON: {json.dumps(result, indent=2)}")
                
                # Extract the content from the response
                if "choices" in result and len(result["choices"]) > 0:
                    message = result["choices"][0].get("message", {})
                    content = message.get("content", "No content in response")
                    return content
                else:
                    print("No choices in response")
                    return "No response content available"
            else:
                print(f"Error Response: {response.text}")
                return f"Error: {response.status_code} - {response.text}"
        
        except Exception as e:
            print(f"Exception: {str(e)}")
            return f"Error connecting to OpenRouter: {str(e)}"
    
    def chat_loop(self):
        """Run the interactive chat loop."""
        print("Teaching Assistant Chatbot")
        print("Type 'exit' or 'quit' to end the conversation")
        print("Type 'student: [name]' to focus on a specific student")
        print("Type 'help' for more commands")
        print()
        
        current_student = None
        student_data = None
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            elif user_input.lower() == "help":
                print("\nCommands:")
                print("  student: [name] - Focus on a specific student")
                print("  at-risk - List at-risk students")
                print("  module: [number] - Get info about a specific module")
                print("  clear - Clear the current student focus")
                print("  exit/quit - End the conversation")
                print()
                continue
                
            elif user_input.lower() == "at-risk":
                at_risk = self.assistant.identify_at_risk_students()
                print("\nAt-risk students:")
                for student in at_risk:
                    print(f"  - {student['name']} ({student['completion_percentage']:.1f}% completion)")
                print()
                continue
                
            elif user_input.lower() == "clear":
                current_student = None
                student_data = None
                print("Student focus cleared.")
                continue
                
            elif user_input.lower().startswith("module:"):
                try:
                    module_num = int(user_input.split(":", 1)[1].strip())
                    if 1 <= module_num <= 6:
                        module_data = self.assistant.get_module_progress(module_num)
                        print(f"\nModule {module_num} Progress:")
                        print(f"Average Completion: {module_data['average_completion']:.1f}%")
                        print(f"Average Assessment Score: {module_data['average_assessment_score']:.1f}%")
                        print(f"Top 3 Students:")
                        for i, student in enumerate(module_data['students'][:3]):
                            print(f"  {i+1}. {student['name']} - {student['completion_percentage']:.1f}%")
                        print()
                    else:
                        print("Module number must be between 1 and 6")
                except (ValueError, IndexError):
                    print("Invalid module format. Use 'module: [number]'")
                continue
                
            elif user_input.lower().startswith("student:"):
                student_name = user_input.split(":", 1)[1].strip()
                try:
                    student_data = self.get_student_data(student_name)
                    current_student = student_name
                    print(f"\nFocused on student: {student_name}")
                    print(f"Completion: {student_data['overall_completion']:.1f}%")
                    print(f"Assessment Average: {student_data['average_assessment_score']:.1f}%")
                    print()
                except Exception as e:
                    print(f"Error finding student: {str(e)}")
                continue
            
            # Process the query with the LLM
            response = self.query_llm(user_input, student_data)
            print(f"\nAssistant: {response}\n")


def main():
    parser = argparse.ArgumentParser(description="Teaching Assistant Chatbot")
    parser.add_argument("--api-key", help="OpenRouter API key")
    parser.add_argument("--model", default="openai/gpt-3.5-turbo", 
                        help="Model to use (default: openai/gpt-3.5-turbo)")
    parser.add_argument("--assessment-data", default="assets/student_data.json",
                        help="Path to student assessment data JSON file")
    parser.add_argument("--resource-time-data", default="assets/resource_time.json",
                        help="Path to resource time data JSON file")
    parser.add_argument("--study-history-data", default="assets/study_history.json",
                        help="Path to study history data JSON file")
    parser.add_argument("--query", help="Single query to process instead of interactive mode")
    parser.add_argument("--student", help="Student to focus on for the query")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    args = parser.parse_args()
    
    # Get API key from args or environment variable
    api_key = args.api_key or os.environ.get("OPENROUTER_API_KEY")
    
    if not api_key:
        print("Error: OpenRouter API key is required.")
        print("Either provide it with --api-key or set the OPENROUTER_API_KEY environment variable.")
        sys.exit(1)
    
    chatbot = TeachingAssistantChatbot(api_key, args.model,
                                       assessment_data_path=args.assessment_data,
                                       resource_time_data_path=args.resource_time_data,
                                       study_history_data_path=args.study_history_data)
    
    if args.interactive:
        # Run in interactive mode
        chatbot.chat_loop()
    elif args.query:
        # Process a single query
        student_data = None
        if args.student:
            try:
                student_data = chatbot.get_student_data(args.student)
                print(f"Focused on student: {args.student}")
            except Exception as e:
                print(f"Error finding student: {str(e)}")
        
        # Process the query with the LLM
        response = chatbot.query_llm(args.query, student_data)
        print(f"\nQuery: {args.query}")
        print(f"\nResponse: {response}\n")
    else:
        # No query or interactive mode specified
        print("Error: Either --query or --interactive must be specified.")
        print("Use --query 'your question' for a single question")
        print("Use --interactive for interactive chat mode")
        sys.exit(1)


if __name__ == "__main__":
    main()
