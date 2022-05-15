import core
import db
import sys
if sys.argv[1] == "init":
    #db.initialize_new_database()
    db.initialize_empty_database(db)
    db.populate_sample_data(db)
core.app.debug = True
core.app.run(host="0.0.0.0")