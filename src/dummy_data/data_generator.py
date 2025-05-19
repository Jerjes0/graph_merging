import json
import google.generativeai as genai
from typing import Dict, Any, Optional

class DataGenerator:
    def __init__(self, api_key: str):
        """
        Initialize the DataGenerator with a Google Gemini API key.
        
        Args:
            api_key (str): Google Gemini API key
        """
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Initialize the model with safety settings
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
        
        self.model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
    def generate_graph(self, query: str, depth: int = 10) -> Dict[str, Dict[str, Any]]:
        """
        Generate a causal graph using the Gemini API based on the user's query.
        
        Args:
            query (str): The user's query to generate the graph
            depth (int, optional): Maximum depth of the graph. Defaults to 10.
            
        Returns:
            Dict[str, Dict[str, Any]]: The generated graph as a dictionary
        """
        prompt = f"""
        You are a causal graph generator. Your task is to generate a causal graph based on the following query:
        "{query}"
        
        The graph should have a maximum depth of {depth} levels.
        
        IMPORTANT: Your response must be ONLY a valid Python dictionary string in the following format, with no additional text or explanation:
        {{
            "node1": {{
                "children": ["node2", "node3"],
                "description": "Description of node1"
            }},
            "node2": {{
                "children": ["node4"],
                "description": "Description of node2"
            }}
        }}
        
        Rules:
        1. Each node must have exactly two keys: "children" and "description"
        2. "children" must be a list of strings (node names)
        3. "description" must be a string
        4. The response must be a valid Python dictionary that can be parsed by json.loads()
        5. Do not include any explanatory text before or after the dictionary
        6. Use double quotes for all strings
        7. Do not include markdown code block markers (```) in your response
        """
        
        try:
            response = self.model.generate_content(prompt)
            graph_str = response.text
            
            # Print the raw response for debugging
            # print("Raw response from model:")
            # print(graph_str)
            # print("\nAttempting to parse response...")
            
            # Clean the response string to ensure it's a valid JSON
            graph_str = graph_str.strip()
            
            # Remove markdown code block markers if present
            if graph_str.startswith('```'):
                # Find the first newline after the opening ```
                first_newline = graph_str.find('\n')
                if first_newline != -1:
                    # Remove the opening ``` and any language specifier
                    graph_str = graph_str[first_newline:].strip()
            
            # Remove closing ``` if present
            if graph_str.endswith('```'):
                graph_str = graph_str[:-3].strip()
            
            return self._parse_graph_string(graph_str)
        except Exception as e:
            print(f"Error generating graph: {str(e)}")
            raise
    
    def _parse_graph_string(self, graph_str: str) -> Dict[str, Dict[str, Any]]:
        """
        Parse a string representation of a graph into a dictionary.
        
        Args:
            graph_str (str): String representation of the graph
            
        Returns:
            Dict[str, Dict[str, Any]]: Parsed graph dictionary
        """
        try:
            # First try to parse as JSON
            return json.loads(graph_str)
        except json.JSONDecodeError as e:
            print(f"JSON parsing failed: {str(e)}")
            print("Attempting to evaluate as Python literal...")
            try:
                return eval(graph_str)
            except Exception as e:
                print(f"Python literal evaluation failed: {str(e)}")
                raise ValueError(f"Failed to parse graph string: {str(e)}")
    
    def save_graph(self, graph: Dict[str, Dict[str, Any]], path: str, name: str) -> None:
        """
        Save the generated graph to a JSON file.
        
        Args:
            graph (Dict[str, Dict[str, Any]]): The graph to save
            path (str): Directory path where to save the file
            name (str): Name of the file (without extension)
        """
        import os
        
        # Create directory if it doesn't exist
        os.makedirs(path, exist_ok=True)
        
        # Construct full file path
        file_path = os.path.join(path, f"{name}.json")
        
        # Save graph to file
        with open(file_path, 'w') as f:
            json.dump(graph, f, indent=4) 