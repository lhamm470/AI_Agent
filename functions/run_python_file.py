import subprocess
import os
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file and returns the STDOUT and STDERR content or error messages if there is an error, and contains optional args arguments as additional commands",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path for a file, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script"
            ),
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        completed_process = subprocess.run(
            command, 
            cwd=working_dir_abs, 
            capture_output=True, 
            text=True, 
            timeout=30
        )

        result_string = ""
        if completed_process.returncode != 0:
            result_string += f'Process exited with code {completed_process.returncode}'
        if not completed_process.stdout and not completed_process.stderr:
            result_string += "No output produced"
            return result_string
        result_string += f'STDOUT:{completed_process.stdout}'
        result_string += f'STDERR:{completed_process.stderr}'
        return result_string
    except(Exception) as e:
        return f"Error: executing Python file: {e}"
    