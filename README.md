# Smart Travel Agent ✈️

Smart Travel Agent is an AI-powered travel planning application that utilizes a multi-agent system to craft the perfect itinerary. Built with **CrewAI** and **Streamlit**, it automates the research and planning process for your next trip.

## 🌟 Features

- **Multi-Agent Research**: Uses specialized AI agents for logistics, destination scouting, and concierge services.
- **Real-time Data**: Integrated with tools for:
  - 🛫 **Flights**: Real-time flight search and logistics.
  - 🏨 **Places**: Hotel and restaurant recommendations using Google Places.
  - 🌤️ **Weather**: Accurate forecasts for your travel dates.
  - 🔍 **Web Search**: Comprehensive research for travel tips and local events.
- **Customizable Itineraries**: Tailor your trip based on budget, travel style, number of travelers, and specific interests.
- **Streamlit Interface**: A clean, interactive web UI for easy planning and previewing.
- **LLM Resilience**: Built-in fallback logic to handle rate limits and API errors by switching between multiple LLMs (e.g., Groq, Gemini).

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- API Keys for:
  - [Groq](https://console.groq.com/) (Primary LLM)
  - [Google Gemini](https://aistudio.google.com/) (Optional Fallback)
  - [Serper.dev](https://serper.dev/) or other search tools (if configured)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Darshan-Subash/Smart-Travel-Agent.git
   cd Smart-Travel-Agent
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GROQ_API_KEY=your_groq_api_key
   # GEMINI_API_KEY=your_gemini_api_key (optional)
   # Add other tool-specific keys as needed
   ```

### Running the Application

- **Web UI (Streamlit)**:
  ```bash
  streamlit run app.py
  ```

- **CLI Mode**:
  ```bash
  python main.py
  ```

## 📂 Project Structure

- `backend/`: Core logic, CrewAI agents, tasks, and custom tools.
- `frontend/`: Streamlit UI components and page layouts.
- `data/`: Knowledge base and data storage.
- `output/`: Generated itineraries.

## 🤖 How it Works

The system employs three specialized agents:
1. **Logistics Specialist**: Handles flight search and transport options.
2. **Destination Scout**: Finds top attractions and restaurants.
3. **Travel Concierge**: Manages hotel bookings, weather checks, and compiles the final day-by-day itinerary.

The agents work sequentially, passing context to ensure the final plan is consistent and data-driven.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
