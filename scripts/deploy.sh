#!/bin/bash

# Exit on any error
set -e

# Define variables
APP_DIR="/home/ec2-user/employee-entry-form-web-app"
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
GUNICORN_SERVICE_PATH="/etc/systemd/system/gunicorn.service"
GUNICORN_PORT="5000"
GUNICORN_WORKERS="3"
USER="ec2-user"
GROUP="webapps"
APP_MODULE="app:app"  # Adjust this if your app module is named differently
REMOTE_DIR="/home/jenkins/jenkins-agent/workspace/dev-EmployeeEntryFormBuildDeploy/"
REMOTE_KEY="/var/lib/jenkins/.ssh/dev-employee-entryfrom-web-python.pem"
REMOTE_IP="54.179.191.156"

# Rsync to copy the application code from Jenkins to EC2
echo "Syncing application files from Jenkins workspace..."
rsync -avzu --delete -e "ssh -i ${REMOTE_KEY}" ${REMOTE_DIR} ec2-user@${REMOTE_IP}:${APP_DIR}

# Navigate to the application directory
cd ${APP_DIR} || exit

# Delete and recreate the virtual environment
if [ -d "${VENV_DIR}" ]; then
    echo "Removing existing virtual environment..."
    rm -rf ${VENV_DIR}
fi

# Create a new virtual environment
echo "Creating a new virtual environment..."
python3 -m venv ${VENV_DIR} || { echo "Failed to create virtual environment"; exit 1; }

# Activate the virtual environment
echo "Activating virtual environment..."
source ${VENV_DIR}/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

# Upgrade pip to the latest version
pip install --upgrade pip

# Install dependencies
pip install --no-cache-dir -r ${REQUIREMENTS_FILE}

# Run unit tests
echo "Running unit tests..."
python3 -m unittest discover -s tests || { echo "Unit tests failed"; exit 1; }

# Install Gunicorn
pip install --no-cache-dir gunicorn

# Create the Gunicorn service file if it doesn't exist
if [ ! -f ${GUNICORN_SERVICE_PATH} ]; then
    echo "[Unit]
Description=Gunicorn instance to serve Flask Application
After=network.target

[Service]
User=${USER}
Group=${GROUP}
WorkingDirectory=${APP_DIR}
ExecStart=${APP_DIR}/${VENV_DIR}/bin/gunicorn --workers ${GUNICORN_WORKERS} --bind 0.0.0.0:${GUNICORN_PORT} ${APP_MODULE}

[Install]
WantedBy=multi-user.target" | sudo tee ${GUNICORN_SERVICE_PATH}
fi

# Reload systemd
sudo systemctl daemon-reload

# Start Gunicorn
sudo systemctl start gunicorn

# Enable Gunicorn to start on boot
sudo systemctl enable gunicorn

# Restart Gunicorn to apply any changes
sudo systemctl restart gunicorn
