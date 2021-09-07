from flask import Flask, flash, redirect, render_template, request, session

from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    """Show index.html"""

    return render_template("index.html")


@app.route("/user_inputs")
def user_inputs():
    """Show index.html"""

    return render_template("user_inputs.html")