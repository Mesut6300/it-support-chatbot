from rasa_sdk import Action, Tracker                         # Basis-Klassen für Actions
from rasa_sdk.executor import CollectingDispatcher           # Bot-Antworten senden
from rasa_sdk.events import SlotSet, ActiveLoop, EventType   # Slots & Formularsteuerung
from rasa_sdk.events import UserUtteranceReverted            # Eingabe zurücksetzen (z.B. bei Fallback)
from typing import Any, Text, Dict, List                     # Typannotationen


class ActionCheckService(Action):  # Erbt von der Action-Klasse von Rasa (Basis für alle benutzerdefinierten Aktionen)

    def name(self):
        # Name der Action, unter diesem Namen wird sie dann in die domain referenziert
        return "action_check_service"

    def run(self, dispatcher, tracker, domain):
        # dispatcher: wird genutzt, um z.B. eine Nachricht an den Nutzer zu senden
        # tracker: enthält Infos zum bisherigen Gespräch (z.B. letzte User-Nachricht sowie gesetzte Slots)
        # domain: enthält die Domain-Konfiguration (nicht verwendet, aber vorgeschrieben)

        # Holt die letzte User-Nachricht (alles klein geschrieben für einfacheren Vergleich)
        user_message = tracker.latest_message.get("text", "").lower()

        # Holt den aktuell gespeicherten Wert aus dem Slot "service_type", falls vorhanden
        service_type = tracker.get_slot("service_type")

        # Wenn allgemeine Service-Frage erkannt wird
        if (
            "was bieten sie an" in user_message
            or "was sind ihre services" in user_message
            or "welche dienstleistungen gibt es" in user_message
        ):
            dispatcher.utter_message(
                text="💼 Wir bieten IT-Support, Netzwerkinstallationen und Softwareentwicklung an. Was interessiert dich?"
            )

        # Wenn das Wort "cloud" erkannt wird
        elif "cloud" in user_message:
            dispatcher.utter_message(
                text="☁️ Wir bieten aktuell keine Cloudlösungen an, aber vielleicht in Zukunft!"
            )

        # Wenn der Nutzer nach Software oder Entwicklung fragt
        elif "software" in user_message or "entwick" in user_message:
            dispatcher.utter_message(
                text="🖥️ Ja, wir entwickeln individuelle Softwarelösungen von Apps bis hin zu maßgeschneiderten Tools."
            )

        # Wenn das Wort "support" erkannt wird
        elif "support" in user_message:
            dispatcher.utter_message(
                text="👨‍💻 Klar, unser IT-Support hilft dir bei technischen Problemen, Systemeinrichtung und mehr."
            )

        # Wenn das Wort "netz" erkannt wird
        elif "netz" in user_message:
            dispatcher.utter_message(
                text="🌐 Natürlich! Wir übernehmen Netzwerkinstallationen für Zuhause und Unternehmen – zuverlässig und schnell."
            )

        # Fallback-Antwort, wenn keine spezifische Erkennung greift
        else:
            dispatcher.utter_message(
                text="💼 Wir bieten IT-Support, Netzwerkinstallationen und Softwareentwicklung an. Was interessiert dich?"
            )

        # Rückgabe einer SlotSet-Event-Liste (Sie kann später genutzt werden, um z.B. den Slot "service_type" zu setzen oder zu tracken)
        return [SlotSet("service_type", service_type)]


class ActionDefaultFallback(Action):                                                                                                         # Definiert den Namen der Action, wie er in der domain.yml referenziert wird
    def name(self) -> str:
        return "action_default_fallback"

    # Methode wird asynchron aufgerufen, wenn der Bot etwas nicht versteht
    async def run(self, dispatcher, tracker, domain):
        # Nachricht, die dem Nutzer angezeigt wird, wenn z.B. seine Eingabe nicht verstanden wurde
        message = "❓ Ich bin mir nicht sicher, was du meinst. Meintest du vielleicht:"

        # Drei Buttons mit Vorschlägen (helfen dem Nutzer weiter und verbessern somit die User Experience)
        buttons = [
            {
                "title": "📅 Einen Termin buchen",       # Text auf dem Button
                "payload": "/book_appointment"           # Intent, der beim Klick ausgelöst wird
            },
            {
                "title": "📞 Kontakt aufnehmen",
                "payload": "/contact"
            },
            {
                "title": "🖥️ Unsere Leistungen",
                "payload": "/services"
            }
        ]

        # Nachricht samt Buttons wird ausgegeben
        dispatcher.utter_message(text=message, buttons=buttons)

        # Rückgabe eines Events: Die letzte Nutzereingabe wird verworfen (der Bot "vergisst" sie)
        # Sinnvoll, weil die Eingabe nicht verstanden wurde und somit nicht weiterverarbeitet werden soll
        return [UserUtteranceReverted()]


class ActionHandleComplaint(Action):
    # Der Name der Action, so wie er in der domain verwendet wird
    def name(self):
        return "action_handle_complaint"

    # Die Methode, die ausgeführt wird, wenn die Action ausgelöst wird
    def run(self, dispatcher, tracker, domain):
        # Bot antwortet empathisch und zeigt somit auch Verständnis für das Problem
        dispatcher.utter_message(
            text="😔 Es tut mir leid, dass du ein Problem hattest. Ich werde das Feedback weiterleiten."
        )

        # Es werden keine Slots gesetzt und keine weiteren Aktionen durchgeführt
        return []


class ActionCollectFeedback(Action):
    # Der Name der Action, muss exakt so in der domain eingetragen werden
    def name(self):
        return "action_collect_feedback"

    # Die Methode wird aufgerufen, wenn der Intent (z.B. "give_feedback") mit dieser Action verknüpft ist
    def run(self, dispatcher, tracker, domain):
        # Der Bot reagiert freundlich und bedankt sich -> schafft Vertrauen
        dispatcher.utter_message(
            text="🙏 Vielen Dank für dein Feedback! Wir wissen das sehr zu schätzen."
        )

        # Es wird kein Slot gesetzt und kein weiteres Event ausgelöst
        return []


