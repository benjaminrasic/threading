# "Restful User-Service"

## Aufgabenstellung
Die detaillierte [Aufgabenstellung](TASK.md) beschreibt die notwendigen Schritte zur Realisierung.

## Implementierung
Die angegebene Aufgabenstellung wurde mittels Flask, SQLLite und Vue.js umgesetzt. Getestet werden die einzelnen Teile
mit Flask-Unit Tests und CypressIO. Automatisiert wird die Anwendung mittels TravisCI unter dem Deployer Tox.

Die Umsetzung in Python wurde dabei auf zwei Files rest_server.py und api.py augeteilt. Dabei bietet rest_server.py
die Klasse Server, die die Methoden des Servers darstellen. Hier werden mittels Methoden die CRUD Funktionalität zur
Datenbank zur Verfügung gestellt. Die File api.py bietet die Schnittstelle zum Server und die Implementierung von Flask.

Die Client Anwendung wurde zusätzlich mittels Vue.js umgesetzt, dazu wurden einfache Bootstrap Elemente verwendet.
Kommuniziert wird dabei zum Server mittels Ajax Requests. Das Front- und Backend des Clients befindet sich großteils
File User.vue.

### 1. TODO.md erstellen
Hier finden Sie die aktuelle [TODO Liste](TODO.md) .

### 2. Git Repository forken & Upstream pushen
* Repository auf Github-Website des gewünschten Projektes forken (Über Fork-Button)
* Geforktes (eigenes) Repository clonen und als locales Repository adden
* Im localen Repo Upstream adden: `git remote add upstream https://github.com/ORIGINAL_OWNER/ORIGINAL_REPOSITORY.git`
* Überprüfen, ob Upstream geaddet wurde: `git remote -v`

### 3. Synching a Fork
* Im geforkten Repo: `git fetch upstream`
* Local master auschecken: `git checkout master`
* Merge Änderungen into local master: `git merge upstream/master`
* Oder: `git push upstream`

### 4. Tox Konfiguration & Ausführung
* Tox Installation: `pip install tox`
* [Tox.ini](tox.ini) File wie im Beispiel konfigurieren. Wichtig hierbei ist, dass man die benötigten Requirements
festhält (im BSP in einem eigenen File) und das die Versionen und Paths richtig gesetzt sind. <br>
Unter commands wurde außerdem bruch auf server geändert, damit die Coverage der Tests nach dem Ausführen von Tox ausgegeben wird.
* Requirements.txt:
```requirements.txt
    pytest
    pytest-cov
    flask
    flask-restful
    pytest-flask
    pytest-html
    flask-cors
    flask-httpauth
```
* In der Console, im Projektordner, `tox` ausführen, um Tox zu starten.
* <b>Achtung!</b> Werden die Requirements geändert, kann es notwendig sein den Tox-Ordner zu löschen und tox neu auszuführen.


### 5. Server Implementierung
Der Server wurde in Form einer Klasse, vollkommen abgetrennt von der API, erstellt. Dieser bietet mittels Funktionen die Schnittstelle
zur Datenbank und überprüft die übergebenen Daten auf Korrektheit bevor diese in die Datenbank geschrieben werden. Der Server bietet
also alle CRUD Funktionen, die die API später benötigen wird, und kommuniziert als einziger mit der Datenbank. Der Server befindet sich in
folgendem [File](src/main/python/server/rest_server.py) . <br>
Um mit der Datenbank zu kommunizieren werden die Daten in JSON-Formate geschrieben und in die Datenbank gespeichert. Bei GET werden
werden dann die JSON-Dateien wieder herausgelesen und im Programm in ein Dictionary gespeichert, um weiter verarbeitet zu werden.
Für diese Funktionalitäten wurden die Funktionen `json.loads()` und `json.dumps()` verwendet. <br>
Die Überprüfung der übergebenen Werte findet ebenfalls hier mittels Regexes und if Unterscheidungen statt. <br>
Die Datenbank wird wie bereits erwähnt ebenfalls nur hier verwendet, als Beispiel für die Kommunikation wird im folgenden die Methode gezeigt,
um alle User zu bekommen:
```getAllMembers() Methode
    # getAllMembers()
    # Ermöglicht es die Daten aller Benutzer zu bekommen
    def getAllMembers(self):
        conn = sqlite3.connect(self.dbname)
        c = conn.cursor()

        c.execute("SELECT count(*) FROM users")
        count = int(c.fetchone()[0])

        c.execute("SELECT * FROM users")
        obj = c.fetchall()

        ausgabe = "["
        for i in range(0, count):
            ausgabe += obj[i][0]
            if i != count - 1:
                ausgabe += ","
        ausgabe += "]"

        conn.commit()
        conn.close()
        return ausgabe
```


