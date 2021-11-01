# Meme generator
## Video Demo:  https://youtu.be/vc0DTkMHJqg
## Description:

### What is this project?

This is my final project for Harvard's CS50 (Introduction to Computer Science) course.

In a nutshell, the project comprises of a webpage that allows the user to input an image file (either an URL pointing to one, or a file uploaded by user) and define some text alongside with basic text formatting. The application will overlay the defined text on top of the input (base) image in a stylish (I hope) manner. This modified image sort of resembles a meme, hence the name. The app allows the user to download the modified image (meme).

<img width="937" alt="CS50 meme generator" src="https://user-images.githubusercontent.com/8441401/139600237-85dfceb8-fdde-466c-9eae-3cbb71be7e25.png">


### Setup

Prerequisites: pipenv installed (install e.g. with `pip install --user pipenv`)

1. Clone this repo
2. In the project root folder, run `pipenv install`. This installs and setups the virtual environment with the necessary dependencies
3. In the project root folder, run `pipenv run flask run`. This spins up a web server that will be serving the flask app. After the server is up and running, the flask app can typically be accessed at http://127.0.0.1:5000/

For the time being, the meme gen app is also hosted on Heroku and can be accessed here:
https://cs50-memegen.herokuapp.com/

### Description of the main files

- **app.py**: Contains the Flask application that renders the templates, calls make_meme endpoint to request for a modified image to be processed and finally serves the resulting image.
- **image_processor.py**: Contains the code taking care of obtaining and manipulating images. Image manipulation is done using Pillow (PIL) library for python.
- **utils.py**: Two utility functions related to serving the modified image (the output) to the web page.
- **html documents in templates folder**: layout.html sets the overall page layout. index.html extends the layout and contains the main content of the page.
- **styles.css in static folder**: Defines most of the CSS used in the pages (some is left in the html files).
- **scripts.js in static folder**: Contains javascript used on the page, e.g. for the slider and for making the application work in an async/ajax manner.
- **Pipfile and Pipfile.lock**: Files defining the environment, e.g. the dependencies.

#### Some design choices

1. Make the app work in asyncronous manner (e.g. click "Fetch" (from url) or "Generate" -> we stay on the same page, but the request is processed in the background)
2. Do not store anything on the server. No original nor modified images are persisted.
3. Make it relatively simple, both for the user and also internally. For example, font size is automatically adjusted to make the given text fit (simple for the user), but I didn't consider breaking long texts automatically to multiple lines (simple internally).
4. Where needed, reasonable default values are used to make the output pleasing (at least for typical kinds and sizes of images and texts)

### Possible gotchas

At first, the python requests module did not work out of the box within pipenv. It nagged that it wasn't able to find libcrypto and libssl files. As a workaround, I copied the libcrypto-1_1-x64.* and libssl-1_1-x64.* files from the python distribution's bin folder (mine was …\anaconda3\Library\bin) to corresponding virtualenv's \Script folder. After this, requests was happy.

However, I didn't bump into this issue anymore when I later `pipenv install`'ed the whole thing from scratch.


### TODO

- Go from print statements (for logging purposes) to actual logging
