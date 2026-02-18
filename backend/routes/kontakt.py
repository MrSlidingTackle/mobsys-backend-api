from flask import Blueprint, jsonify, request
import backend.classes.tables as tables
from sqlalchemy import select

kontakt_bp = Blueprint('kontakt', __name__, url_prefix='/api/kontakt')


def init_routes(db):
    """Initialize routes with database instance"""
    
    @kontakt_bp.route('', methods=['GET'])
    def get_contacts():
        """Get all contacts with resolved Person or Unternehmen data"""
        try:
            with db.session as session:
                contacts = session.execute(select(tables.Kontakt)).scalars().all()
                result = []
                for contact in contacts:
                    contact_data = {
                        "id": contact.id,
                        "email": contact.EMail,
                        "telefonnummer": contact.Telefonnummer,
                        "rolle": contact.Rolle,
                        "referenz": contact.Referenz,
                        "ref_typ": contact.RefTyp
                    }
                    
                    # Resolve Referenz foreign key (Person or Unternehmen)
                    if contact.RefTyp == "Person":
                        person = session.execute(
                            select(tables.Person).where(tables.Person.id == contact.Referenz)
                        ).scalar_one_or_none()
                        
                        if person:
                            # Also resolve Adresse for Person
                            adresse = session.execute(
                                select(tables.Adresse).where(tables.Adresse.id == person.Adresse)
                            ).scalar_one_or_none()
                            
                            contact_data["referenz_data"] = {
                                "id": person.id,
                                "name": person.Name,
                                "adresse_id": person.Adresse,
                                "geburtsdatum": person.Geburtsdatum.isoformat() if person.Geburtsdatum else None,
                                "titel": person.Titel
                            }
                            
                            if adresse:
                                contact_data["referenz_data"]["adresse"] = {
                                    "id": adresse.id,
                                    "plz": adresse.Plz,
                                    "ortsname": adresse.ortsname,
                                    "strasse": adresse.Strasse,
                                    "hausnr": adresse.Hausnr
                                }
                    
                    elif contact.RefTyp == "Unternehmen":
                        unternehmen = session.execute(
                            select(tables.Unternehmen).where(tables.Unternehmen.id == contact.Referenz)
                        ).scalar_one_or_none()
                        
                        if unternehmen:
                            # Also resolve Adresse for Unternehmen
                            adresse = session.execute(
                                select(tables.Adresse).where(tables.Adresse.id == unternehmen.Adresse)
                            ).scalar_one_or_none()
                            
                            contact_data["referenz_data"] = {
                                "id": unternehmen.id,
                                "name": unternehmen.Name,
                                "adresse_id": unternehmen.Adresse,
                                "umsatz": unternehmen.Umsatz
                            }
                            
                            if adresse:
                                contact_data["referenz_data"]["adresse"] = {
                                    "id": adresse.id,
                                    "plz": adresse.Plz,
                                    "ortsname": adresse.ortsname,
                                    "strasse": adresse.Strasse,
                                    "hausnr": adresse.Hausnr
                                }
                    
                    result.append(contact_data)
                return jsonify({"contacts": result, "count": len(result)}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @kontakt_bp.route('/<int:contact_id>', methods=['GET'])
    def get_contact(contact_id):
        """Get a single contact by ID with resolved Person or Unternehmen data"""
        try:
            with db.session as session:
                contact = session.execute(
                    select(tables.Kontakt).where(tables.Kontakt.id == contact_id)
                ).scalar_one_or_none()
                
                if contact:
                    contact_data = {
                        "id": contact.id,
                        "email": contact.EMail,
                        "telefonnummer": contact.Telefonnummer,
                        "rolle": contact.Rolle,
                        "referenz": contact.Referenz,
                        "ref_typ": contact.RefTyp
                    }
                    
                    # Resolve Referenz foreign key (Person or Unternehmen)
                    if contact.RefTyp == "Person":
                        person = session.execute(
                            select(tables.Person).where(tables.Person.id == contact.Referenz)
                        ).scalar_one_or_none()
                        
                        if person:
                            # Also resolve Adresse for Person
                            adresse = session.execute(
                                select(tables.Adresse).where(tables.Adresse.id == person.Adresse)
                            ).scalar_one_or_none()
                            
                            contact_data["referenz_data"] = {
                                "id": person.id,
                                "name": person.Name,
                                "adresse_id": person.Adresse,
                                "geburtsdatum": person.Geburtsdatum.isoformat() if person.Geburtsdatum else None,
                                "titel": person.Titel
                            }
                            
                            if adresse:
                                contact_data["referenz_data"]["adresse"] = {
                                    "id": adresse.id,
                                    "plz": adresse.Plz,
                                    "ortsname": adresse.ortsname,
                                    "strasse": adresse.Strasse,
                                    "hausnr": adresse.Hausnr
                                }
                    
                    elif contact.RefTyp == "Unternehmen":
                        unternehmen = session.execute(
                            select(tables.Unternehmen).where(tables.Unternehmen.id == contact.Referenz)
                        ).scalar_one_or_none()
                        
                        if unternehmen:
                            # Also resolve Adresse for Unternehmen
                            adresse = session.execute(
                                select(tables.Adresse).where(tables.Adresse.id == unternehmen.Adresse)
                            ).scalar_one_or_none()
                            
                            contact_data["referenz_data"] = {
                                "id": unternehmen.id,
                                "name": unternehmen.Name,
                                "adresse_id": unternehmen.Adresse,
                                "umsatz": unternehmen.Umsatz
                            }
                            
                            if adresse:
                                contact_data["referenz_data"]["adresse"] = {
                                    "id": adresse.id,
                                    "plz": adresse.Plz,
                                    "ortsname": adresse.ortsname,
                                    "strasse": adresse.Strasse,
                                    "hausnr": adresse.Hausnr
                                }
                    
                    return jsonify(contact_data), 200
                else:
                    return jsonify({"error": "Contact not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @kontakt_bp.route('', methods=['POST'])
    def create_contact():
        """Create a new contact"""
        try:
            data = request.get_json()
            
            # Validate required fields
            if not all(key in data for key in ['email', 'telefonnummer', 'rolle', 'referenz', 'ref_typ']):
                return jsonify({"error": "Missing required fields"}), 400
            
            with db.session as session:
                new_contact = tables.Kontakt(
                    EMail=data['email'],
                    Telefonnummer=data['telefonnummer'],
                    Rolle=data['rolle'],
                    Referenz=data['referenz'],
                    RefTyp=data['ref_typ']
                )
                print(type(data['email']))
                print(type(data['telefonnummer']))
                print(type(data['rolle']))
                print(type(data['referenz']))
                print(type(data['ref_typ']))
                session.add(new_contact)
                session.commit()
                session.refresh(new_contact)
                
                return jsonify({
                    "id": new_contact.id,
                    "email": new_contact.EMail,
                    "telefonnummer": new_contact.Telefonnummer,
                    "rolle": new_contact.Rolle,
                    "referenz": new_contact.Referenz,
                    "ref_typ": new_contact.RefTyp
                }), 201
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500


    @kontakt_bp.route('/<int:contact_id>', methods=['PUT'])
    def update_contact(contact_id):
        """Update an existing contact"""
        try:
            data = request.get_json()
            
            with db.session as session:
                contact = session.execute(
                    select(tables.Kontakt).where(tables.Kontakt.id == contact_id)
                ).scalar_one_or_none()
                
                if not contact:
                    return jsonify({"error": "Contact not found"}), 404
                
                # Update fields if provided
                if 'email' in data:
                    contact.EMail = data['email']
                if 'telefonnummer' in data:
                    contact.Telefonnummer = data['telefonnummer']
                if 'rolle' in data:
                    contact.Rolle = data['rolle']
                if 'referenz' in data:
                    contact.Referenz = data['referenz']
                if 'ref_typ' in data:
                    contact.RefTyp = data['ref_typ']
                
                session.commit()
                session.refresh(contact)
                
                return jsonify({
                    "id": contact.id,
                    "email": contact.EMail,
                    "telefonnummer": contact.Telefonnummer,
                    "rolle": contact.Rolle,
                    "referenz": contact.Referenz,
                    "ref_typ": contact.RefTyp
                }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @kontakt_bp.route('/<int:contact_id>', methods=['DELETE'])
    def delete_contact(contact_id):
        """Delete a contact"""
        try:
            with db.session as session:
                contact = session.execute(
                    select(tables.Kontakt).where(tables.Kontakt.id == contact_id)
                ).scalar_one_or_none()
                
                if not contact:
                    return jsonify({"error": "Contact not found"}), 404
                
                session.delete(contact)
                session.commit()
                
                return jsonify({"message": "Contact deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return kontakt_bp
