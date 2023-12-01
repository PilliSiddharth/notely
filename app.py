import os
import uuid
import openai
from markupsafe import Markup
from flask import Flask, request, render_template, send_from_directory, render_template_string
from pip._vendor import cachecontrol

app = Flask("Notely", template_folder='./templates', static_folder='./css')

openai.api_key = "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"

# Dictionary to store the generated notes content
notes_data = {}
timetable_data = {}

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

        # Generate a unique identifier (UUID) for the user
        user_id = str(uuid.uuid4())

        notes_html = generate_notes(curriculum_board=curriculum_board, indian_state=indian_state, study_grade=study_grade, notes_topic=notes_topic)

        # Store the generated notes content in the dictionary with user_id as the key
        notes_data[user_id] = notes_html

        return render_template('app.html', notes_there=True, user_id=user_id, loader=True)
    else:
        return render_template('app.html')
    

@app.route('/jee-simplify')
def jee_simplify_render():
    return render_template('jee_simplify.html', question=None, options=None, answer=None)


@app.route('/jee-simplify-post', methods=['POST'])
def jee_simplify():
    # Retrieve user input
    question = request.form['question']
    options = request.form['options'].split(',')

    prompt = f'''
You are notely, you can solve jee mains questions for any subject on maths, physics, and chemsitry and give the
option for which is the correct answer also you shoul give a brief solution on how you solved the question, basically 
explain like it were a 5th grade student you were explaining to and like i said the solution
should be so easy that even a 5th grade student should understand but make it long and use real 
life examples, make sure when you use any mathematical equations
have them in latex,

for now solve me for the question {question}, and these are the options: {options}
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
    raw_answer = response.choices[0].text.strip()
    answer = Markup(raw_answer.replace('\n', '<br>'))


    # Perform AI logic here (replace with your actual AI logic)
    # For now, just return a dummy answer
    # answer = "Dummy Answer"

    return render_template('jee_simplify.html', question=question, options=options, answer=answer)


@app.route('/neet-simplify')
def neet_simplify_render():
    return render_template('neet_simplify.html', question=None, options=None, answer=None)


@app.route('/neet-simplify-post', methods=['POST'])
def neet_simplify():
    # Retrieve user input
    question = request.form['question']
    options = request.form['options'].split(',')

    prompt = f'''
You are notely, you can solve neet questions for any subject on biology, physics, and chemsitry and give the
option for which is the correct answer also you shoul give a brief solution on how you solved the question, basically 
explain like it were a 5th grade student you were explaining to and like i said the solution
should be so easy that even a 5th grade student should understand but make it long and use real 
life examples, make sure when you use any mathematical equations
have them in latex,

for now solve me for the question {question}, and these are the options: {options}
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
    raw_answer = response.choices[0].text.strip()
    answer = Markup(raw_answer.replace('\n', '<br>'))


    # Perform AI logic here (replace with your actual AI logic)
    # For now, just return a dummy answer
    # answer = "Dummy Answer"

    return render_template('neet_simplify.html', question=question, options=options, answer=answer)


@app.route("/lesson-scheduler", methods=['GET', 'POST'])
def render_scheduler():
    if request.method == 'POST':

        curriculum_board = request.form.get('curriculum_board')
        indian_state = request.form.get('indian_state')
        study_grade = request.form.get('study_grade')
        notes_topic = request.form['notes-topic']

        # Generate a unique identifier (UUID) for the user
        user_id = str(uuid.uuid4())

        timetable_html = generate_timetable(curriculum_board=curriculum_board, indian_state=indian_state, study_grade=study_grade, notes_topic=notes_topic)

        # Store the generated notes content in the dictionary with user_id as the key
        timetable_data[user_id] = timetable_html

        return render_template('learn_scheduler.html', notes_there=True, user_id=user_id, loader=True)
    else:
        return render_template('learn_scheduler.html')
    

@app.route("/notes/<user_id>", methods=['GET', 'POST'])
def generated_notes(user_id):
    # Check if the user_id exists in the dictionary
    if user_id in notes_data:
        # Retrieve the notes content from the dictionary
        notes_html = notes_data[user_id]
        return render_template_string(notes_html)
    else:
        # If the user_id doesn't exist, return an error message or redirect to a different page
        return "Notes not found."