### 6. Flask-API Implementierung
Die API wurde mittels Flask umgesetzt und bietet die Rest Schnittstelle zum Server. Sie führt die Methoden des Servers je nachdem welche URL
aufgerufen, wurde auf. Sie beinhaltet außerdem auch die Methoden und Konfigurationen (wie CORS), die später vom Vue.js Client benötigt werden.
Die Daten werden dabei über "request", also Parameter, oder direkt in der URL angegeben. Zum Starten des Servers ruft man einfach `python api.py`
aus, dann startet sich der Server auf localhost und man kann diesen nutzen. Die API kann [hier](src/main/python/server/api.py) gefunden werden. <br>
Die Konfiguration für das Api-File wird im Folgenden kurz gezeigt, dabei wird eine Instanz des Servers erstellt, welche den Datenbanknamen bzw. der Pfad
übergeben bekommt. Dies ist notwendig da beim Testing später der Path zur Datenbank ein anderer ist bzw. man leicht den Datenbankname/Pfad ändern kann,
zum Beispiel für Testingdatenbanken oder bei Änderungen.
```api.py
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)
rest = rest_server.Server("UserDatabase") # Server
```

Die einzelnen Methoden sind dann wie bereits beschrieben wie folgt aufgebaut:
```api.py
@app.route("/user/add/<string:email>/")
def webAddMember(email):
    username = request.args.get('name', default=1, type=str)
    picture = request.args.get('picture', default=1, type=str)
    return rest.addMember(email, username, picture)

# Für VUE.JS Client
@app.route("/user/add/", methods=["POST"])
def webAddMemberPost():
    post_data = request.get_json()
    email1 = request.get_json().get('email')
    email = post_data.get('email')
    username = post_data.get('username')
    picture = post_data.get('picture')
    return rest.addMember(email, username, picture)
```
Bei diesen Methoden wird immer zwischen einer Implementierung nur über die URL und einer über die einzelnen HTTP Methoden (z.B. POST) unterschieden. Im
angeführten Code wird mit `@app.route` die URL der Methode und die HTTP-Methoden angegeben.<br>
Ausführung: Zum Ausführen der API muss diesen mit `python api.py` ausgeführt werden, damit wird auch der Server gestartet.


### 7. Python Testing
Getestet wurde die Funktionalität von API und Server mittels "pytest". Dazu benötigt man zunächst eine Konfiguration für das Testfile:
```test_server.py
    import pytest
    from server import api

    @pytest.fixture
    def client():
        api.app.testing = True
        api.setTestingMode() # Methode um Path für Tox zu setzen
        client = api.app.test_client()
        yield client
```

Mit `api.app.testing = True` wird der Testingmodus von Flask aktiviert, der unter anderem verständlichere Fehlermeldungen bietet. Danach holt man sich mit "app.test_client()" einen
Test-Client der App. Beispiel für einen Test:

```test_server.py
    def test_getExistingUser(client):
        client.get('/user/deleteUser/mailx@m.com/')
        client.get('/user/add/mailx@m.com/?name=paul&picture=https://bild.com/bild.svg')
        res = client.get('/user/get/mailx@m.com/')
        client.get('/user/deleteUser/mailx@m.com/')
        assert res.status_code == 200
        assert b'Username: paul, Email: mailx@m.com, Picture: https://bild.com/bild.svg' in res.data
```

