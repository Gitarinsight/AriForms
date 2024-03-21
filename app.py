from flask import Flask, render_template, request, send_file
from docx import Document
from docxtpl import DocxTemplate
from docx2pdf import convert
from datetime import datetime
import pythoncom
import os
import psutil

app = Flask(__name__)

@app.route('/morakhasi')
def index():
    return render_template('morakhasi.html')

@app.route('/generate_morakhasi_docx', methods=['POST'])
def generate_docx():
    # Get form data
    fullName = request.form['fullName']
    department = request.form['department']
    leaveType = request.form['leaveType']
    duration = request.form['duration']
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    dailyDuration = request.form['dailyDuration']
    dailyDate = request.form['Date']
    startTime = request.form['startTime']
    endTime = request.form['endTime']

    doc = DocxTemplate('templates/morakhasi.docx')

    tick1 = ""
    tick2 = ""

    if leaveType == "daily":
        tick1 = "X"
    else:
        tick2 = "X"

    context = {
        'نام': fullName,
        'department': department,
        'tick1': tick1,
        'tick2': tick2,
        'مدتروزانه': duration,
        'تاریخشروع': startDate,
        'تاریخپایان': endDate,
        'مدتساعتی': dailyDuration,
        'تاریخ': dailyDate,
        'ساعتشروع': startTime,
        'ساعتپایان': endTime,
    }
    doc.render(context)

    filename = department + '_' + str(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))

    # Save the modified document
    output_path = filename + '.docx'
    output_full_path = os.path.abspath(output_path)  # Get the full path
    doc.save(output_full_path)

    # Convert DOCX to PDF
    pdf_file = filename + '.pdf'
    convert_docx_to_pdf(output_full_path, pdf_file)


    # Send the generated document as a response
    return send_file(pdf_file, mimetype='application/pdf', as_attachment=True, download_name=filename)

def convert_docx_to_pdf(docx_file, pdf_file):
    try:
        # Close any existing instances of Microsoft Word
        for proc in psutil.process_iter():
            if "WINWORD.EXE" in proc.name():
                proc.kill()

        pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
        convert(docx_file, pdf_file)
        return pdf_file
    except Exception as e:
        print(f'Error: {str(e)}')


if __name__ == "__main__":
    app.run(debug=True)
