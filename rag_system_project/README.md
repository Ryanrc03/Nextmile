# RAG System Project

## Overview
The Retrieval-Augmented Generation (RAG) system is designed to enhance the process of answering questions based on a user's resume. By leveraging a combination of retrieval and generation techniques, the system provides accurate and contextually relevant responses.

## Project Structure
```
rag_system_project
├── rag_core
│   ├── __init__.py
│   ├── rag_core.py
├── tests
│   ├── __init__.py
│   └── test_rag_core.py
├── main.py
├── requirements.txt
└── README.md
```

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd rag_system_project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the RAG system, execute the `main.py` file. This file serves as the entry point for the application and allows for user interaction with the RAG system.

```
python main.py
```

## Testing
Unit tests for the `rag_core` module are located in the `tests` directory. To run the tests, use the following command:

```
pytest tests/test_rag_core.py
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.