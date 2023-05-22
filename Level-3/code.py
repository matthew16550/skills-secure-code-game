from flask import Flask, request  
from pathlib import Path

base_path = Path(__file__).parent.resolve()
assets_path = (base_path / 'assets').resolve()

def asset_path(path):
    # Kludge so CodeQL doesnt report false positive "Uncontrolled data used in path expression"
    # Alas CodeQL doesnt support the usual "noqa" comment (https://github.com/github/codeql/issues/11427)
    path = str(path)
    
    result = (base_path / path).resolve()
    if result.is_relative_to(assets_path) and result.is_file():
        return result
    return None

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    TaxPayer('foo', 'bar').get_tax_form_attachment(request.args["input"])
    TaxPayer('foo', 'bar').get_prof_picture(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

class TaxPayer:
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.prof_picture = None
        self.tax_form_attachment = None

    # returns the path of an optional profile picture that users can set        
    def get_prof_picture(self, path=None):
        # setting a profile picture is optional
        if not path:
            pass

        safe_path = asset_path(path)
        if not safe_path:
            return None

        picture = safe_path.read_bytes()

        # assume that image is returned on screen after this
        return str(safe_path)

    # returns the path of an attached tax form that every user should submit
    def get_tax_form_attachment(self, path=None):
        tax_data = None
        
        if not path:
            raise Exception("Error: Tax form is required for all users")
       
        safe_path = asset_path(path)
        if not safe_path:
            return None

        tax_data = safe_path.read_bytes()

        # assume that taxa data is returned on screen after this
        return str(safe_path)
