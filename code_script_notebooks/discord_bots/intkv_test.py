import dbm
import json

# need to additional work if dict and lists are stored
# so getting the json. Also the keys and values are in 
# byte format, so cast it to str

with dbm.open("kvstore", "c") as db:
    db['key'] = "value"
    db['25'] = "twentyfive"  # key must be str / bytes
    db['dict'] = json.dumps({"nature": "Gives"})
    db['list'] = ",".join(["nature", "Gives"])
    # db is accessible only in the context
    print(db.keys())
    print(db['25'])
    print(db['key'])
    print(db['list'])
    db['25'] = 'twenty six'  # update works
    print(db['25'])
    del db['25']  # does delete work
    print('25' in db)
    for el in str(db['list']).split(','):
        print(el, end=' ')
    print(json.loads(db['dict']))
