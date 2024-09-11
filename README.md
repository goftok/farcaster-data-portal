# Farcaster Data Portal

The **Farcaster Data Portal** is a Flask-based API that provides advanced tools and features for interacting with Farcaster data, including checking copywriting, generating casts, retrieving ENS addresses, and accessing detailed user engagement metrics. This portal extends the functionality of Warpcast by offering features not available to default users.

## Features

- **Check Copywriting**: Ensure that your casts are compliant with copyright standards.
- **Generate Casts**: Automatically generate casts based on specific keywords.
- **Fetch ENS Addresses**: Retrieve ENS addresses linked to Warpcast users.
- **Retrieve Top Warps Tipped**: Access the top casts based on warp tips, views, reactions, and replies.


## Project Structure

```bash
backend/
├── env_links.py                 # Environment variables and model paths
├── models.py                    # Database models and structure
├── resources/
│   ├── home_page.py             # Home page resource
│   ├── healthy_check.py         # Health check resource
│   ├── check_copywriting.py     # Check copywriting resource
│   ├── generate_cast.py         # Generate cast resource
│   ├── get_most_warps_tipped.py # Get top warps tipped resource
│   └── get_ens_for_the_user.py  # Get ENS for user resource
├── scrappers/
│   └── scrap_ens.py             # Script for scraping ENS information
app.py                           # Main application script
requirements.txt                 # Dependencies for the project
README.md                        # Project documentation
```

## Installation

1. **Clone the repository**:

```bash
   git clone https://github.com/your-username/farcaster-data-portal.git
   cd farcaster-data-portal
```

2. Set up a virtual environment:

```bash
    python3 -m venv venv
    source venv/bin/activate
```

3. Install the required dependencies:

```bash
   pip install -r requirements.txt
```

4. Set up environment variables:

Create a .env file in the root directory with the structure as in the .env.example

5. Set up the PostgreSQL database:

Use the models.py file to set up the database structure. Run the SQL commands or use an ORM to create the necessary tables for profiles, addresses, and casts.

## Running the API
Start the Flask API:

```bash
    python -m backend.app
```

## Hosting

The application is currently hosted on **Heroku** and can be accessed via the following URL:

[https://farcaster-data-portal-e40fc222318a.herokuapp.com/](https://farcaster-data-portal-e40fc222318a.herokuapp.com/)

Note: The model is not yet deployed
