"""
chatgpt_to_notebook.py

Convert a ChatGPT text response into a Jupyter Notebook (.ipynb)
with proper Markdown and Code cell separation.
"""

import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import re
from pathlib import Path


def chatgpt_response_to_notebook(
    text: str,
    output_path: str = "converted.ipynb",
    notebook_metadata: dict | None = None,
):
    """
    Convert ChatGPT response text into a Jupyter Notebook.

    Parameters
    ----------
    text : str
        Raw ChatGPT response text (copied as-is)
    output_path : str
        Output .ipynb file path
    notebook_metadata : dict, optional
        Metadata for the notebook (kernelspec, language info, etc.)
    """

    cells = []
    lines = text.splitlines()

    in_code_block = False
    code_buffer = []
    markdown_buffer = []
    code_language = None

    code_block_pattern = re.compile(r"^```(\w+)?")

    def flush_markdown():
        if markdown_buffer:
            cells.append(new_markdown_cell("\n".join(markdown_buffer).strip()))
            markdown_buffer.clear()

    def flush_code():
        if code_buffer:
            cell = new_code_cell("\n".join(code_buffer))
            if code_language:
                cell.metadata["language"] = code_language
            cells.append(cell)
            code_buffer.clear()

    for line in lines:
        code_match = code_block_pattern.match(line)

        # Start or end code block
        if code_match:
            if not in_code_block:
                flush_markdown()
                in_code_block = True
                code_language = code_match.group(1)
            else:
                flush_code()
                in_code_block = False
                code_language = None
            continue

        if in_code_block:
            code_buffer.append(line)
        else:
            markdown_buffer.append(line)

    # Flush remaining content
    flush_markdown()
    flush_code()

    nb = new_notebook(
        cells=cells,
        metadata=notebook_metadata or {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.x",
            },
        },
    )

    output_path = Path(output_path).resolve()
    nbformat.write(nb, output_path)

    return output_path


# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    filepath = Path(__file__).parent / "chatgpt_response.txt"
    with open(filepath, "r", encoding="utf-8") as f:
        response_text = f.read()

    outputpath = Path(__file__).parent / "converted.ipynb"
    notebook_path = chatgpt_response_to_notebook(
        response_text
    )

    print(f"Notebook created at: {notebook_path}")
