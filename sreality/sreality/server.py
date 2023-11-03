from flask import Flask

from sreality.utils import close_db, connect_db_from_env

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Home page with first 500 ads from SReality (only flats for sales).

    Page renders ad title and image.
    """
    conn, cursor = connect_db_from_env()

    cursor.execute("SELECT * FROM ads")
    ads_records = cursor.fetchall()
    close_db(conn, cursor)

    if ads_records:
        # Minor optimization. Since Python string is immutable and would be changed many times,
        # I decided to put rendered elements into a list and join them once the response all ads
        # are rendered.
        ads_html_list = []
        for ad in ads_records:
            ads_html_list.append(f"<h2>{ad[0]}</h2><img src='{ad[1]}'>")

        return "".join(ads_html_list)
    else:
        return "No data to display."
