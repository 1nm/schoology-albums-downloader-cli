# Schoology Albums Downloader CLI

Downloads all photos and videos from Schoology albums.

## Usage

1. Go to `https://<school>.schoology.com/api`, generate the consumer key and secret.

1. Run the following commands, replace `<YOUR_CONSUMER_KEY>` and `<YOUR_CONSUMER_SECRET>` with yours.

   ```bash
   echo 'SCHOOLOGY_API_CONSUMER_KEY=<YOUR_CONSUMER_KEY>' >> .env
   echo 'SCHOOLOGY_API_CONSUMER_SECRET=<YOUR_CONSUMER_SECRET>' >> .env
   ```

1. (Option 1) Run with Docker

   ```bash
   docker run -v $PWD:/downloads x1nm/sadc
   ```

1. (Option 2) Run the script with Python3

   ```bash
   pip3 install -r requirements.txt
   python3 main.py
   ```

Photos will be downloaded into `./photos/<parent_name>/<child_name>/<course_title>/<album_title>/`