import json
import os
from llamaapi import LlamaAPI


# Initialize the llamaapi with your api_token
llama = LlamaAPI("api_token")


# Define your API request
def finalTerminalCommand():
    Query = input("Enter your query: ")
    Query = Query + ". Platform:" + os.name

    api_request_json = {
                "messages": [
                    {
                        "role": "system",
                        "content": """You are a computer expert. You want to
                        respond to prompts with the commands required to
                        complete the task. You are given a prompt with a task.
                        You must respond with the command to complete the task.
                        """
                    },
                    {
                        "role": "user",
                        "content": Query
                    }
                ],
                "functions": [
                    {
                        "name": "find_terminal_command",
                        "description": """Get the command to execute a terminal
                        function. Return the command and any other arguments
                        that may be needed to fulfil the command.""",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "action": {
                                    "title": "action",
                                    "type": "string",
                                    "description": """The name of the command
                                    to execute on the platform, including any
                                    flags if necessary"""
                                },
                                "target": {
                                    "title": "target",
                                    "type": "string",
                                    "description": """Any required parameters
                                    for the action to be performed
                                    successfully, and according to the prompt
                                    """
                                },
                                "platform": {
                                    "title": "platform",
                                    "type": "string",
                                    "description": """The platform that is used
                                    to determine the command, e.g. Windows
                                    , mac , Linux ,or the operating system
                                    that the command runs on. It should be
                                    found from the query."""
                                }
                            }
                        },
                        "required": [
                            "action",
                            "target",
                            "platform"
                        ]
                    }
                ],
                "temperature": 1.0,
                "stream": False,
                "function_call": {"name": "find_terminal_command"}
            }

    # Make your request and handle the response
    response = llama.run(api_request_json)
    print(json.dumps(response.json(), indent=2))
    args = response.json()["choices"][0]["message"]["function_call"]
    return args["arguments"]


while True:
    command = finalTerminalCommand()

    # Execute the command
    if command["target"] != "":
        os.system(command["action"] + " " + command["target"])
    else:
        os.system(command["action"])