Im angegebenen Beispiel wird ausschließlich mittels "get" Methode getestet. Die Methoden bekommen über die Parameter immer den Testclient und können mittels diesem die Funktionen über die URL ausführen.
Getestet wird dabei sowohl der `status_code` als auch die `data` des Ergebnisses der Anfrage als Bit. Das gesamte Testfile finden Sie [hier](src/unittest/GK/test_server.py) .


### 8. Vue.js Konfiguration
* Zunächst NodeJS am System installieren (sofern notwendig)
* Im Projektordner unter `src/main/python/client` VueJS installieren; `npm install -g vue-cli@2.9.3`
* VueJs in diesem Ordner initialisieren: `vue init wepback` <br>
`? Generate project in current directory? Yes` <br>
`? Project name <name>` <br>
`? Project description <description>` <br>
`? Author <email>` <br>
`? Vue build Runtime+Compiler` <br>
`? Install vue-router? Yes` <br>
`? Use ESLint to lint your code? Airbnb` <br>
`? Set up unit tests No` <br>
`? Setup e2e tests with Nightwatch? No` <br>
`? Should we run 'npm install' for you after the project has been created? npm` <br>
* Axios installieren, um später auf die REST-Schnittstelle zugreifen zu können. `npm install --save axios`
* Mit `npm run dev` in `src/main/python/client/client` ausführen, um den Client zu starten.
* Vuejs Client ausführen: Im Vue.js Ordner `npm run dev` ausführen.


### 9. Vue.js Implementierung
* Nun erstellt man eine neue Componente im Vue.js Ordner unter `src/components` mit dem Namen `User.vue`
* Dieses File muss nun unter [src/router/index.js](src/main/python/client/client/src/router/index.js) eingebunden werden.
Damit wird festgelegt, dass die User.vue auf localhost unter dem Path "/" erreicht werden kann.
* Um später Bootstrap verwenden zu können, muss dieses im [main.js](src/main/python/client/client/src/main.js) importiert werden.
* Das [User.vue](src/main/python/client/client/src/components/User.vue) File teilt sich nun in zwei Bereiche:
    - Den HTML Teil, der das Frontend darstellt.
    Mit `v-model` wird einem Element ein Name gegeben, welcher später im Script zum Auslesen der Informationen gegeben werden kann. <br>
    Mit `v-on:click` oder `@onlick` kann einem Element (z.B. Button) das Aufrufen einer Funktion aufgetragen werden. <br>
    Mit `v-for` kann eine For-Schleife innerhalb eines HTML Elemtns (z.B. Tabelle) durchgeführt werden.
    Mit `v-if` kann eine IF-Unterscheidung innerhalb eines Elemtens (z.B. Component) durchgeführt werden.

    Für die Alerts wurde eine zusätzliche Componente mit dem Namen `Alert.vue` erstellt:
    ```Alert.vue
    <template>
      <div>
        <b-alert variant="success" show>{{ message }}</b-alert>
        <br>
      </div>
    </template>

    <script>
    export default {
      props: ['message'],
    };
    </script>
    ```

    - Den NodeJs Teil, der das Backend darstellt.
    Mit `this.name` kann der Inhalt eines zuvor mit `v-model` bezeichneten Elements ausgelesen werden. <br>
    Mit `axios.get/post/put/delete` werden mit übergebenen Path und wenn benötigt übergebenen JSON Element die Anfragen an den Server gesendet. <br>


### 10. Vue.js Testing - Cypress.io
* Der zuvor erstellte Vue.js Client soll nun mittels Cypress.io getestet werden. Dazu müssen Client und Server gestartet sein. Die Testcases wurden wie folgt geschrieben, dabei werden alle Funktionen der Website sowie das Listing zum Client und Server getestet:
* Cypress starten: ` ./node_modules/.bin/cypress open`
* Im folgenden wird ein Beispiel für ein solchen Test gezeigt:
```
describe('Add User Testing', function() {
  it('adds a new User', function() {
    cy.visit('http://localhost:8080')

	cy.get('#inputName').type('Maxi Cypress').should('have.value', 'Maxi Cypress')
	cy.get('#inputEmail').type('mcypress@gmail.com').should('have.value', 'mcypress@gmail.com')
	cy.get('#inputPicture').type('https://cypress.bild/bild.png').should('have.value', 'https://cypress.bild/bild.png')

	cy.contains('button', 'Add User').click()

	cy.contains('tr', 'Maxi Cypress')
  })
})
```
Mit `cy.visit` kann eine URL besucht werden. <br>
Mit `cy.get` kann man sich ein Element auf der Website suchen (z.B. über die ID) <br>
Mit `.type` kann etwas in ein Inputfeld eingegeben werden, mit `.should` kann diese Eingabe dann überprüft werden. <br>
Mit `cy.contains` kann das vorhandensein eines Elements auf der Website geprüft sein. <br>
Mit `.click` kann ein gefundenes Element geklickt werden. <br>

