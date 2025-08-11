from flask import Flask, request, send_file, abort
from playwright.sync_api import sync_playwright
import tempfile
import os

app = Flask(__name__)

@app.route("/pdf", methods=["GET"])
def generate_pdf():
    itinerary_id = request.args.get("id")
    if not itinerary_id:
        abort(400, "Missing id parameter")

    url = f"https://letstrip.world/dashboard/pdf-preview?id={itinerary_id}"

    # Temp file for PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        pdf_path = tmp_pdf.name

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="load")
        page.wait_for_selector("body")

        full_height = page.evaluate("document.body.scrollHeight")
        page.set_viewport_size({"width": 1200, "height": full_height})

        page.pdf(
            path=pdf_path,
            width="400px",
            height=f"{full_height}px",
            print_background=True,
            page_ranges="1",
        )
        browser.close()
    # Return file to user
    return send_file(pdf_path, as_attachment=True, download_name="itinerary.pdf")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)