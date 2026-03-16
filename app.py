from flask import Flask, request, send_file, render_template_string
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Hostel Students Marks Generator</title>
</head>
<body style="font-family:Arial;text-align:center;margin-top:50px;">

    <h2>Upload Marks & Hostel Excel</h2>

    <p>
        🎥 <a href="https://youtu.be/YOUR_VIDEO_LINK" target="_blank">
        Watch Demo Video
        </a>
    </p>

    <form method="POST" enctype="multipart/form-data">
        Marks Excel: <input type="file" name="marks"><br><br>
        Hostel Excel: <input type="file" name="hostel"><br><br>
        <button type="submit">Generate Hostel Marks</button>
    </form>

</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        marks_file = request.files["marks"]
        hostel_file = request.files["hostel"]

        marks_path = os.path.join(UPLOAD_FOLDER, "marks.xlsx")
        hostel_path = os.path.join(UPLOAD_FOLDER, "hostel.xlsx")

        marks_file.save(marks_path)
        hostel_file.save(hostel_path)

        marks = pd.read_excel(marks_path)
        hostel = pd.read_excel(hostel_path)

        common_column = "REG NO"   # change if needed

        marks[common_column] = marks[common_column].astype(str).str.strip()
        hostel[common_column] = hostel[common_column].astype(str).str.strip()

        hostel_marks = marks[marks[common_column].isin(hostel[common_column])]

        output_path = os.path.join(UPLOAD_FOLDER, "hostel_students_marks.xlsx")
        hostel_marks.to_excel(output_path, index=False)

        return send_file(output_path, as_attachment=True)

    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(debug=True)
