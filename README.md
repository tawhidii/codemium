# Codemium

## Description

This system leverages a Large Language Model (LLM) to take a code repository into its context. It can understand and analyze the repository's structure, code, and documentation, providing accurate and relevant answers to technical questions. Whether you need help understanding a particular function, debugging an issue, or getting insights into the overall architecture, this tool is designed to assist developers in navigating complex codebases efficiently.






## Getting Started

### Dependencies

* Python 3.10 or higher
* Langchain
* FAISS
* Boto3 (for Amazon Web Services)
* streamlit
* Aws bedrock

Please refer to the `requirements.txt` file for a comprehensive list of dependencies.

### Installing

Clone the repository and install the dependencies using pip:

```bash
git clone https://github.com/tawhidii/codemium.git
cd codemium
pip install -r requirements.txt
```
### Project Structure
The project is structured as follows:
```
codemium/
│
├── .DS_Store
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── main.py
│
├── core/
│   ├── __init__.py
│   ├── codemium_engine.py
│   └── __pycache__/
│       ├── __init__.cpython-312.pyc
│       └── codemium_engine.cpython-312.pyc
│
└── utils/
    ├── ui.py
    ├── __init__.py
    └── __pycache__/
        ├── ui.cpython-312.pyc
        └── __init__.cpython-312.pyc
```

### Executing program
Run the main program:

```python
streamlit run main.py

```

