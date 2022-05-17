from flask import Flask, render_template, request, redirect, render_template_string
from ctypes import cdll
import backtracking
import maze
import minSpanningTree
import solver

width = 20
height = 20
gen_type = "backtracking"
generator = minSpanningTree.MinSpanningTreeGenerator(height, width)
my_maze = generator.generate()
answer = False

app = Flask(__name__)

@app.route('/')
def begin():
    return render_template("start.html")


@app.route('/Labyrinth')
def labyrinth():
    return render_template("labyrinth.html")

@app.route('/Labyrinth/start', methods = ['POST', 'GET'])
def lab_start():
    global answer
    answer = False
    if request.method == 'GET':
        return render_template("lab_start.html")
    if request.method == 'POST':
        if request.form['width'] == "" or request.form['height'] == "" or request.form['type'] == '':
            return "Not all arguments were provided"
        elif int(request.form['width']) > 75 or int(request.form['height']) > 75:
            return "Sorry, my maximum is 75(("
        else:
            print('Here')
            global width
            global height
            global gen_type
            width = int(request.form['width'])
            height = int(request.form['height'])
            gen_type = request.form['type']
            print(width, height, "yay")
            return redirect('/Labyrinth/gstart')

@app.route('/Labyrinth/gstart', methods = ['POST', 'GET'])
def lab_gstart():
    global generator
    global my_maze
    global height
    global width
    if gen_type == 'backtracking':
        generator = backtracking.BacktrackingGenerator(height, width)
    else:
        generator = minSpanningTree.MinSpanningTreeGenerator(height, width)
    my_maze = generator.generate()
    filename = './templates/lab_game.html'
    with open(filename, 'w') as file:
        my_maze.draw(file)
    return render_template('lab_gstart.html')

@app.route('/Labyrinth/game', methods = ['POST', 'GET'])
def lab_game():
    global my_maze
    global answer
    if request.method == 'GET':
        if answer:
            return redirect('/Labyrinth/victory')
        else:
            filename = './templates/lab_game.html'
            with open(filename, 'r') as file:
                source = file.readlines()
            return render_template_string(''.join(source))
    if request.method == "POST":
        if request.json['name'] == 'ArrowUp':
            answer = my_maze.move('w')
        if request.json['name'] == 'ArrowDown':
            answer = my_maze.move('s')
        if request.json['name'] == 'ArrowLeft':
            answer = my_maze.move('a')
        if request.json['name'] == 'ArrowRight':
            answer = my_maze.move('d')
        filename = './templates/lab_game.html'
        with open(filename, 'w') as file:
            my_maze.draw(file)
        return render_template('lab_start.html')

@app.route('/Labyrinth/victory')
def lab_victory():
    global answer
    answer = False
    return render_template("lab_victory.html")

@app.route('/Labyrinth/solution')
def lab_solution():
    global my_maze
    my_solver = solver.MazeSolver()
    filename = './templates/lab_solution.html'
    with open(filename, 'w') as file:
        my_solver.solve(my_maze).draw_solution(file)
    with open(filename, 'r') as file:
        source = file.readlines()
    return render_template_string(''.join(source))


@app.route('/Labyrinth/rules')
def lab_rules():
    return render_template("lab_rules.html")


@app.route('/KnightSurvive')
def knight():
    return render_template("knight.html")


@app.route('/KnightSurvive/start')
def start():
    return render_template("game.html")

@app.route('/KnightSurvive/rules')
def rules():
    return render_template("rules.html")

@app.route('/KnightSurvive/ongoing')
def ongoing():
    file = cdll.LoadLibrary("./libMainBuild.so")
    output = file.main()
    if (output == 0):
        return render_template("victory.html")
    else:
        return render_template("defeat.html")

