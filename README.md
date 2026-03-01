# Business Intelligence Agent

An executive-level data analysis Business Intelligence Agent connected to Monday.com boards. It answers real-time business queries regarding your Sales Pipeline (Deals Board) and Project Execution (Work Order Tracker).

## Features
- Provides Founder-level insights using Llama-3.3-70b (via Groq API).
- Live fetching of Monday.com API data.
- Built-in conversation memory.
- Standardized and transparent data reporting.
- Ready for production via Docker.

## Running Locally

1. Ensure you have Python 3.11+ installed.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your `.env` file with the required API keys:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   MONDAY_API_KEY=your_monday_api_key_here
   ```
5. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Running via Docker (Production)

The quickest way to run this in production without worrying about environment differences is using Docker and Docker Compose.

1. Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).
2. Ensure your `.env` file is present in the root directory (same folder as `docker-compose.yml`).
3. Build and start the service:
   ```bash
   docker-compose up -d --build
   ```
   > The application will safely run in the background. If the container stops or crashes, it is configured to restart automatically.

4. Open your browser to `http://localhost:8501`.

To stop the containers:
```bash
docker-compose down
```

## Environment Variables Configuration

- **GROQ_API_KEY**: API key for interacting with Groq. Used to instantiate `ChatGroq`.
- **MONDAY_API_KEY**: API key for your Monday.com organization. Required by `tools.py` to query board data.

## Modifying the Model

The Agent currently defaults to `openai/gpt-oss-120b` running on Groq (as explicitly required). You can find this configuration in `main.py` under the `initialize_agent` function.
