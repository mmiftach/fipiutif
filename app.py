from flask import Flask, request, redirect, flash, send_from_directory,render_template_string

import pandas as pd
import shutil
import os
import requests
import json
import os
import pandas as pd
import datetime
import csv


app = Flask(__name__)
app.secret_key = 'ba1a2a5a16902566850db7125beadd8c'

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

#***webserver
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Delete all files in the UPLOAD_FOLDER before saving the new file
            delete_files_in_directory(app.config['UPLOAD_FOLDER'])
            filename = 'export-users.csv'  # Renamed file to export-users.csv
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            processed_filename, table_html = process_file(filepath)
            download_link = f'<a href="/download/{os.path.basename(processed_filename)}" class="btn btn-primary">Download Processed File</a>'
            return f'''
            <!doctype html>
            <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Jira Revoker - Processed Data</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    .table td, .table th {{
                        text-align: center;
                        border: 1px solid #dee2e6;
                    }}
                </style>
            </head>
            <body>
            <div class="container mt-5">
                <h1>Jira Revoker</h1>
                <div class="card">
                <div class="card-header">
                    Processed Data
                </div>
                <div class="card-body">
                    {table_html}
                </div>
                </div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
            </body>
            </html>
            '''
        else:
            flash('File type not allowed')
            return redirect(request.url)
    return '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Jira Revoker - Upload CSV</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
      <div class="container mt-5">
        <h1>Jira Revoker</h1>
        <div class="card">
          <div class="card-header">
            Upload CSV File
          </div>
          <div class="card-body">
            <form method="post" enctype="multipart/form-data">
              <div class="mb-3">
                <input type="file" name="file" class="form-control">
              </div>
              <button type="submit" class="btn btn-primary">Upload</button>
            </form>
          </div>
        </div>
      </div>
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''
    
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/revoke/<filename>', methods=['POST'])
def revoke_admin(filename):
    # Construct the filepath for the processed file
    processed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    print(processed_filepath)
    # Assume revokeListJira returns a list of dictionaries, e.g., [{'user': 'john_doe', 'status': 'Revoked'}, ...]
    results = revokeListJira(processed_filepath)
    print(results)
    flash('Users have been successfully revoked')

   # Assuming the 'results' variable is already defined as shown
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Revoke Complete</title>
        <!-- Include Bootstrap CSS from CDN -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="mb-3 text-center">Revoke Operation Completed</h1>
            <p class="mb-3 text-center">Users have been successfully revoked. See the results below:</p>
            <!-- Apply Bootstrap table styling -->
            <table class="table table-bordered">
                <thead class="thead-light">
                    <tr>
                        <th class="text-center">Username</th>
                        <th class="text-center">Email</th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in results %}
                    <tr>
                        <td class="text-center">{{ row[1] }}</td>
                        <td class="text-center">{{ row[2] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            <!-- Back to Home button -->
            <div class="text-center mt-4">
                <a href="/" class="btn btn-primary">Back to Home</a>
            </div>
        </div>
        <!-- Optional JavaScript and jQuery for Bootstrap components -->
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </body>
    </html>
    ''', results=results)

def process_file(filepath):
    data = pd.read_csv(filepath)
    filtered_data = filterAccount(data)  # Assuming filterAccount now returns a DataFrame
    processed_filename = filepath.rsplit('.', 1)[0] + '_processed.csv'  # Append '_processed' to the original filename
    filtered_data.to_csv(processed_filename, index=False)  # Save the processed file
    
    # Wrap the table in a div with class 'table-responsive' for responsiveness
    table_html = f'<div class="table-responsive"><table class="table table-striped table-bordered text-center">{filtered_data.to_html(classes="table text-center table-bordered", index=False, border=0)}</table></div>'
    
    # Correctly place the download button on the left and the revoke button on the right
    buttons_html = f'''
    <div style="display: flex; justify-content: space-between; margin-top: 20px;">
        <div>
            <form action="/download/{os.path.basename(processed_filename)}" method="get">
                <button type="submit" class="btn btn-primary">Download Processed File</button>
            </form>
        </div>
        <div>
            <form action="/revoke/{os.path.basename(processed_filename)}" method="post">
                <button type="submit" class="btn btn-danger">Revoke Processed Users </button>
            </form>
        </div>
    </div>
    '''
    
    # Combine table and buttons HTML
    combined_html = table_html + buttons_html
    
    return processed_filename, combined_html  # Return both the filename and HTML string

def delete_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')



#***functionRevokeJira
def revokeJira(userId):
  token = "eyJraWQiOiJzZXNzaW9uLXNlcnZpY2UvcHJvZC0xNTkyODU4Mzk0IiwiYWxnIjoiUlMyNTYifQ.eyJhc3NvY2lhdGlvbnMiOltdLCJzdWIiOiI2MWYzNjVlYWNiN2M1ZjAwNmIwYWNiZDUiLCJlbWFpbERvbWFpbiI6InRlbGtvbS5jby5pZCIsImltcGVyc29uYXRpb24iOltdLCJjcmVhdGVkIjoxNjk1MjYzODI0LCJyZWZyZXNoVGltZW91dCI6MTcxNzc3NzQ4NiwidmVyaWZpZWQiOnRydWUsImlzcyI6InNlc3Npb24tc2VydmljZSIsInNlc3Npb25JZCI6IjQwODQyY2Y1LTM1MTMtNDc4Yi1iMGQxLTA3ODY5MGIzMmZiOCIsInN0ZXBVcHMiOltdLCJhdWQiOiJhdGxhc3NpYW4iLCJuYmYiOjE3MTc3NzY4ODYsImV4cCI6MTcyMDM2ODg4NiwiaWF0IjoxNzE3Nzc2ODg2LCJlbWFpbCI6Ijk0MDQ4N0B0ZWxrb20uY28uaWQiLCJqdGkiOiI0MDg0MmNmNS0zNTEzLTQ3OGItYjBkMS0wNzg2OTBiMzJmYjgifQ.rW92LYkTmp0jhdkLC-ntqYzk5_nDbI9caRaDVxZ3iWn6A3XBEBkI__lGMBu47RDeft4Gis5XI9McnpkkpsYXYXZpnTvBLEC1a2deloYhQ7mI7UUeg2z05E14FwOYdyslnkr-XL590dKYG188khgrjHv6j3Nbd8aY73AjKQL2tue7vHmic7rJyjt19_Pdjxam1G2e0i6t2grRzFG04fTT8-uI9W3FL6b_ObnwxFYsPSpbjIiRpQE5FhMVfFxw6pOdGLDH5frelkDpNq2_-0JumLVp6uW9FpHFx51Qp4OBi3KqV6IqQFi4Kvd-uujMrr8N5wyTbyLpJ5h5_bj3e7pizQ"
  acountId = userId
  #old url = "https://admin.atlassian.com/gateway/api/adminhub/um/site/d671a7c1-0502-419d-b721-1028332bc10a/users/"+acountId+"/deactivate"
  url = "https://admin.atlassian.com/gateway/api/adminhub/um/org/9b02d1eb-a23d-4222-9b04-444ba42b9d0a/users/"+acountId+"/deactivate"

  headers = {
    "Content-Type": "application/json",
    'Cookie': token
  }

  payload = json.dumps( {
    "message": "On 6-month suspension"
  } )

  response = requests.post(url, headers={'Cookie': "cloud.session.token="+token})
  return response.status_code

def convertCSVtoList(csvFile):
    with open(csvFile, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        list = []
        for row in reader:
            list.append(row)
    return list

def revokeListJira(data):
  listRevokeUser = convertCSVtoList(data)  # Convert the DataFrame to a list
  revokedUsers = []  # Step 1: Initialize an empty list to store revoked user IDs
  for index, revokeUser in enumerate(listRevokeUser):
      if index == 0:
          continue  # Skip the first iteration
      print(revokeJira(revokeUser[0]))  # Step 2: Print the response from the revokeJira function
      revokedUsers.append(revokeUser)  # Step 2: Append the user ID to the list
  return revokedUsers  # Step 3: Return the list of revoked user IDs


#***functionFilterAccount
def filter_data(column_name, date,data):
    return data[column_name].apply(lambda x: False if x == "Never accessed" else pd.to_datetime(x, format='%d %b %Y', errors='coerce') > pd.to_datetime(date, format='%d %b %Y'))

def filterAccount(data):
    # Define the date
    current_date = datetime.datetime.now()
    date = (current_date - datetime.timedelta(days=30)).strftime('%d %b %Y')

    # Apply the filter to the necessary columns
    data['Filter Jira Service Management'] = filter_data('Last seen in Jira Service Management - telkomdds', date,data)
    data['Filter Jira Software'] = filter_data('Last seen in Jira - telkomdds', date,data)
    data['Filter Confluence'] = filter_data('Last seen in Confluence - telkomdds', date,data)
    data['Filter Atlas'] = filter_data('Last seen in Atlas - telkomdds', date,data)

    # Filter the 'Added to org' column
    data['One Month Create'] = pd.to_datetime(data['Added to org'], format='%d %b %Y', errors='coerce') > pd.to_datetime(date, format='%d %b %Y')

    # Create a mask for rows where all filters are False
    mask = (
        (data['Filter Jira Software'] == False) &
        (data['Filter Jira Service Management'] == False) &
        (data['Filter Confluence'] == False) &
        (data['Filter Atlas'] == False) &
        (data['One Month Create'] == False)
    )

    # Print the filtered data and save it to a CSV file
    return data[mask]



if __name__ == '__main__':
    app.run(debug=True)