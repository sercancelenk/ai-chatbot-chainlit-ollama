# AI Chatbot with Chainlit and Ollama

This project implements a conversational AI chatbot using Chainlit, LangChain, and Ollama. It features user authentication, persistent chat history using PostgreSQL, and integration with the Llama3 model.

## Features

- Interactive chat interface using Chainlit
- User authentication system
- Persistent chat history with PostgreSQL
- Integration with Llama3 model via Ollama
- Dockerized PostgreSQL and pgAdmin setup
- Message history tracking and context management

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Ollama (for running the Llama3 model)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai_bot_chainlit
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with the following content:
```
ANTHROPIC_API_KEY="your_anthropic_api_key"
CHAINLIT_AUTH_SECRET="your_auth_secret"
```

5. Start PostgreSQL and pgAdmin:
```bash
docker-compose -f chainlit_postgres.yml up -d
```

6. Start Ollama (if not already running):
```bash
./run_ollama.sh
```

## Usage

1. Start the Chainlit application:
```bash
chainlit run app.py
```

2. Access the application at `http://localhost:8000`

3. Login credentials:
   - Admin user: username: `admin`, password: `admin`
   - Volkan user: username: `volkan`, password: `volkan`

## Project Structure

- `app.py`: Main application file containing the Chainlit setup and chat logic
- `custom_layer.py`: Custom data layer implementation
- `chainlit_postgres.yml`: Docker Compose configuration for PostgreSQL and pgAdmin
- `requirements.txt`: Python dependencies
- `.env`: Environment variables
- `initdb/`: Database initialization scripts
- `ollama-native/`: Native Ollama configuration
- `ollama-docker/`: Docker-based Ollama configuration

## Database Access

- PostgreSQL is accessible at `localhost:5432`
- pgAdmin is accessible at `http://localhost:8090`
  - Login: admin@example.com / adminpassword

## Dependencies

- chainlit
- python-dotenv
- langchain_core
- langchain_anthropic
- langchain_ollama
- langchain_community
- neo4j
- asyncpg
- SQLAlchemy
- psycopg2-binary
- greenlet

## Security Notes

- The application uses password-based authentication
- Environment variables are used for sensitive information
- Database credentials are configured in the Docker Compose file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here] 