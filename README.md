# Jira Revoker

## Overview
Jira Revoker is a Flask-based web application designed to manage user permissions in Jira by allowing administrators to upload a CSV file containing user information, process it, and revoke permissions as needed.

## Features
- **Upload CSV**: Users can upload a CSV file with user details.
- **Revoke Permissions**: Automatically revokes permissions for users listed in the uploaded CSV file.
- **Results Display**: Shows the outcome of the revoke operation in a tabulated format on the web interface.

## Installation

### Prerequisites
- Python 3.6 or higher
- pip

### Dependencies
Install the required dependencies by running:
```sh
pip install -r requirement.txt
```

## Configuration
Set up the Flask application by configuring the secret key and upload folder in app.py:

app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads/'

Usage
Running the Application
Start the application by executing:

python app.py

The application will be accessible at http://localhost:5000.

```markdown

### Running the Application
Start the application by executing:
```sh
python app.py
```
Navigate to `http://127.0.0.1:5000/` in your web browser to access the Jira Revoker application.

### Uploading CSV File
1. Click on the "Upload CSV File" button.
2. Select the CSV file containing user details to be revoked.
3. Click on "Upload" to submit the file.

### Viewing Results
After uploading the CSV file, the application will process the file and display the results of the revoke operation on a new page.

## CSV File Format
The CSV file should contain the following columns:
- User id
- User name
- email
- User status
- Added to org
- Org role
- Last seen in Jira Service Management - telkomdds
- Last seen in Jira - telkomdds
- Last seen in Confluence - telkomdds
- Last seen in Atlas - telkomdds
- Filter Jira Service Management
- Filter Jira Software
- Filter Confluence
- Filter Atlas
- One Month Create

Example:
```csv
User id,User name,email,User status,Added to org,Org role,Last seen in Jira Service Management - telkomdds,Last seen in Jira - telkomdds,Last seen in Confluence - telkomdds,Last seen in Atlas - telkomdds,Filter Jira Service Management,Filter Jira Software,Filter Confluence,Filter Atlas,One Month Create
712020:978521a6-2367-4092-a7f6-7cc1b9043bdd,akmalimansyah1,akmalimansyah1@gmail.com,Active,3 Jan 2024,NaN,Never accessed,28 Apr 2024,12 May 2024,Never accessed,False,False,False,False,False
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.
```

User id,User name,email,User status,Added to org,Org role,Last seen in Jira Service Management - telkomdds,Last seen in Jira - telkomdds,Last seen in Confluence - telkomdds,Last seen in Atlas - telkomdds,Filter Jira Service Management,Filter Jira Software,Filter Confluence,Filter Atlas,One Month Create
712020:978521a6-2367-4092-a7f6-7cc1b9043bdd,akmalimansyah1,akmalimansyah1@gmail.com,Active,3 Jan 2024,NaN,Never accessed,28 Apr 2024,12 May 2024,Never accessed,False,False,False,False,False


License
This project is licensed under the MIT License - see the LICENSE file for details. ```