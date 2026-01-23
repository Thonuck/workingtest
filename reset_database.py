#!/usr/bin/env python3
"""
Database Reset Script

Dieses Script löscht die bestehende Datenbank komplett und erstellt sie neu mit dem aktuellen Schema.
ACHTUNG: Alle Daten gehen verloren!

Verwendung:
    python reset_database.py
"""

import os
import shutil
from app import create_app, db
from app.models import User

def reset_database():
    """Löscht und erstellt die Datenbank neu."""
    
    # Pfad zum instance-Verzeichnis (enthält die Datenbank)
    instance_path = 'instance'
    
    # Lösche das GESAMTE instance-Verzeichnis wenn es existiert
    if os.path.exists(instance_path):
        print(f"🗑️  Lösche komplettes instance-Verzeichnis: {instance_path}")
        shutil.rmtree(instance_path)
        print("✅ Instance-Verzeichnis gelöscht.")
    else:
        print("ℹ️  Kein instance-Verzeichnis gefunden.")
    
    # Erstelle instance-Verzeichnis neu
    print("📁 Erstelle instance-Verzeichnis...")
    os.makedirs(instance_path, exist_ok=True)
    
    # Jetzt create_app aufrufen - es wird eine komplett neue Datenbank erstellt
    print("🔧 Initialisiere Flask-App...")
    app = create_app()
    
    with app.app_context():
        # create_app() erstellt bereits die Datenbank und den Admin-User!
        # Wir müssen nichts weiter tun.
        print("✅ Datenbank erfolgreich zurückgesetzt!")
        print("\n📋 Standard-Login:")
        print("   Username: admin")
        print("   Password: admin")
        print("\n⚠️  WICHTIG: Ändern Sie das Admin-Passwort in der Produktion!")

if __name__ == '__main__':
    import sys
    
    print("=" * 60)
    print("Database Reset Script")
    print("=" * 60)
    print("\n⚠️  WARNUNG: Dieser Vorgang löscht ALLE Daten!")
    
    response = input("\nMöchten Sie fortfahren? (ja/nein): ")
    
    if response.lower() in ['ja', 'j', 'yes', 'y']:
        reset_database()
    else:
        print("❌ Abgebrochen.")
        sys.exit(0)
