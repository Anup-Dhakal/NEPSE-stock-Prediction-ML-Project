from flask import Flask, send_file
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the Nepse Index History Dataset!'

@app.route('/download')
def download_csv():
    # Read the dataset
    df = pd.read_csv('/kaggle/input/nepse-index-historical-data/nepse_index_history.csv', parse_dates=['date'], index_col=0, thousands=',')
    
    # Save the dataset to a temporary file
    temp_file_path = '/tmp/nepse_index_history.csv'
    df.to_csv(temp_file_path)
    
    # Send the file for download
    return send_file(temp_file_path, as_attachment=True, attachment_filename='nepse_index_history.csv')

if __name__ == '__main__':
    app.run(debug=True)
