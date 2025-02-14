from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

class Todo:
    def __init__(self, id, title, description, done=False):
        self.id = id
        self.title = title
        self.description = description
        self.done = done

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done
        }

todos = [
    Todo(1, "Learn Flask", "Read Flask documentation and tutorials"),
    Todo(2, "Build a Flask app", "Create a simple Flask application"),
]

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/todos")
def get_todos():
    return render_template("todo.html", todos=todos)

@app.post("/todos")
def add_todos():
    title = request.form["title"]
    description = request.form["description"]
    id = todos[-1].id + 1
    todo = Todo(id, title, description)
    todos.append(todo)
    return render_template("todo.html", todos=todos)

@app.route("/todos/<int:id>", methods=["POST"])
def delete_todos(id):
    if request.form.get("_method") == "DELETE":
        todo = next((todo for todo in todos if todo.id == id), None)
        if todo:
            todos.remove(todo)
    return redirect(url_for('get_todos'))

@app.route("/todos/<int:id>/edit", methods=["GET", "POST"])
def edit_todos(id):
    todo = next((todo for todo in todos if todo.id == id), None)
    if request.method == "POST":
        todo.title = request.form["title"]
        todo.description = request.form["description"]
        return redirect(url_for('get_todos'))
    return render_template("edit.html", todo=todo)

if __name__ == "__main__":
    app.run(debug=True)