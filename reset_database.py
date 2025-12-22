#!/usr/bin/env python3
"""
Database Reset Script

Dieses Script löscht die bestehende Datenbank und erstellt sie neu mit dem aktuellen Schema.
ACHTUNG: Alle Daten gehen verloren!

Verwendung:
    python reset_database.py
"""

import os
from app import create_app, db
from app.models import User

def reset_database():
    """Löscht und erstellt die Datenbank neu."""
    
    app = create_app()
    
    with app.app_context():
        # Pfad zur Datenbank-Datei
        db_path = 'instance/database.db'
        
        # Lösche alte Datenbank wenn sie existiert
        if os.path.exists(db_path):
            print(f"🗑️  Lösche alte Datenbank: {db_path}")
            os.remove(db_path)
        else:
            print("ℹ️  Keine alte Datenbank gefunden.")
        
        # Erstelle neue Datenbank mit aktuellem Schema
        print("🔨 Erstelle neue Datenbank mit aktuellem Schema...")
        db.create_all()
        
        # Erstelle Admin-User
        print("👤 Erstelle Admin-User...")
        admin_user = User(username="admin", role="admin")
        admin_user.set_password("admin")
        db.session.add(admin_user)
        db.session.commit()
        
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
