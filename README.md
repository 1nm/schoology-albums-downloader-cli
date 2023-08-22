# Schoology Albums Downloader CLI

## Usage

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
