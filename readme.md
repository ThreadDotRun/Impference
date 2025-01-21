# Llama Flask Interface

A Flask web application that provides a user interface for working with Llama language models. This application allows users to select different models, prompts, and parameters to generate text using the Llama.cpp implementation.

## Features

- Web-based interface for Llama model interaction
- Support for multiple models
- Configurable parameters:
  - Context size
  - Batch size
  - Number of tokens
  - Temperature
  - Repeat penalty
- Custom prompt management
- Real-time text generation
- Special character handling

## Prerequisites

- Python 3.x
- Flask
- Llama.cpp compiled with the `main` executable
- Sufficient disk space for model storage

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install the required Python packages:
```bash
pip install flask
```

3. Set up the required directory structure:
```
├── models
│   └── xtra_models/
├── prompts/
├── context_size/
├── num_tokens/
├── temperatures/
└── creds.txt
```

4. Place your Llama models in the `models/xtra_models/` directory

## Directory Structure

The application expects the following directory structure for configuration:

- `temperatures/`: Temperature parameter files (e.g., `0.05.temp`, `0.3.temp`)
- `prompts/`: Prompt template files
- `context_size/`: Context length configuration files
- `num_tokens/`: Token limit configuration files
- `models/xtra_models/`: Llama model files

## Configuration Files

### Temperature Files
Create `.temp` files in the `temperatures` directory:
```
temperatures/
├── 0.05.temp
├── 0.3.temp
├── 1.5.temp
└── 1.temp
```

### Prompt Files
Store prompt templates as `.txt` files in the `prompts` directory.

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Access the web interface at `http://localhost:5001`

3. Select your desired:
   - Model
   - Prompt template
   - Context size
   - Number of tokens
   - Temperature

4. Enter your input text and submit to generate the response

## Security Notes

- The application reads credentials from `creds.txt`
- Ensure proper file permissions are set
- Consider implementing additional security measures for production use

## API Endpoints

### GET /
- Returns the main web interface
- Lists available models, prompts, and configuration options

### POST /run_model
- Accepts JSON payload with model parameters
- Returns generated text response
- Parameters:
  - `model`: Selected model name
  - `prompt`: Prompt template file name
  - `input`: User input text
  - `ctls`: Context size
  - `num_tokens`: Maximum tokens to generate
  - `temps`: Temperature value

## Error Handling

The application includes basic error handling for:
- Subprocess execution errors
- File reading/writing operations
- Invalid parameters

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

[Your chosen license]

## Acknowledgments

- Based on the Llama.cpp implementation
- Uses Flask for web interface

