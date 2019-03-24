# Report für SEW TEST
Das hier ist ein Report MD file

#flask-vue-crud
#Anwendungsentwicklung - Verwendung von APIs
Implementieren Sie eine REST-Schnittstelle mit Flask um eine einfache TODO-Liste abzubilden und diese über einen Vue.js Client anzuzeigen und bearbeiten zu können. Es ist möglich das vorhandene Beispiel (flask-vue-crud) zu benutzen und dieses anzupassen.

##Definieren Sie einen Test-Endpunkt auf localhost mit der Port Nummer 8080. Was müssen Sie dafür beim Flask-Server konfigurieren?
app.run(port=8080)
port im app run hinzufügen


##Implementieren Sie eine TODO-Liste mit Flask mit folgenden Elementen: {id, todo, assignee, done}. Was haben Sie geändert oder welche Elemente haben Sie neu definiert?
Refactor mit Match-Case in app.py
title -> todo
author -> assignee
read -> done
Book -> Todo
BOOKS -> TODOS
book -> todo

Die app.routes müssen geändert werden!

STRG F "price" alles mit price entfernen, beistriche nicht vergessen

charge methoden entfernen

app route zu remove_book hinzugefügt

Ich habe das Dictonary geändert. Die referenzen zu den dictonary variabeln und dem dictonary selbst in den methoden geändert.
Ich habe die app routes geändert.


##Bereiten Sie die grafische Oberfläche für eine einfache Erstellung, Anzeige, Löschung und Anpassung der TODOs vor. Welche Komponenten müssen dafür erstellt werden?

Änderung aller referencen von büchern auf todos, wir haben jetzt Todo beschreibung assigne und done statt den jeweilg unten angeführten
Refactor mit Match-Case in app.py
title -> todo
author -> assignee
read -> done
Book -> Todo
BOOKS -> TODOS
book -> todo

Purchase STR-F
Purchase entfernen

price entfernen


localhost port auf 8080 changen refrencen von büchern auf todo nach server file app routes

Books.vue umbennen und den router link ändern (router -> index.js) (Beim import und bei routes)


##Ermöglichen Sie die einfache Erweiterung der grafischen Oberfläche und beschreiben Sie notwendige Schritte um neue Komponenten zur Anmeldung oder persönlichen Definition von personenbezogenen TODOs zu ermöglichen.
Im index.js (router) die bennenung der route für alle oder nur für spezifischer user(zb mit userid) gestallten

##Wie würden Sie eine einfache Authentifizierung implementieren? Beschreiben Sie die notwendigen Schritte!


#Anwendungsentwicklung - Anforderungsmanagement und SW-Design
Passen Sie das bereitgestellte Beispiel (flask-vue-crud) soweit an, dass eine Verwendung der bestehenden API durch einen eigenen Python-Client ermöglicht wird. Veränderungen der definierten Schnittstelle sind so weit wie möglich zu vermeiden.

##Implementieren Sie einen Client in Python, der sich mit der vorhandenen Server-Einheit verbindet und die Daten in eine eigene JSON Struktur lädt.

##Was würden Sie bei der Server-API anders definieren, damit verschiedene Clients auf die angebotenenen Funktionen zugreifen könnten?
in app.run threading=true machen damit er neue threads spawnt und mehrere clients gleizeitig zulassen kann


#flask-vue-spa
#Softwareentwicklungsprozess - Verifikation und kontinuierliche Entwicklung
Schreiben Sie zu den funktionalen Anforderungen des bereitgestellten Beispiels (flask-vue-spa) entsprechende Testfälle um deren korrekte Implementierung überprüfen zu können.

##Welche Tools würden Sie einsetzen, und wie würden die entsprechenden Konfigurationsdateien aussehen? Erstellen Sie ein Konzept!
Ich würde in travis tox mit pytest und in travis cypress verwenden. pytest für unit tests und cypress für graphische tests, travis ist für die automatisierung

.travis.yml soll so aussehen:
language: python, node_js

install:
-   pip install tox-travis
script:
-   tox
-   cypress run



tox.ini mit ( in requrements soll alles was drinnen steht installiert werden.)

[tox]
envlist = py34

[testenv]
deps = -r requirements.txt
commands =
    pytest --cov=server --html=testreport.html --self-contained-html

[pytest]
testpaths = src/unittest/python
python_files = test_*.py
python_classes = Test

jetzt werden in pytest alle files mit der namens definition test_irgendetwas.py ausgeführt

##Bereiten Sie einen einfachen Test für den Aufruf der Random Funktion vor. Wie würden Sie diesen starten?
from server import api  <- api holen

@pytest.fixture
def client():
    api.app.testing = True   <- als testing
    client = api.app.test_client()  <- client var in der der test server is
    yield client   <- diesen cleint yielden


##Implementieren Sie einen einfachen grafischen Test. Worauf achten Sie dabei?
Das cypress case sensitiv ist
Das das cypress test file in cypress unter integration liegt und diesem muster entspricht name.spec.js

describe  den test  it  does  cy.something

##Definieren Sie eine Konfiguration mit TravisCI für eine kontinuierliche Integration. Was müssen Sie dabei für die Python Tests und was für die grafischen Tests vorsehen?
language: python, node_js

install:
-   pip install tox-travis
script:
-   tox
-   cypress run
Das alle requirements für die python tests installiert sind der server importet wird auf den diese tests laufen beim tox in -r requirements.txt drin(da auch cypress)
Bei den graphischen muss cypress installed und dan in travis ausgeführt werden.
Es müssen für die graphischen tests die language (hier node_js) angegeben seien. selbe für python tests mit python bei language

##Welche Tests würden Sie für die Grenzen der Random Funktion vorsehen?
Einen test der schaut ob es innerhalb der grenzen zurückkommt
einen über und einen unterhalb der grenzen
einen schauen ob ein int zurückkommt



































