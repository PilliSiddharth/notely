import os
import openai
from flask import Flask, request, render_template, send_from_directory
from pip._vendor import cachecontrol

app = Flask("Notely", template_folder='./templates', static_folder='./css')

openai.api_key = "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"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, '/css/favicon/'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('landing.html')

@app.route("/about-us", methods=['GET', 'POST'])
def about_us():
    return render_template('about-us.html')

@app.route("/generate-notes", methods=['GET', 'POST'])
def render_notes():
    if request.method == 'POST':

        curriculum_board = request.form.get('curriculum_board')
        indian_state = request.form.get('indian_state')
        study_grade = request.form.get('study_grade')
        notes_topic = request.form['notes-topic']

        # tokens_trial -= 1  # Deduct one token

        notes_html = generate_notes(curriculum_board=curriculum_board, indian_state=indian_state, study_grade=study_grade, notes_topic=notes_topic)

        return render_template('app.html', notes_there=True)
    else:
        return render_template('app.html')
    

@app.route("/notes", methods=['GET', 'POST'])
def generated_notes():
    return render_template('notes.html')




def generate_notes(curriculum_board, indian_state, study_grade, notes_topic):
    # Custom prompt
    prompt = f'''
You are notely, you can generate detailed and brief and very long and very simple to understand the class notes for students in 10th, 11th, and 12th grade for any chapter of a subject out there. This app is mainly targeted for students in India whose syllabus can be consisted of curriculum ranging from SSC, CBSE, ICSE, or IB. The generated notes should contain in a format of having synopsis, important points to remember, definitions, all formulas, 5 or more example problems solved with step by step explanation of it (the problems should be in right text formatting mathematically or not).
You have to now makes this class notes in a nice html format with a bunch of tags to make it get a class notes feel and make it in bootstrap, also make any mathermatical symbol formatted in HTML with improved mathematical formatting using MathJax and Bootstrap.
Also for showing the problems or solutions, see that everything is in one line by using span tags inside p tags, and use dividers for each section like for the title of the notes, the synopsis and etc. also the title of the notes should be like name of the topic – Notes.
Also make a last section called Diagrams, with 5 image tags in a good fit like very noticeable and nice.
Only do the necessary prompt and return me the necessary code, with nothing else, use this html code template and change the necessary content needed: 
<!DOCTYPE html>
<html>
<head>
  <title>2D Coordinate Plane - Notes</title>
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>
</head>
<body>

<div class="container">
  <h1 class="text-center">2D Coordinate Plane - Notes</h1>
  
  <div class="notes-section">
    <h2>Synopsis</h2>
    <p>The 2D Coordinate Plane is a mathematical tool used to represent points and graph equations. It consists of two perpendicular number lines known as the x-axis and y-axis.</p>
  </div>

  <hr>

  <div class="notes-section">
    <h2>Important Points</h2>
    <ul>
      <li>The point where the x-axis and y-axis intersect is called the origin, denoted as (0, 0).</li>
      <li>The x-coordinate represents the horizontal position of a point, while the y-coordinate represents the vertical position.</li>
      <li>The coordinates of a point on the plane are written as (x, y), where x is the x-coordinate and y is the y-coordinate.</li>
      <li>Quadrants on the coordinate plane are numbered counterclockwise starting from the top right quadrant as I, II, III, and IV.</li>
      <li>Distance between two points A(x1, y1) and B(x2, y2) can be calculated using the distance formula: \(d = \sqrt{{(x2 - x1)^2 + (y2 - y1)^2}}\).</li>
    </ul>
  </div>

  <hr>

  <div class="notes-section">
    <h2>Definitions</h2>
    <ul>
      <li><strong>Origin:</strong> The point where the x-axis and y-axis intersect, denoted as (0, 0).</li>
      <li><strong>X-axis:</strong> The horizontal number line on the coordinate plane.</li>
      <li><strong>Y-axis:</strong> The vertical number line on the coordinate plane.</li>
      <li><strong>Coordinates:</strong> The values (x, y) that represent the position of a point on the coordinate plane.</li>
      <li><strong>Quadrants:</strong> The four regions formed by the x-axis and y-axis on the coordinate plane.</li>
      <li><strong>Distance Formula:</strong> The formula used to calculate the distance between two points on the coordinate plane.</li>
    </ul>
  </div>

  <hr>

  <div class="notes-section">
    <h2>Formulas</h2>
    <p><strong>Distance Formula:</strong> \(d = \sqrt{{(x2 - x1)^2 + (y2 - y1)^2}}\)</p>
  </div>

  <hr>

  <div class="notes-section">
    <h2>Example Problems</h2>
    <p><strong>Problem 1:</strong> Find the distance between points A(3, 4) and B(7, 2).</p>
    <p><strong>Solution:</strong> Using the distance formula:</p>
    <p class="problem-solution">\(d = \sqrt{{(7 - 3)^2 + (2 - 4)^2}} = \sqrt{{16 + 4}} = \sqrt{{20}}\)</p>

    <p><strong>Problem 2:</strong> Determine the coordinates of the point that is equidistant from (-2, 5) and (4, 1).</p>
    <p><strong>Solution:</strong> We can find the midpoint between the two given points:</p>
    <p class="problem-solution">\(x = \frac{{-2 + 4}}{2} = \frac{2}{2} = 1\)</p>
    <p class="problem-solution">\(y = \frac{{5 + 1}}{2} = \frac{6}{2} = 3\)</p>
    <p class="problem-solution">Therefore, the coordinates of the point are (1, 3).</p>
  </div>

  <hr>

  <div class="notes-section">
    <h2>Diagrams</h2>
    <img src="diagram1.jpg" alt="Diagram 1">
    <img src="diagram2.jpg" alt="Diagram 2">
    <img src="diagram3.jpg" alt="Diagram 3">
    <img src="diagram4.jpg" alt="Diagram 4">
    <img src="diagram5.jpg" alt="Diagram 5">
  </div>

</div>

</body>
</html>


for now generate me for {notes_topic} in {study_grade} at {curriculum_board} {indian_state}
'''

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=2000,
        temperature=0.5,
        top_p=1.0,
        n=1,
        stop=None,
        timeout=10
    )
    html_code = response.choices[0].text.strip()

    with open("templates/notes.html", 'w') as file:
            file.write(html_code)

if __name__ == '__main__':
    app.run(debug=True)
  #db