### 11. Travis Konfiguration & Verwendung
* Im Root Verzeichnis des Projektordners muss zunächst das [tarvis.yml](.tarvis.yml) erstellt werden:
```.travis.yml
sudo: false
language: python
python:
  - "3.6"
install: pip install tox-travis
script: tox
```
* Danach meldet man sich auf https://travis-ci.com/ an und verbindet seinen Github-Account mit Travis.
* Nun gibt man Travis die Berechtigung auf das Github Repository zuzugreifen.
* Zuletzt startet man unter dem gegebenen Link den Builtvorgang und Travis sollte so aussehen:

![Travis.PNG](Dokumentation/Travis.PNG)

#### Cypress mit Travis
* Um auch das Cypress Testing durch Travis ausführen zu lassen, kann Cypress im Client Ordner installiert werden.
* Das [tarvis.yml](.tarvis.yml) wurde darüber hinaus angepasst.

### 12. Desktop Client Application - PyQT5
* PyQT5 installieren : `pip3 install pyqt5`
* PyQT Tools installieren: `pip3 install PyQt5-tools`
* Designer kann hier gefunden werden: `Programs\Python\Python36\Lib\site-packages\pyqt5-tools`
* Request installieren: `pip install requests --user`
* Mittels PYQT Elementen und dann Request Anfragen den Client umsetzen, dieser kann [hier](src/main/python/client/pyqt_client.py) gefunden werden.
* Ausführen: `python pyqt_client.py`
* PyQT Grundkondigurationen:
```
def __init__(self):
    super().__init__()
    self.title = 'PyQT REST Client'
    self.left = 0
    self.top = 0
    self.width = 600
    self.height = 400
    self.url = "http://127.0.0.1:5000/user"
    self.initUI()

 def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Draw Elements
        self.createInputLayout()
        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.horizontalGroupBox)
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # connect button to function on_click
        self.add.clicked.connect(self.on_click_add)
        self.update.clicked.connect(self.on_click_update)

        # Show widget
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
```

### 13. Basic Authentification
Alle CRUD Funktionen sollen authentifiziert werden, der Benutzer muss sich also
vor dem Benutzen dieser anmelden. Normale Benutzer dürfen nur alle anderen Nutzer sehen.
Neue User hinzufügen, Aktive updaten oder löschen kann nur ein Admin. <br>
GK: mit HTTP -> Digest auf bestehende User-DB (mind. SHA256 -> PW-Hash) <br>
EK: OAuth <br>

### 14. Deployment
GK: Local <br>
EK: Heroku, Zertifika-HTTPS <br>

#### Heroku
* Zunächst muss ein Heroku-Account erstellt und die Heroku CLI heruntergeladen werden.
* Nun wird Online (Auch in der Console möglich) das Projekt auf der Herokuseite erstellt.
* Nun führt man in der Console `heroku login` aus und loggt sich im gestarteten Browser Fenster ein.
* Mittels `heroku git:clone -a simple-user-database` wird das Repository geclont. (Danach in den Ordner `cd simple-user-database`)
* Nun wurde Gunicorn installiert: `pip install gunicorn`
* Mit `pip freeze > requirements.txt` werden alle notwendigen Dependencies in requirements.txt
* Nun wurde das Procfile erstellt, nachdem Heroku dann die Application startet. Wichtig
bei diesem ist, dass der Pythonpath angegben wird und auch mögliche Unterordner. Außerdem
darf das Procfile keinen Dateityp haben (kein .txt): <br>
`web: env PYTHONPATH=$PYTHONPATH:$PWD/src/main/python gunicorn server.api:app`
* Außerdem war folgender Befehl, zum Setzen der im Procfile verwendeten Definitionen notwendig:
`heroku ps:scale web=1`
* Bei jeder Änderung werden nun folgende drei Befehle ausgeführt:
    * `git add .`
    * `git commit -am "make it better"`
    * `git push heroku master`

