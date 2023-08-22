# Schoology Albums Downloader CLI

## Usage

### Option 1: Run the binary

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

### Option 2: Docker

1. Go to `https://<school>.schoology.com/api`, generate the consumer key and secret.

1. Run the following commands, replace `<YOUR_CONSUMER_KEY>` and `<YOUR_CONSUMER_SECRET>` with yours.

   ```bash
   mkdir downloads
   echo "SCHOOLOGY_API_CONSUMER_KEY=<YOUR_CONSUMER_KEY>" > ./downloads/.env
   echo "SCHOOLOGY_API_CONSUMER_SECRET=<YOUR_CONSUMER_SECRET" >> ./downloads/.env
   chown -R 1000:1000 downloads
   ```

1. Run the downloader

   ```bash
   docker run -v $PWD/downloads:/downloads x1nm/sadc
   ```

   Photos will be downloaded into `./downloads/photos/<parent_name>/<child_name>/<course_title>/<album_title>/` .
