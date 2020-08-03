from flask import Flask, redirect, render_template, request
import pymongo
import random
import string
import pymongo

# DB CONFIG
MONGO_URI = "mongodb://localhost:27017/"
client = pymongo.MongoClient("mongodb://localhost:27017/")
table = client.url.urls

# FLASK
app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def main():
    """ Main method for program. Handles both POST and GET requests for the url shortening website and service.

    Returns:
        string: Returns corresponding or new short URL.
    """

    if request.method == "POST":
        # parse json body data
        data = request.get_json()

        url = table.find_one({"original": data["original"]})

        # check if url already exists
        if url:
            return "http://127.0.0.1:5000/{0}".format(url["key"])
        else:
            key = get_random_string()
            url = table.find_one({"key": key})

            # loop to make sure each key is different
            while url:
                key = get_random_string()
                url = table.find_one({"key": key})

            table.insert_one({"original": data["original"], "key": key})
            return "http://127.0.0.1:5000/{0}".format(key)

    else:
        return render_template("index.html")


@app.route("/<key>", methods=["GET"])
def key_detector(key):
    """ Detects key in database and redirects user to corresponding original field.

    Args:
        key (string): The URL's unique key

    Returns:
        function: Redirects to original page or 404 page.
    """

    url = table.find_one({"key": key})

    if url:
        return redirect(url["original"])
    else:
        return "404"


def get_random_string():
    """ Generates random string with an assortment of characters.

    Returns:
        string: New key value
    """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(6))


if __name__ == "__main__":
    app.run(debug=True)
