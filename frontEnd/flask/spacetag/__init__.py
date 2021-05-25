#!./venv/bin/python

from flask import Flask, render_template



# creates the app instance using the name of the module
app = Flask( __name__, template_folder='templates' )


print(__name__, " app created.") # DEBUG ONLY


# https://replit.com/talk/learn/Flask-Tutorial/36529
@app.route('/') # Route the Function
def main(): # Run the function
    x = 'String' # Set x to 'String'
    return render_template( 'index.html', x=x ) # Render the template with a variable

app.run(host='0.0.0.0', port=5000, debug=True) # Run the Application (in debug mode)
