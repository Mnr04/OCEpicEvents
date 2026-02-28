# OCEpicEvents - CRM CLI Application

Epic Events is an agency that organizes events for its clients.
This CRM software allows the collection and processing of client and event data, while facilitating communication between the company's different departments.

This is a command-line interface (CLI) application built with Python 3.

###  Installation and Setup

1. Clone the repository and navigate to the directory:

```bash
git clone https://github.com/Mnr04/OCEpicEvents.git
cd OCEpicEvents
```

2. Create and activate a virtual environment (recommended):

```bash
python3 -m venv env
source env/bin/activate

# On Windows:
env\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Environment variables configuration:

Create a .env file at the root of the project and add your keys (database, JWT, Sentry):

```python
DATABASE_URL=sqlite:///epic_events.db
SECRET_KEY=your_jwt_secret_key
SENTRY_DSN=your_sentry_key
```

## Database Initialization

Before the first use, you must initialize the database. This command will create the tables and generate a default admin account (Management Team):

```bash
python init_db.py
(Default credentials: admin / admin123)
```


## Usage (CLI Commands)

The application is run via the main.py entry point.

1. The Magic Command (Help)

To discover all available commands and options:

```bash
python main.py --help
python main.py users --help
python main.py contracts --help
```

2. Login (Authentication)

You must be logged in to access the data:

```bash
python main.py auth login

To logout:
python main.py auth logout
```

3. Manage Users (Management Team)

```bash
# View all users
python main.py users list

# Create a user (Click will prompt you step by step)
python main.py users create

# One line mode
python main.py users create --nom "Alice" --email "alice@epicevents.com" --role "Commercial"

# Update or delete
python main.py users update
python main.py users delete
```

4. Manage Clients (Sales Team)

```bash
# View the list of all clients
python main.py clients list

# Create a client
python main.py clients create

# Update the company name of a client you are responsible for
python main.py clients update
```

5. Manage Contracts
```bash
# View all contracts
python main.py contracts list

# View only unsigned contracts
python main.py contracts list --filtre non-signes

# View only unpaid contracts
python main.py contracts list --filtre non-payes

# Create a contract (Management Team only)
python main.py contracts create

# Sign a contract (Sales Team) using the "--signe" flag
python main.py contracts update --contract-id 1 --signe
```

6. Manage Events
```bash
# View all events
python main.py events list

# Create an event (Sales Team, requires a signed contract)
python main.py events create

# List events that do not have a support contact assigned yet (Management Team)
python main.py events list --filtre sans-support

# Assign a Support colleague to an event (Management Team)
python main.py events update --event-id 1 --support-id 3

# View my own events (Support Team)
python main.py events list --filtre mes-evenements
```

## Testing and Code Coverage

The project uses pytest for unit and integration testing.

Run the tests:

```bash
python -m pytest
```

Check code coverage:

```bash
coverage run -m pytest
coverage report
```