class ActionBookAppointment(Action):
    # Rückgabe des Action-Namens, dieser wird in domain referenziert
    def name(self):
        return "action_book_appointment"

    # Methode wird aufgerufen, wenn die Action durch z.B. durch eine Regel oder Story aktiviert wird
    def run(self, dispatcher, tracker, domain):
        # Bot antwortet freundlich und bestätigt somit die Aufnahme der Anfrage
        dispatcher.utter_message(
            text="📅 Kein Problem! Ich habe deine Anfrage aufgenommen. Wir melden uns zeitnah zur Terminbestätigung."
        )

        # Es werden keine Slots gesetzt und keine Daten gespeichert, die Funktion dient nur rein der Rückmeldung
        return []


class ValidateAppointmentForm(Action):
    # Name der Action, wie er in der domain und rules sowie stories verwendet wird
    def name(self) -> str:
        return "validate_appointment_form"

    # Die Methode wird aufgerufen, wenn der Bot überprüfen soll, ob z.B. der Slotwert gültig ist
    def run(self, dispatcher, tracker, domain):
        import re  # Die Regex-Bibliothek wird importiert zur Formatprüfung

        # Holt den aktuellen Wert aus dem Slot "appointment_time"
        time = tracker.get_slot("appointment_time")

        # Prüft, ob überhaupt ein Wert vorliegt und ob das Format auch nicht stimmt
        if time and not re.match(r"^(?:[01]?\d|2[0-3]):[0-5]\d$", time):
            # Wenn die Eingabe ungültig ist, wird eine entsprechende Nachricht gesendet
            dispatcher.utter_message(
                text="🕒 Die Uhrzeit scheint nicht gültig zu sein. Bitte gib sie im Format HH:MM an."
            )
            # Slot zurücksetzen -> wird in der nächsten Runde erneut abgefragt
            return [SlotSet("appointment_time", None)]

        # Wenn es keine Probleme gibt, dann sind auch keine Änderungen notwendig
        return []


class ActionCancelAppointment(Action):
    # Name der Action, die in der Domain verwendet wird
    def name(self) -> str:
        return "action_cancel_appointment"

    # Hauptfunktion, die beim Ausführen der Action aufgerufen wird
    def run(self, dispatcher, tracker, domain):
        # Termin-Slots aus dem Tracker werden abgefragt
        date = tracker.get_slot("appointment_date")
        time = tracker.get_slot("appointment_time")

        # Wenn entweder ein Datum oder eine Uhrzeit gesetzt ist, gilt -> Termin vorhanden
        if date or time:
            # Antwort-Nachricht -> verlinkt zu einem vordefinierten utterance im Domain-File
            dispatcher.utter_message(response="utter_cancel_appointment")

            # Termin wird „gelöscht“ -> somit werden alle relevanten Slots auf None gesetzt
            return [
                SlotSet("appointment_date", None),
                SlotSet("appointment_time", None),
                SlotSet("appointment_reason", None),
            ]
        else:
            # Wenn kein Termin gebucht ist -> Bekommt der Nutzer Info
            dispatcher.utter_message(
                text="ℹ️ Du hast aktuell keinen Termin gebucht, daher kann ich nichts stornieren."
            )

            return []


class ActionCancelCallback(Action):
    # Name der Action (wichtig für die Referenzierung in rules, stories sowie domain)
    def name(self) -> str:
        return "action_cancel_callback"

    # Die Action wird ausgeführt, wenn der Nutzer z.B. einen Rückruf abbrechen möchte
    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_cancel_callback")
        # Es erfolgt keine Ausgabe, sondern nur das Zurücksetzen der Callback-Slots
        return [
            SlotSet("callback_time", None),   # Uhrzeit für Rückruf löschen
            SlotSet("callback_phone", None),  # Telefonnummer löschen
        ]


class ActionHandleInterrupt(Action):
    # Name der Action (wichtig für Regeln und Story-Verweise)
    def name(self) -> Text:
        return "action_handle_interrupt"

    # Action wird ausgeführt, wenn der Nutzer das Formular unterbricht (z.B. durch eine andere Frage)
    def run(
        self,
        dispatcher: CollectingDispatcher,  # Zum Senden von Nachrichten
        tracker: Tracker,                  # Aktueller Gesprächsverlauf
        domain: Dict[Text, Any],           # Domain-Konfiguration
    ) -> List[EventType]:

        # Ermittelt den Intent der letzten Nutzer-Eingabe
        intent = tracker.latest_message["intent"].get("name")

        # Mögliche alternative Intents, die der Nutzer während eines Formulars äußern kann
        responses = {
            "greet": "utter_greet",
            "ask_pricing": "utter_ask_pricing",
            "ask_email": "utter_ask_email",
            "ask_phone": "utter_ask_phone",
            "contact": "utter_contact",
            "opening_hours": "utter_opening_hours",
            "services": "utter_services",
            "complaint": "utter_complaint",
            "feedback": "utter_feedback",
        }

        # Wenn der erkannte Intent in der Liste enthalten ist, dann passende Antwort senden
        if intent in responses:
            dispatcher.utter_message(response=responses[intent])
        else:
            # Wenn kein bekannter Intent, dann Standardantwort (Formular wird trotzdem abgebrochen)
            dispatcher.utter_message(
                text="✅ Okay, ich habe das Formular abgebrochen."
            )

        # Hier wird das laufende Formular deaktiviert
        return [ActiveLoop(None)]

