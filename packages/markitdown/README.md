# MarkItDown

> [!IMPORTANT]
> MarkItDown is a Python package and command-line utility for converting various files to Markdown (e.g., for indexing, text analysis, etc). 
>
> For more information, and full documentation, see the project [README.md](https://github.com/microsoft/markitdown) on GitHub.

## Installation

From PyPI:

```bash
pip install markitdown[all]
```

From source:

```bash
git clone git@github.com:microsoft/markitdown.git
cd markitdown
pip install -e packages/markitdown[all]
```

## Usage

### Command-Line

```bash
markitdown path-to-file.pdf > document.md
```

### Python API

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("test.xlsx")
print(result.text_content)
```

### More Information

For more information, and full documentation, see the project [README.md](https://github.com/microsoft/markitdown) on GitHub.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.

### Audio transcription providers

Without a transcription client, audio transcription uses Google Speech Recognition.
When an `llm_client` with an audio transcription API is supplied, recordings are sent
to that client only; authentication, network, and client errors do not trigger a
fallback to Google. The result uses the generic `Audio Transcript` heading.
