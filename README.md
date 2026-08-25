# Helpora

Helpora is a donation platform built with Flask that allows users to create fundraising campaigns and support people in need through donations.

The application includes user authentication, campaign management, donation tracking, profile management, and an admin system for reviewing and managing campaigns.

## Features

- User registration and login
- Secure password hashing
- User profile and profile settings
- Password changing
- Campaign creation
- Campaign editing and deletion
- Campaign categories and filtering
- Admin approval and rejection of campaigns
- Donation system
- Donation history
- Fundraising progress tracking
- Campaign goal progress bar
- Admin dashboard
- Campaign and donation management
- Access control for campaign owners and administrators

## Tech Stack

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Werkzeug

### Database
- SQLite

### Frontend
- HTML
- CSS
- Bootstrap
- Jinja2

## Project Structure

```text
Helpora/
│
├── server.py
├── models.py
├── forms.py
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── homepage.html
│   ├── all_campaigns.html
│   ├── single_campaign.html
│   ├── add_campaign_form.html
│   ├── edit.html
│   ├── donate.html
│   ├── success_donate.html
│   ├── login_page.html
│   ├── register_page.html
│   ├── my_profile.html
│   ├── profile_settings.html
│   ├── admin.html
│   └── about_page.html
│
└── static/
    ├── css/
    └── uploads/
```

## How It Works

Users can create an account and submit fundraising campaigns. Campaigns created by regular users must be reviewed by an administrator before becoming publicly available.

Once approved, other users can view the campaign and make donations. The application tracks the total amount donated and displays the progress toward the campaign's fundraising goal.

Campaign owners can manage their own campaigns, while administrators have additional permissions for reviewing and managing campaigns across the platform.

## Installation

Clone the repository:

```bash
git clone https://github.com/DVeljko/Helpora.git
```

Enter the project directory:

```bash
cd Helpora
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your Flask secret key:

```text
SECRET_KEY=your_secret_key
```

Run the application:

```bash
python server.py
```

## Screenshots

Screenshots of the application will be added here.

## Current Limitations

Helpora is currently a portfolio/development project.

Donations are recorded by the application, but no real payment gateway is currently integrated.

## Future Improvements

- PostgreSQL database support
- Database migrations with Flask-Migrate
- Real payment gateway integration
- Improved campaign completion workflow
- Additional admin controls
- Deployment to a production environment
- Automated tests

## Author

**Veljko Dimitrijevic**

Python Backend Developer
