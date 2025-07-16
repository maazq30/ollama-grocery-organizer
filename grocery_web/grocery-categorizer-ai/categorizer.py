import ollama
import os
from flask import Flask, request, render_template, send_file
from io import BytesIO #no need to dwn file locally does it 
app = Flask(__name__)
MODEL = "llama3.2"  



@app.route('/', methods=['GET', 'POST']) #imp line used in flask 
def index():
    categorized_text = None
    if request.method == 'POST':
        file = request.files.get('grocery_file') #file lega 
        if not file:
            return render_template('index.html', error="No file uploaded.")

        try:
            items = file.read().decode('utf-8').strip()

        #model creation add anything here you need to change here something 

            prompt = f"""         
You are an assistant that categorizes and sorts grocery items.
Here is a list of grocery items:
{items}
Please:
1. Categorize these items into appropriate categories such as Produce, Dairy, Meat, Bakery, Beverages, etc.
2. Sort the items alphabetically within each category.
3. Present the categorized list in a clear and organized manner, using bullet points or numbering.

IF THERE IS A NON-CATEGORIZED ITEM, CREATE ITS OWN NEW CATEGORY AND BASED ON THAT NEWLY CREATED CATEGORY, ASSIGN NEW ITEMS TO IT IF THEY MATCH.
            """

            response = ollama.generate(model=MODEL, prompt=prompt)
            categorized_text = response.get("response", "").strip()
            return render_template('index.html', result=categorized_text)  #sending data or presenting back on website
        except Exception as e:
            return render_template('index.html', error=str(e))  #error print krega

    return render_template('index.html')


@app.route('/download', methods=['POST']) # download the categorized file...... #wapas reroute krta hai to allow user to download 

def download():
    content = request.form.get('content')
    if not content:
        return "No content found", 400

    buffer = BytesIO()
    buffer.write(content.encode('utf-8'))  #convert into bytes and adds data into the file 
    buffer.seek(0)#first position i guess
    return send_file(buffer, as_attachment=True, download_name="categorized_grocery_list.txt", mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True)
