#!python3

from flask import Flask, render_template, jsonify, request
import random
import requests
r = requests.get('https://www.python.org')

app = Flask(__name__)


# Route to render the index.html template
@app.route('/')
def rootpage():
    return render_template("index.html")


# Route to generate a random quote
@app.route('/random-quote', methods=['GET'])
def random_quote():
    return render_template("quote.html")

# Route to generate quote of the day via search icon
@app.route('/search', methods=['POST'])
def search():
    search_word = request.form.get('search_word')

    if search_word.lower() == 'quote of the day':
        # Make a request to the They Said So Quotes API for the quote of the day
        url = "https://quotes.rest/qod"
        headers = {"X-TheySaidSo-Api-Secret": "bQfClzm6lbrqUKEDB6GZkwsJrLr2r9k1sewSWWr2"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            quote_data = data.get('contents', {}).get('quotes', [])[0]
            quote = quote_data.get('quote')
            author = quote_data.get('author')

            return render_template('result.html', quote=quote, author=author)
        else:
            message = 'Failed to fetch the quote of the day. Please try again.'
            return render_template('error.html', message=message)

    else:
        # Make a request to the They Said So Quotes API with the search word
        url = f"https://quotes.rest/quote/search?category={search_word}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            quotes = data.get('contents', {}).get('quotes', [])

            if quotes:
                # Randomly select a quote from the retrieved quotes
                random_quote = random.choice(quotes)
                quote = random_quote.get('quote')
                author = random_quote.get('author')

                return render_template('result.html', quote=quote, author=author)
            else:
                message = 'No quotes found for the search word.'
        else:
            message = 'Failed to fetch quotes. Please try again.'

        return render_template('error.html', message=message)



# Route to landing page
@app.route('/Home', methods=['GET'])
def landing_page():
    return render_template('landing.html')

# Run the Flask application
if __name__ == '__main__':
    app.run()