def generate_notes(curriculum_board, indian_state, study_grade, notes_topic):
    
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

    # ... (your existing code for generating the notes HTML)

    # with open(f"templates/notes/{filename}", 'w') as file:
    #     file.write(html_code)

    # Return the filename so it can be used in the "generated_notes" route
    return html_code


@app.route("/timetables/<user_id>", methods=['GET', 'POST'])
def generated_timetable(user_id):
    # Check if the user_id exists in the dictionary
    if user_id in timetable_data:
        # Retrieve the notes content from the dictionary
        timetable_html = timetable_data[user_id]
        return render_template_string(timetable_html)
    else:
        # If the user_id doesn't exist, return an error message or redirect to a different page
        return "Notes not found."


def generate_timetable(curriculum_board, indian_state, study_grade, notes_topic):
    
    prompt = f'''
You are notely, you can generate detailed and brief timetable that will help,
students to complete a chapter also make the topics indepth like everything, which means in a chapter every concept
and topic doesn't matter if its a sub topic or not with specific timeframes 
needed for each one and the entierty of time make
 you can make it yourself based on how much time is needed to get better in it
   use this html code template and change the necessary content needed: 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mathematics Workshop Timetable</title>
    <!-- Add Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>

    <div class="container mt-5">
        <h2 class="mb-4">Mathematics Workshop Timetable</h2>

        <table class="table">
            <thead>
                <tr>
                    <th>Day</th>
                    <th>Time</th>
                    <th>Topic</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td rowspan="3">Day 1</td>
                    <td>10:00 AM - 11:30 AM</td>
                    <td>Session 1: Introduction to Limits and Continuity</td>
                </tr>
                <tr>
                    <td>11:45 AM - 01:15 PM</td>
                    <td>Session 2: Definition of Derivatives and First Principles</td>
                </tr>
                <tr>
                    <td>02:00 PM - 04:30 PM</td>
                    <td>Session 3: Techniques of Differentiation - Power Rule, Product Rule, Quotient Rule</td>
                </tr>
                <tr>
                    <td rowspan="3">Day 2</td>
                    <td>10:00 AM - 11:30 AM</td>
                    <td>Session 4: Derivatives of Trigonometric Functions and their Inverses</td>
                </tr>
                <tr>
                    <td>11:45 AM - 01:15 PM</td>
                    <td>Session 5: Derivatives of Exponential and Logarithmic Functions</td>
                </tr>
                <tr>
                    <td>02:00 PM - 04:30 PM</td>
                    <td>Session 6: Chain Rule, Implicit Differentiation, and Logarithmic Differentiation</td>
                </tr>
                <tr>
                    <td rowspan="2">Day 3</td>
                    <td>10:00 AM - 11:30 AM</td>
                    <td>Session 7: Applications of Derivatives - Related Rates and Optimization</td>
                </tr>
                <tr>
                    <td>11:45 AM - 01:30 PM</td>
                    <td>Session 8: Applications of Derivatives - Curve Sketching and L'Hôpital's Rule</td>
                </tr>
                <tr>
                    <td>02:30 PM - 04:00 PM</td>
                    <td>Session 9: Review, Practice, and Q&A</td>
                </tr>
            </tbody>
        </table>


    </div>

    <!-- Add Bootstrap JS and Popper.js -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

    <script src="https://rawgit.com/eKoopmans/html2pdf/master/dist/html2pdf.bundle.js"></script>

    <script>
        // Function to download the timetable as a PDF
       
    </script>
</body>
</html>
```


for now generate me timetable for {notes_topic} in {study_grade} at {curriculum_board} {indian_state}
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

    # ... (your existing code for generating the notes HTML)

    # with open(f"templates/notes/{filename}", 'w') as file:
    #     file.write(html_code)

    # Return the filename so it can be used in the "generated_notes" route
    return html_code

if __name__ == '__main__':
    app.run(debug=True)
