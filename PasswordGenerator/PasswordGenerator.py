import random
import string
import cherrypy


class PasswordGenerator:
    @cherrypy.expose
    def index(self):

        return self.render_page(password=None)

    def render_page(self, password):

        return f'''
            <html>
                <head>
                    <title>Generare Parolă</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f7f7f7;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                        }}
                        .container {{
                            background-color: white;
                            padding: 30px;
                            border-radius: 8px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            width: 400px;
                        }}
                        h2 {{
                            text-align: center;
                            color: #333;
                        }}
                        input[type="number"],
                        input[type="checkbox"] {{
                            margin: 10px 0;
                        }}
                        label {{
                            font-size: 14px;
                            color: #333;
                        }}
                        input[type="submit"], .copy-button {{
                            width: 100%;
                            padding: 10px;
                            font-size: 16px;
                            background-color: #007bff;
                            color: white;
                            border: none;
                            border-radius: 5px;
                            cursor: pointer;
                        }}
                        input[type="submit"]:hover,
                        .copy-button:hover {{
                            background-color: #0056b3;
                        }}
                        .password-display {{
                            font-size: 20px;
                            font-weight: bold;
                            text-align: center;
                            padding: 10px;
                            margin-bottom: 20px;
                            background-color: #e9ecef;
                            border-radius: 5px;
                        }}
                        .complexity-bar {{
                            margin-top: 10px;
                            height: 5px;
                            border-radius: 5px;
                        }}
                        .weak {{ background-color: red; }}
                        .medium {{ background-color: orange; }}
                        .strong {{ background-color: green; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2>Generator Parolă</h2>
                        <form method="post" action="generate_password">
                            Lungimea parolei: <input type="number" name="length" min="8" value="12" required><br><br>
                            Include caractere speciale: <input type="checkbox" name="special" checked><br>
                            Include cifre: <input type="checkbox" name="digits" checked><br>
                            Include litere mari: <input type="checkbox" name="uppercase" checked><br>
                            Include litere mici: <input type="checkbox" name="lowercase" checked><br><br>
                            <input type="submit" value="Generează Parolă">
                        </form>
                        {self.render_password(password)}
                    </div>
                </body>
            </html>
        '''

    def render_password(self, password):
        if not password:
            return ''


        complexity = self.calculate_complexity(password)

        return f'''
            <h3>Parola generată:</h3>
            <div class="password-display" id="passwordDisplay">{password}</div>
            <button class="copy-button" onclick="copyPassword()">Copiază Parola</button>
            <div class="complexity-bar {complexity['class']}" style="width: 100%"></div>
            <p style="text-align: center; color: {complexity['color']};">{complexity['label']}</p>
            <script>
                function copyPassword() {{
                    var password = document.getElementById("passwordDisplay").innerText;
                    navigator.clipboard.writeText(password).then(function() {{
                        alert('Parola a fost copiată!');
                    }});
                }}
            </script>
        '''

    @cherrypy.expose
    def generate_password(self, length=12, special=True, digits=True, uppercase=True, lowercase=True):
        length = int(length)
        special = special == 'on'
        digits = digits == 'on'
        uppercase = uppercase == 'on'
        lowercase = lowercase == 'on'

        characters = string.ascii_lowercase if lowercase else ''
        characters += string.ascii_uppercase if uppercase else ''
        characters += string.digits if digits else ''
        characters += string.punctuation if special else ''

        if not characters:
            return "Trebuie să selectezi cel puțin o opțiune!"

        password = ''.join(random.choice(characters) for _ in range(length))

        return self.render_page(password)

    def calculate_complexity(self, password):

        complexity = 0
        if len(password) >= 12:
            complexity += 1
        if any(c.isdigit() for c in password):
            complexity += 1
        if any(c.islower() for c in password):
            complexity += 1
        if any(c.isupper() for c in password):
            complexity += 1
        if any(c in string.punctuation for c in password):
            complexity += 1

        if complexity == 5:
            return {"label": "Foarte puternică", "class": "strong", "color": "green"}
        elif complexity >= 4:
            return {"label": "Puternică", "class": "strong", "color": "green"}
        elif complexity >= 3:
            return {"label": "Medie", "class": "medium", "color": "orange"}
        else:
            return {"label": "Slabă", "class": "weak", "color": "red"}


if __name__ == '__main__':
    cherrypy.quickstart(PasswordGenerator())

    #Cod pentru a rula: python PasswordGenerator.py

