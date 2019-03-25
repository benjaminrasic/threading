# Report: Anwendungsentwicklung - Verwendung von APIs

#### Definieren Sie einen Test-Endpunkt auf localhost mit der Port Nummer 8080. Was müssen Sie dafür beim Flask-Server konfigurieren?
Es musste in app.py in der Mainmethode Flask mit Parametern gestartet werden. Dort kann der Port 8080 angegeben werden. ``app.run(host='0.0.0.0', port=8080)``

#### Implementieren Sie eine TODO-Liste mit Flask mit folgenden Elementen: {id, todo, assignee, done}. Was haben Sie geändert oder welche Elemente haben Sie neu definiert?
Es wurde ein dictionary von dem vorhandenen Beispiel in app.py genommen und erstellt. Der Name ist TODOS. Dort wurden die einzelnen Attribute hinzugefügt. Zusätzlich wurden die in app.py vorhandenen Methoden kopiert und für die Todo Liste angepasst. Es können die Todos hinzugefügt, abgerufen und gelöscht werden. Dazu musste die Approute angepasst werden und die Methoden ``all_todos`` , ``single_todo`` und ``remove_todo`` mussten auf die Todo Liste angepasst werden.

#### Bereiten Sie die grafische Oberfläche für eine einfache Erstellung, Anzeige, Löschung und Anpassung der TODOs vor. Welche Komponenten müssen dafür erstellt werden?
Es muss ein Todo.vue erstellt werden. Dort muss eine Dynamische Tabelle erstellt werden, welche die Todos anzeigt. Anschließend wurden die Methoden aus Books.vue genommen, kopiert, und abgeändert, so dass diese das Schema der TODO Liste abdeckt. Zudem musste in index.js folgendes hinzugefügt werden:
``import Todos from '@/components/Todos';`` Außerdem wurde in index.js die Route folgendermaßen gesetzt:
``
{
      path: '/',
      name: 'Todos',
      component: Todos,
    }
    ``

#### Ermöglichen Sie die einfache Erweiterung der grafischen Oberfläche und beschreiben Sie notwendige Schritte um neue Komponenten zur Anmeldung oder persönlichen Definition von personenbezogenen TODOs zu ermöglichen
Dies ist bereits möglich, es müssen lediglich neue Vue Components hinzufügt werden. In der Abfrage in Javascript kann nach Asignees gefiltert werden. Für die neue Vue Komponente muss im index.js auch eine Route hinzugefügt werden. 
#### Wie würden Sie eine einfache Authentifizierung implementieren? Beschreiben Sie die notwendigen Schritte!

# Anwendungsentwicklung - Anforderungsmanagement und SW-Design

#### Implementieren Sie einen Client in Python, der sich mit der vorhandenen Server-Einheit verbindet und die Daten in eine eigene JSON Struktur lädt.
Es wurde ein einfacher Client in Python erstellt, welcher sich mit dem Server verbindet und die Todos aufruft und anschließend in ein JSON lädt.
``
    import json
    import requests
    
    if __name__ == "__main__":
        """
        Einfache Funktion, um sich mit der Servereinheit zu verbinden und anschließend
        die Antwort des Servers in ein JSON zu laden
        """
        reply = requests.get("http://localhost:8080/todos")
        daten = json.loads(reply.text)
``
    
#### Was würden Sie bei der Server-API anders definieren, damit verschiedene Clients auf die angebotenenen Funktionen zugreifen könnten?
Hierfür wurde CORS verwendet. CORS ist eine Technik, die Webbrowsern aber auch anderen Clients Cross Origin Requests ermöglicht. Dies wurde in app.py implementiert.
``
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
``

# Softwareentwicklungsprozess - Verifikation und kontinuierliche Entwicklung
#### Welche Tools würden Sie einsetzen, und wie würden die entsprechenden Konfigurationsdateien aussehen? Erstellen Sie ein Konzept!
TravisCI
Das Backend kann mit PyTest getestet werden. Dort kann der HTTP-Statuscode geprüft werden. Zum Testen des Frontends kann Cypress verwendet werden. Dazu muss Cypress lediglich mit ``npm install cypress`` Cypress initalisiert werden. Das ganze kann dann mit Tox gestartet werden und auch getestet werden. Dazu muss im tox.ini - File für die PyTests folgendes hinzugefügt werden: 
``
[pytest]
testpaths = src/test
python_files = test_*.py
python_classes = Test
``
für die Cypress Tests muss im tox.ini folgendes hinzugefügt werden:
``
[tox]
envlist = py36, cypress-dashboard, cypress-explore
``

Das kann anschließend noch auf TravisCI laufen gelassen werden. Dafür muss ein File mit dem Namen .travis.yml erstellt werden. Für die PyTests muss folgendes ins Travis-File geschrieben werden:
``
    - stage: Tox Test
        name: "Unit Tests"
        language: python
        python:
      - 3.6
      install: pip install tox-travis
      script: tox
``
Für die Cypress-Tests muss folgendes ins Travis-File geschrieben werden:
``
    - stage: Cypress Test
      name: "End to End testing Cypress"
      language: node_js
      node_js:
        - 10
      cache:
        npm: true
        directories:
          - ~/.npm
          - ~/.cache
          - node_modules
        node_js:
          - '8'
      install:
        - cd src/router
        - npm ci
      script:
        - npm run cy:run
``
#### Bereiten Sie einen einfachen Test für den Aufruf der Random Funktion vor. Wie würden Sie diesen starten?
Hierfür wurde ein PyTest erstellt, welcher die Randomfunktion aufruft, und anschließend den HTTP-Statuscode abfragt, welcher im bestel Fall 200 ist. Der Testcase sieht wie folgt aus:
``
def test_pingrandom(client):
    res = client.get('/api/random')
    assert res.status_code == 200
`` 
Gestartet werden kann dieser Test auf mehrere Arten. Ich würde, da es sich hierbei nur um einen einzelnen Test handelt, diesen direkt starten mit: 
``
pytest unittest/
``
#### Implementieren Sie einen einfachen grafischen Test. Worauf achten Sie dabei?
Hierfür wurde ein Testfile erstellt. Dort wurde ein Testcase erstellt, welcher die Seite besucht und einer, welche überprüft, ob der Button Klickbar ist. Der Test zur Überprüfung des Buttons sieht folgendermaßen aus:
``
describe('Test', function() {
    it('Checking if Button clickable', function(){
        cy.visit('http://localhost:5000/')
        cy.contains('New Random Number').click()
    })
})
``
#### Definieren Sie eine Konfiguration mit TravisCI für eine kontinuierliche Integration. Was müssen Sie dabei für die Python Tests und was für die grafischen Tests vorsehen?
Dafür muss ein File mit dem Namen .travis.yml erstellt werden. Für die PyTests muss folgendes ins Travis-File geschrieben werden:
``
    - stage: Tox Test
        name: "Unit Tests"
        language: python
        python:
      - 3.6
      install: pip install tox-travis
      script: tox
``
Für die Cypress-Tests muss folgendes ins Travis-File geschrieben werden:
``
    - stage: Cypress Test
      name: "End to End testing Cypress"
      language: node_js
      node_js:
        - 10
      cache:
        npm: true
        directories:
          - ~/.npm
          - ~/.cache
          - node_modules
        node_js:
          - '8'
      install:
        - cd src/router
        - npm ci
      script:
        - npm run cy:run
``
#### Welche Tests würden Sie für die Grenzen der Random Funktion vorsehen?
Ich würde Unittests mit PyTest verwenden. So kann man überprüfen, ob die Obergrenze und die Untergrenze eingehalten wird. 