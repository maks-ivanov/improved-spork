from typing import List, Optional

from langchain.agents import Tool

from ..utils import PassThroughBuffer
from .python_writer import PythonWriter


class PythonWriterToolBuilder:
    def __init__(self, python_writer: PythonWriter, logger: Optional[PassThroughBuffer] = None):
        """
        Initializes a PythonWriterToolBuilder PythonObjectType with the given inputs.

        Args:
        - python_writer (PythonWriter): A PythonWriter PythonObjectType representing the code writer to work with.
        - logger (Optional[PassThroughBuffer]): An optional PassThroughBuffer PythonObjectType to log output.

        Returns:
        - None
        """
        self.python_writer = python_writer
        self.logger = logger

    def python_writer_wrapper(self, input_str) -> str:
        path = input_str.split(",")[0]
        code = ",".join(input_str.split(",")[1:]).strip()

        self.python_writer.modify_code_state(
            *(
                path,
                code,
            )
        )
        return "Success"

    def build_tools(self) -> List[Tool]:
        """
        Builds a list of Tool PythonObjects for interacting with PythonWriter.

        Args:
        - None

        Returns:
        - tools (List[Tool]): A list of Tool PythonObjects representing PythonWriter commands.
        """
        tools = [
            Tool(
                name="python-writer-modify-code-state",
                func=lambda python_path_comma_code_str: self.python_writer_wrapper(
                    python_path_comma_code_str
                ),
                description=f"Modifies the code state in memory by taking a python_path and raw-text code as input."
                f" If the specified function, class, or module does not exist, it creates a new one and updates the in-memory code to reflect this change."
                f" If it already exists, it modifies the existing code."
                f" For Example:"
                f'Suppose you wish to a new function named "my_function" of "my_class" is defined in the file "my_file.py" that lives in "my_folder"'
                f" Then, the correct function call is "
                f'python-writer-modify-code-state(my_folder.my_file.my_class.my_function, def my_function() -> None:\n   """My Function"""\n    print("hello world")'
                f" If new import statements are necessary, then append them to the top of the input string.",
                return_direct=True,
            ),
            Tool(
                name="python-writer-write-to-disk",
                func=lambda: self.python_writer.write_to_disk(),
                description=f"Writes all the latest modifications in the code state to disk."
                f" New files are created when necessary.",
                return_direct=True,
            ),
        ]
        return tools