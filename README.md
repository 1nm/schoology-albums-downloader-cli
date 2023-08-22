# Schoology Albums Downloader CLI

## Usage

1. Install the dependencies

   ```bash
   pip3 install -r requirements.txt
   ```

1. Go to `https://<school>.schoology.com/api`, generate the consumer key and secret.

1. Edit `.env`, copy the content from `.env.example` and fill in the consumer key and secret.

1. Run the script

   ```bash
   python3 main.py
   ```

   Photos will be downloaded into `./photos/<parent_name>/<child_name>/<course_title>/<album_title>/` .
