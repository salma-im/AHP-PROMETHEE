from flask import Flask, jsonify,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/students_db'  # MySQL database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define your model
class Critere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    prix = db.Column(db.Integer)
    stockage = db.Column(db.Integer)
    camera = db.Column(db.Integer)
    design = db.Column(db.Integer)

    def __repr__(self):
        return f"<Critere {self.name}-{self.prix}-{self.stockage}-{self.camera}-{self.design}>"

# Create the tables within the application context
with app.app_context():
    db.create_all()

# Route to get all students
@app.route('/', methods=['GET', 'POST'])

def get_students():
    criteres = Critere.query.all()


    critere_list = []
    critere_list2 = []
    critere_list3 = []
    critere_list4=[]
    critere_list5 = []
    for critere in criteres:
        student_data = {
            'id': critere.id,
            'prix': critere.prix,
            'name': critere.name,
            'stockage': critere.stockage,
            'camera': critere.camera,
            'design': critere.design
        }

        critere_list.append(student_data)
    max_prix = max(critere_list, key=lambda x: x['prix'])
    max_prix_value = max_prix['prix']
    min_prix = min(critere_list, key=lambda x: x['prix'])
    min_prix_value = min_prix['prix']
    max_stockage = max(critere_list, key=lambda x: x['stockage'])
    max_stockage_value = max_stockage['stockage']
    min_stockage = min(critere_list, key=lambda x: x['stockage'])['stockage']
    min_stockage_value = min_stockage
    max_camera = max(critere_list, key=lambda x: x['camera'])
    min_camera = min(critere_list, key=lambda x: x['camera'])
    print(min_camera)
    max_design = max(critere_list, key=lambda x: x['design'])
    min_design = min(critere_list, key=lambda x: x['design'])
    MaxMinPrix=max_prix_value-min_prix_value
    MaxMinStockage = max_stockage_value - min_stockage_value
    MaxMinCamera = max_camera['camera'] - min_camera['camera']
    MaxMinDesign=max_design['design']-min_design['design']
    for critere in critere_list:
        student_data = {
            'prix': (critere['prix'] - min_prix_value) / MaxMinPrix,
            'stockage':(critere['stockage']-min_stockage_value)/MaxMinStockage,
            'camera': (critere['camera'] - min_camera['camera']) / MaxMinCamera,
            'design': (critere['design'] - min_design['design']) / MaxMinDesign,
            'name':critere['name']
        }
        critere_list2.append(student_data)
    i=0;
    print(critere_list3)
    pi=[]
    z=len(critere_list)
    for critere in critere_list2:

        for critere1 in critere_list2:
            prix=(critere['prix']-critere1['prix'])*0.35
            if prix<0:
                prix=0
            stockage = (critere['stockage'] - critere1['stockage']) * 0.25
            if stockage < 0:
                stockage = 0
            design = (critere['design'] - critere1['design']) * 0.15
            if design < 0:
                design = 0
            camera = (critere['camera'] - critere1['camera'])*0.25
            if camera < 0:
                camera = 0
            student_data = {
                'name': critere['name'] + ' ' + critere1['name'],
                'pi': prix+stockage+design+camera
            }
            critere_list3.append(student_data)
            pi.append((prix+stockage+design+camera))
            i=i+1
    x=0
    flux_entrant=0
    flux_sortant=0

    for critere in critere_list2:
        op=0
        for a in range(z):
            flux_sortant+=pi[x+a]
            flux_entrant+=pi[op]
            op+=z
        cri={
            'name':critere['name'],
            'flux_entrant' : flux_entrant/(z-1),
            'flux_sortant' : flux_sortant/(z-1),
            'flux_net':(flux_entrant/(z-1))-(flux_sortant/(z-1))
            }

        critere_list4.append(cri)
        x=x+z
    ranked=sorted(critere_list4, key=lambda x: x['flux_net'],reverse=True)
    it=0
    for critere in ranked:
        it=it+1
        lis ={
            'name':critere['name'],
            'rank':it
        }
        critere_list5.append(lis)



    return render_template('index.html', criteres=criteres, critere_list2=critere_list2, critere_list3=critere_list3, critere_list4=critere_list4, critere_list5=critere_list5)


if __name__ == '__main__':
    app.run(debug=True)