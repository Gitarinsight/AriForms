from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/send-data', methods=['POST'])
def receive_data():
    # Get JSON data sent from client-side JavaScript
    data = request.get_json()

    # Extract variables from JSON data
    fullName = data['fullName']
    department = data['department']
    leaveType = data['leaveType']
    duration = data['duration']
    startDate = data['startDate']
    endDate = data['endDate']
    dailyDuration = data['dailyDuration']
    Date = data['Date']
    startTime = data['startTime']
    endTime = data['endTime']

    # Create a blank image
    img = Image.new('RGB', (800, 600), color='white')

    # Initialize the drawing context
    draw = ImageDraw.Draw(img)

    # Define the font and font size
    font = ImageFont.truetype("arial.ttf", 24)

    # Write the variables onto the image
    draw.text((10, 10), f"Full Name: {fullName}", fill='black', font=font)
    draw.text((10, 40), f"Department: {department}", fill='black', font=font)
    draw.text((10, 70), f"Leave Type: {leaveType}", fill='black', font=font)
    draw.text((10, 100), f"Duration: {duration}", fill='black', font=font)
    draw.text((10, 130), f"Start Date: {startDate}", fill='black', font=font)
    draw.text((10, 160), f"End Date: {endDate}", fill='black', font=font)
    draw.text((10, 190), f"Daily Duration: {dailyDuration}", fill='black', font=font)
    draw.text((10, 220), f"Date: {Date}", fill='black', font=font)
    draw.text((10, 250), f"Start Time: {startTime}", fill='black', font=font)
    draw.text((10, 280), f"End Time: {endTime}", fill='black', font=font)

    # Save the image to a bytes buffer
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    pdfmetrics.registerFont(TTFont('Persian', 'akshar.ttf'))
    c = canvas.Canvas("request.pdf", pagesize=letter)
    c.setFont('Persian', 12)
    text = "احتراما اینجانب رضا آزاده مشغول در واحد اینسایت تقاضای مرخصی دارم"
    rtl_text = text[::-1]
    c.drawString(100, 750, rtl_text)
    c.save()

    return send_file(img_byte_array, mimetype="image/png", download_name="request.png", as_attachment=True)
    # Return the image data as a response with appropriate headers for download
    # return send_file(img_byte_array, attachment_filename='generated_image.png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)