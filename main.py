import sys

def test():
    from sqlalchemy import select
    print("Hello from mobsys-backend-api!")

    import backend.classes.aiven as aiven
    import backend.classes.tables as tables
    aiven_env = aiven.AivenEnvironment()
    db = aiven.AivenDatabase(aiven_env)
    db.connect()

    products = select(tables.Produkt).where(tables.Produkt.id == 1)
    with db.session as session:
        result = session.execute(products).scalar_one_or_none()
        if result:
            print(f"Product ID: {result.id}, Name: {result.Bezeichnung}, Price: {result.Preis}")
        else:
            print("No product found with ID 1.")

def main():
    from backend.app import app
    app.run(debug=True, host='0.0.0.0', port=5000)



if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        main()
