from flask import Blueprint, jsonify, request
import backend.classes.tables as tables
from sqlalchemy import select

products_bp = Blueprint('products', __name__, url_prefix='/api/products')


def init_routes(db):
    """Initialize routes with database instance"""
    
    @products_bp.route('', methods=['GET'])
    def get_products():
        """Get all products"""
        try:
            with db.session as session:
                products = session.execute(select(tables.Produkt)).scalars().all()
                result = []
                for product in products:
                    result.append({
                        "id": product.id,
                        "name": product.Bezeichnung,
                        "price": float(product.Preis) if product.Preis else None
                    })
                return jsonify({"products": result, "count": len(result)}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @products_bp.route('/<int:product_id>', methods=['GET'])
    def get_product(product_id):
        """Get a single product by ID"""
        try:
            with db.session as session:
                product = session.execute(
                    select(tables.Produkt).where(tables.Produkt.id == product_id)
                ).scalar_one_or_none()
                
                if product:
                    return jsonify({
                        "id": product.id,
                        "name": product.Bezeichnung,
                        "price": float(product.Preis) if product.Preis else None
                    }), 200
                else:
                    return jsonify({"error": "Product not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return products_bp
