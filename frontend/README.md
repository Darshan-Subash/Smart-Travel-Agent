# Frontend - Smart Travel Agent 🖥️

The frontend is a modern web application built with **Streamlit**, providing an intuitive interface for planning and viewing travel itineraries.

## 🎨 Design and UI

The application uses a custom-styled sidebar and a layout designed for accessibility and visual appeal.

### Components (`frontend/components/`)

- `agent_status.py`: Visualizes the status and logs of the AI agents during the planning process.
- `sidebar.py`: Configures global navigation and user settings.
- `styles.py`: Injects custom CSS for branding and a polished look.

### Pages (`frontend/pages/`)

- **Plan Trip** (`plan_trip.py`): The main workspace where users enter their travel details (destination, origin, dates, budget, etc.) and initiate the planning process.
- **Quick Preview** (`quick_preview.py`): A fast way to view existing itineraries and search results.
- **About** (`about.py`): Provides information about the project, the underlying technology, and the team.

## 🏃 Running the Frontend

To start the Streamlit application:
```bash
streamlit run app.py
```

The application will be accessible at `http://localhost:8501`.
