# OpenAI API Specification Processor

This repository contains a Python script (`process_openai_spec.py`) designed to fetch, parse, and organize various sections of the OpenAI OpenAPI Specification.

## Features

The `process_openai_spec.py` script performs the following operations:

1.  **Fetch OpenAPI Specification**: Downloads the latest OpenAPI specification from the official OpenAI GitHub repository and saves it as `openai-api-spec.yaml`.
2.  **Extract Paths**: Parses the `openai-api-spec.yaml` file and extracts each individual API path. Each path is then saved as a separate YAML file within a `paths/` directory. Forward slashes in the path names are replaced with underscores for valid filenames.
3.  **Extract Schemas**: Extracts all schema definitions from the `components/schemas` section of the OpenAPI specification. Each schema is saved as a separate YAML file within a `schemas/` directory.
4.  **Extract Groups**: Extracts the `x-oaiMeta/groups` information, which defines logical groupings of API endpoints and related documentation. It creates a `groups/` directory, then creates subdirectories for each `navigationGroup` (e.g., `responses`, `chat`, `assistants`), and finally saves each group's definition as a YAML file within its respective `navigationGroup` directory.

## How to Use

1.  **Prerequisites**:
    *   Python 3.x installed
    *   `PyYAML` and `requests` libraries. If you don't have them, you can install them using pip:
        ```bash
        pip install PyYAML requests
        ```

2.  **Run the Script**:
    Execute the `process_openai_spec.py` script from your terminal:
    ```bash
    python process_openai_spec.py
    ```

## Output Structure

After running the script, the following directory structure will be created in your project:

```
.
├── openai-api-spec.yaml
├── paths/
│   ├── assistants.yaml
│   ├── assistants_{assistant_id}.yaml
│   ├── audio_speech.yaml
│   └── ... (and many more path files)
├── schemas/
│   ├── AddUploadPartRequest.yaml
│   ├── AdminApiKey.yaml
│   ├── AssistantObject.yaml
│   └── ... (and many more schema files)
└── groups/
    ├── responses/
    │   ├── responses.yaml
    │   └── responses-streaming.yaml
    ├── chat/
    │   ├── chat.yaml
    │   └── chat-streaming.yaml
    ├── realtime/
    │   ├── realtime.yaml
    │   └── ...
    └── ... (and other navigation group directories)