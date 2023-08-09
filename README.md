# url_shortner_app

This Flask application provides a simple URL shortening service using a SQLite database and Hashids for generating unique short URLs.

# Introduction

This URL shortener API allows you to shorten long URLs and manage them. It utilizes a SQLite database to store URL data and Hashids library to create unique short URLs.

# Setup

1. Prerequisites: A local Python 3 programming environment
2. Clone this repository to your local machine.
3. Go inside the project folder and activate your programming environment

    `source env/bin/activate`

4. Once you have activated your programming environment, install Flask, validators and the Hashids library using the following command:

    `pip install flask hashids validators`
5. Run the unit test using the command

    `python -m unittest test_app.py`
6. Start the application using command, The application will run on `http://127.0.0.1:5000/`.

    `flask run`

# API Endpoints

## Shorten URL
Shortens a provided URL and saves it in the database.

- **URL:** `/`
- **Method:** POST
- **Data Params:**
  - `url`: The URL to be shortened (Required)
  - `expiry`: The expiration date of the short URL (Optional)
- **Success Response:**
  - **Code:** 200
  - **Content:** `{ "shortened_url": "shortened_url_here" }`
- **Error Response:**
  - **Code:** 400
  - **Content:** `{ "message": "Error message here" }`

## Redirect
Redirects a short URL to the original long URL.

- **URL:** `/<id>`
- **Method:** GET

## Statistics
Fetches statistics about the stored URLs.

- **URL:** `/stats`
- **Method:** GET
- **Success Response:**
  - **Code:** 200
  - **Content:** `{ "urls": [ { "id": "short_id", "created": "timestamp", "original_url": "original_url_here", "short_url": "short_url_here", "expiry": "expiry_date", "clicks": click_count }, ... ] }`

## Delete URL
Deletes a short URL and its data from the database.

- **URL:** `/delete/<id>`
- **Method:** DELETE
- **Success Response:**
  - **Code:** 200
  - **Content:** `{ "message": "URL with ID <id> and short URL <short_url> has been deleted" }`
- **Error Response:**
  - **Code:** 404
  - **Content:** `{ "message": "URL with given ID not found" }`

# Note
If the `expiry` parameter is not provided during URL shortening, the default expiration is set to 10 years from the current timestamp.

# Contributors
- Siddharth Sinha