## Quellen
- Flask: <br>
https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example <br>
https://pythonspot.com/flask-web-app-with-python/ <br>

- Flask Testing: <br>
http://flask.pocoo.org/docs/1.0/testing/ <br>

- Tox: <br>
https://tox.readthedocs.io/en/latest/ <br>

- SQLite: <br>
https://docs.python.org/3/library/sqlite3.html <br>
https://pythonspot.com/en/python-database-programming-sqlite-tutorial/ <br>
https://realpython.com/python-json/ <br>

- Vue.js: <br>
https://vuejs.org/v2/guide/ <br>
https://testdriven.io/developing-a-single-page-app-with-flask-and-vuejs <br>

- PyQT: <br>
http://pyqt.sourceforge.net/Docs/PyQt5/installation.html <br>
https://pythonspot.com/pyqt5-table/ <br>
https://build-system.fman.io/pyqt5-tutorial <br>
https://likegeeks.com/pyqt5-tutorial/ <br>
https://data-flair.training/blogs/python-pyqt5-tutorial/ <br>
https://pythonspot.com/pyqt5-textbox-example/ <br>
https://www.tutorialspoint.com/pyqt/pyqt_qmessagebox.htm <br>

- Github Forken: <br>
https://help.github.com/articles/syncing-a-fork/ <br>
https://help.github.com/articles/configuring-a-remote-for-a-fork/ <br>

- Cypress.io: <br>
https://docs.cypress.io/guides/getting-started/writing-your-first-test.html#Step-4-Make-an-assertion <br>

- Authentication: <br>
http://flask.pocoo.org/snippets/31/ <br>
https://flask-httpauth.readthedocs.io/en/latest/ <br>
http://flask.pocoo.org/snippets/8/ <br>
http://docs.python-requests.org/en/master/user/authentication/ <br>
https://manpages.debian.org/testing/python-flask-httpauth/flask-httpauth.1#panels <br>
https://github.com/miguelgrinberg/Flask-HTTPAuth <br>
https://github.com/miguelgrinberg/Flask-HTTPAuth/blob/master/flask_httpauth.py <br>
https://realpython.com/token-based-authentication-with-flask/ <br>
https://medium.com/codingthesmartway-com-blog/vue-js-2-vue-resource-real-world-vue-application-with-external-api-access-c3de83f25c00 <br>
https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/digest <br>
https://flask-oauthlib.readthedocs.io/en/latest/oauth2.html <br>
https://github.com/inorganik/digest-auth-request <br>
https://blog.sqreen.com/authentication-best-practices-vue/ <br>
http://jasonwatmore.com/post/2018/09/21/vuejs-basic-http-authentication-tutorial-example <br>
https://forum.vuejs.org/t/im-trying-to-make-authentication-and-i-get-an-error/30983 <br>
https://alligator.io/vuejs/intro-to-vuex/ <br>
https://github.com/axios/axios <br>
https://kapeli.com/cheat_sheets/Axios.docset/Contents/Resources/Documents/index <br>
https://vuex.vuejs.org/guide/getters.html <br>
https://stackoverflow.com/questions/47814626/vue-js-and-vuex-this-store-is-undefined <br>

- SH256: <br>
https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/digest <br>

- Heroku: <br>
https://devcenter.heroku.com/articles/getting-started-with-python#set-up <br>
https://medium.com/the-andela-way/deploying-a-python-flask-app-to-heroku-41250bda27d0 <br>
https://stackoverflow.com/questions/41804507/h14-error-in-heroku-no-web-processes-running <br>
https://help.heroku.com/W23OAFGK/why-am-i-seeing-couldn-t-find-that-process-type-when-trying-to-scale-dynos <br>
http://blog.sionide21.com/posts/2014/01/managing-pythonpath-on-heroku/ <br>