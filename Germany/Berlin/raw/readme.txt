Die Daten der Verkhersdetektion Berlin werden monatsweise als Stundenwerte der fahrspurgenauen Verkehrsdetektoren und aggregiert über die Richtungsquerschnitte der Straßen bereitgestellt. 

Jedes csv-Archiv enthält die folgenden Datenfelder:

Detektoren:

detid_15 - ID des Detektors (15-stellige Ziffer).
tag - Datum
stunde - Stunde des Tages für die die Messwerte ermittelt wurden (8 => 08:00 - 08:59).
qualitaet - gibt den Anteil der für die Stunde vorliegenden einwandfreien Messintervalle wieder: 1.0 = 100%. Stundenwerte mit weniger als 75% werden nicht berücksichtigt
q_kfz_det_hr - Anzahl aller Kraftfahrzeuge in der Stunde.
v_kfz_det_hr - Mittlere Geschwindigkeit [km/h] über alle Kraftfahrzeuge in der Stunde.
q_pkw_det_hr - Anzahl aller Pkw in der Stunde.
v_pkw_det_hr - Mittlere Geschwindigkeit [km/h] über alle Pkw in der Stunde.
q_lkw_det_hr - Anzahl aller Lkw in der Stunde.
v_lkw_det_hr - Mittlere Geschwindigkeit [km/h] über alle Lkw in der Stunde.


Messquerschnitte:

mq_name - ID des Messquerschnitts.
tag - Datum
stunde - Stunde des Tages für die die Messwerte ermittelt wurden (8 => 08:00 - 08:59).		
qualitaet  - Verfahrensbedingt ist dieser Wert immer 1.0, d.h. es lag ein gültiger Stundenwert für alle zu diesem Messquerschnitt gehörenden Detektoren vor. 
			Fehlen einzelne Detektoren wird kein Wert für den Messquerschnitt gebildet.
q_kfz_mq_hr - Anzahl aller Kraftfahrzeuge in der Stunde.
v_kfz_mq_hr - Mittlere Geschwindigkeit [km/h] über alle Kraftfahrzeuge in der Stunde.
q_pkw_mq_hr - Anzahl aller Pkw in der Stunde.
v_pkw_mq_hr - Mittlere Geschwindigkeit [km/h] über alle Pkw in der Stunde.
q_lkw_mq_hr -  Anzahl aller Lkw in der Stunde.
v_lkw_mq_hr - Mittlere Geschwindigkeit [km/h] über alle Lkw in der Stunde.



Hinweise: 
* Es kann zu geringen Abweichungen zwischen der Anzahl aller Kraftfahrzeuge (q_kfz_det_hr) und der Summe für PKW (q_pkw_det_hr) und LKW (q_lkw_det_hr) kommen. Dies resultiert aus Rundungsfehlern auf Grund des gewählten Verfahrens.
* Es werden nur Stundenwerte für die Detektoren gebildet, wenn für wenigstens 75% der Messintervalle einer Stunde gültige Daten vorliegen. Ist dies nicht der Fall, dann fehlt der entsprechende Stundenwert im csv-Archiv.
* Liegt für eine Stunde nicht für ALLE Detektoren eines Messquerschnitts ein gültiger Stundenwert vor, wird kein Stundenwert für den Messquerschnitt gebildet.



Die Verortung der Detektoren und die Zuordnung der einzelnen Detektoren zu einem richtungsbezogenen Messquerschnitt findet sich in der Datei Stammdaten_Verkehrsdetektion_Berlin.xlsx.

Dies enthält die folgenden Datenblätter:
(1) DET
Zuordnung der Detektor ID (DET_ID15) zur ID des Messquerschnitts (MQ_ID15). 
Die Spalte LANE enthält Informationen zur Lage der Fahrspur (HF_R - 1. Spur von rechts auf der Hauptfahrbahn, HR_2vr - 2. Spur von rechts auf der Hauptfahrbahn, ...).

(2) MQ 
Daten des Messquerschnitts mit folgenden Spalten:

MQ_ID15	- ID des Messquerschnitts.
MQ_SHORT_NAME - Kurzname des Messquerschnitts.
POSITION - Name der Straße.
POSITION_DETAIL	- Beschreibung des Straßenabschnitts.
DIRECTION - Fahrtziel
ORIENTATION	- Fahrtrichtung
X_GK4 - X-Koordinate (Gauß-Krüger-4)
Y_GK4 - Y-Koordinate (Gauß-Krüger-4)
ANZAHL_DET - Anzahl der zum Messquerschnitt gehörenden Detektoren.
