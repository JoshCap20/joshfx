#!/bin/bash

# Utility handlers
handle_sigint() {
    echo "You killed me :( Exiting..."
    exit 1
}

handle_error() {
    echo -e "\033[0;31m[$(date '+%Y-%m-%d %H:%M:%S')] [PID: $$] [ERROR] $1\033[0m"
    exit 1
}

trap handle_sigint SIGINT

# Message handlers
log_warning() {
    echo -e "\033[0;31m[$(date '+%Y-%m-%d %H:%M:%S')] [PID: $$] [WARN] $1\033[0m"
}

log_success() {
    echo -e "\033[0;32m[$(date '+%Y-%m-%d %H:%M:%S')] [PID: $$] [SUCCESS] $1\033[0m"
}

log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [PID: $$] [INFO] $1"
}

# Setup process
command -v python3 >/dev/null 2>&1 || handle_error "Python 3 is not installed. Please install Python 3 before running the application."

# log_message "You have been hacked!"
# sleep 5
# log_message "Just kidding. Setup started."

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating a new one..."
    python3 -m venv venv || handle_error "Failed to create virtual environment."
fi

log_message "Activating the virtual environment..."
source venv/bin/activate || handle_error "Failed to activate virtual environment."

log_message "Ensuring pip is up-to-date..."
pip install --upgrade pip || handle_error "Failed to update pip."

log_message "Checking for any missing requirements..."
pip install -r requirements.txt || handle_error "Failed to install requirements."
log_success "All requirements are met."

log_message "Running migrations..."
python manage.py makemigrations || handle_error "Failed to run makemigrations."
python manage.py migrate || handle_error "Failed to run migrations."
log_success "Migrations completed."

python manage.py load_movies video32.csv || handle_error "Failed to load movies."
open http://localhost:8000
python manage.py runserver

exit 0
