from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Define database models
class CelestialBody(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)

class Spacecraft(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    launch_date = db.Column(db.String(20), nullable=False)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission_details.id'), nullable=False)

class Astronaut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)

class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    results = db.Column(db.String(100), nullable=False)
    spacecraft_id = db.Column(db.Integer, db.ForeignKey('spacecraft.id'), nullable=False)

class AlienEncounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)

class MissionDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)

# Create tables
with app.app_context():
    db.create_all()
    # Sample data
    sample_data = {
        'CelestialBody': [
            {'name': 'Earth', 'type': 'Planet'},
            {'name': 'Moon', 'type': 'Moon'},
            {'name': 'Mars', 'type': 'Planet'}
        ],
        'Spacecraft': [
            {'name': 'Apollo 11', 'launch_date': '1969-07-16', 'mission_id': 1},
            {'name': 'Curiosity', 'launch_date': '2011-11-26', 'mission_id': 3},
            {'name': 'Voyager 1', 'launch_date': '1977-09-05', 'mission_id': 2}
        ],
        'Astronaut': [
            {'name': 'Neil Armstrong', 'specialization': 'Commander'},
            {'name': 'Curiosity Rover', 'specialization': 'Rover'},
            {'name': 'Carl Sagan', 'specialization': 'Astrophysicist'}
        ],
        'Experiment': [
            {'name': 'Microgravity Study', 'results': 'Zero-G achieved', 'spacecraft_id': 1},
            {'name': 'Mars Soil Analysis', 'results': 'Water presence detected', 'spacecraft_id': 3},
            {'name': 'Voyager Imaging', 'results': 'Captured images of outer planets', 'spacecraft_id': 2}
        ],
        'AlienEncounter': [
            {'description': 'Unknown flying object', 'location': 'Space', 'date': '2023-01-15'},
            {'description': 'Strange signal', 'location': 'Proxima Centauri', 'date': '2024-05-20'},
            {'description': 'Unexplained phenomenon', 'location': 'Orion Nebula', 'date': '2022-11-08'}
        ],
        'MissionDetails': [
            {'name': 'Apollo 11 Moon Landing', 'destination': 'Moon'},
            {'name': 'Voyager Interstellar Mission', 'destination': 'Outer Space'},
            {'name': 'Curiosity Mars Exploration', 'destination': 'Mars'}
        ]
    }
    # Insert sample data into tables
    for table_name, data in sample_data.items():
        model_class = globals()[table_name]
        if not db.session.query(model_class).count():
            for entry in data:
                db.session.add(model_class(**entry))
            db.session.commit()




# Routes
@app.route('/')
def index():
    return render_template('index.html', celestial_bodies=CelestialBody.query.all(),
                           spacecraft=Spacecraft.query.all(),
                           astronauts=Astronaut.query.all(),
                           experiments=Experiment.query.all(),
                           alien_encounters=AlienEncounter.query.all(),
                           mission_details=MissionDetails.query.all())

@app.route('/celestial_bodies')
def celestial_bodies():
    return render_template('celestial_bodies.html', celestial_bodies=CelestialBody.query.all())


@app.route('/add_celestial_body', methods=['POST'])
def add_celestial_body():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        new_celestial_body = CelestialBody(name=name, type=type)
        db.session.add(new_celestial_body)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_celestial_body/<int:id>', methods=['POST'])
def delete_celestial_body(id):
    celestial_body = CelestialBody.query.get_or_404(id)
    db.session.delete(celestial_body)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/modify_celestial_body/<int:id>', methods=['POST'])
def modify_celestial_body(id):
    celestial_body = CelestialBody.query.get_or_404(id)
    if request.method == 'POST':
        celestial_body.name = request.form['name']
        celestial_body.type = request.form['type']
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/spacecraft')
def spacecraft():
    return render_template('spacecraft.html', spacecraft=Spacecraft.query.all())


@app.route('/add_spacecraft', methods=['POST'])
def add_spacecraft():
    if request.method == 'POST':
        name = request.form['name']
        launch_date = request.form['launch_date']
        mission_id = request.form['mission_id']

        new_spacecraft = Spacecraft(name=name, launch_date=launch_date, mission_id=mission_id)
        db.session.add(new_spacecraft)
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('spacecraft'))

@app.route('/delete_spacecraft/<int:id>', methods=['POST'])
def delete_spacecraft(id):
    spacecraft = Spacecraft.query.get_or_404(id)
    db.session.delete(spacecraft)
    db.session.commit()
    return redirect(url_for('spacecraft'))

@app.route('/modify_spacecraft/<int:id>', methods=['POST'])
def modify_spacecraft(id):
    spacecraft = Spacecraft.query.get_or_404(id)
    if request.method == 'POST':
        spacecraft.name = request.form['name']
        spacecraft.launch_date = request.form['launch_date']
        spacecraft.mission_id = request.form['mission_id']
        db.session.commit()
    return redirect(url_for('spacecraft'))

@app.route('/astronauts')
def astronauts():
    return render_template('astronauts.html', astronauts=Astronaut.query.all())


@app.route('/add_astronaut', methods=['POST'])
def add_astronaut():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']

        new_astronaut = Astronaut(name=name, specialization=specialization)
        db.session.add(new_astronaut)
        db.session.commit()
        
    return redirect(url_for('astronauts'))

@app.route('/delete_astronaut/<int:id>', methods=['POST'])
def delete_astronaut(id):
    astronaut = Astronaut.query.get_or_404(id)
    db.session.delete(astronaut)
    db.session.commit()
    return redirect(url_for('astronauts'))

@app.route('/modify_astronaut/<int:id>', methods=['POST'])
def modify_astronaut(id):
    astronaut = Astronaut.query.get_or_404(id)
    if request.method == 'POST':
        astronaut.name = request.form['name']
        astronaut.age = request.form['age']
        astronaut.mission_id = request.form['mission_id']
        db.session.commit()
    return redirect(url_for('astronauts'))

@app.route('/experiments')
def experiments():
    return render_template('experiments.html', experiments=Experiment.query.all())

@app.route('/add_experiment', methods=['POST'])
def add_experiment():
    if request.method == 'POST':
        name = request.form['name']
        results = request.form['results']
        spacecraft_id = request.form['spacecraft_id']

        new_experiment = Experiment(name=name, results=results, spacecraft_id=spacecraft_id)
        db.session.add(new_experiment)
        db.session.commit()
        
    return redirect(url_for('experiments'))

@app.route('/delete_experiment/<int:id>', methods=['POST'])
def delete_experiment(id):
    experiment = Experiment.query.get_or_404(id)
    db.session.delete(experiment)
    db.session.commit()
    return redirect(url_for('experiments'))

@app.route('/modify_experiment/<int:id>', methods=['POST'])
def modify_experiment(id):
    experiment = Experiment.query.get_or_404(id)
    if request.method == 'POST':
        experiment.name = request.form['name']
        experiment.results = request.form['results']
        experiment.spacecraft_id = request.form['spacecraft_id']
        db.session.commit()
    return redirect(url_for('experiments'))

@app.route('/alien_encounters')
def alien_encounters():
    return render_template('alien_encounters.html', alien_encounters=AlienEncounter.query.all())

@app.route('/add_alien_encounter', methods=['POST'])
def add_alien_encounter():
    if request.method == 'POST':
        description = request.form['description']
        location = request.form['location']
        date = request.form['date']

        new_encounter = AlienEncounter(description=description, location=location, date=date)
        db.session.add(new_encounter)
        db.session.commit()
        
    return redirect(url_for('alien_encounters'))

@app.route('/delete_alien_encounter/<int:id>', methods=['POST'])
def delete_alien_encounter(id):
    encounter = AlienEncounter.query.get_or_404(id)
    db.session.delete(encounter)
    db.session.commit()
    return redirect(url_for('alien_encounters'))

@app.route('/modify_alien_encounter/<int:id>', methods=['POST'])
def modify_alien_encounter(id):
    encounter = AlienEncounter.query.get_or_404(id)
    if request.method == 'POST':
        encounter.description = request.form['description']
        encounter.location = request.form['location']
        encounter.date = request.form['date']
        db.session.commit()
    return redirect(url_for('alien_encounters'))

@app.route('/mission_details')
def mission_details():
    return render_template('mission_details.html', mission_details=MissionDetails.query.all())

@app.route('/add_mission_detail', methods=['POST'])
def add_mission_detail():
    if request.method == 'POST':
        name = request.form['name']
        destination = request.form['destination']
        new_mission_detail = MissionDetails(name=name, destination=destination)
        db.session.add(new_mission_detail)
        db.session.commit()
    return redirect(url_for('mission_details'))

@app.route('/delete_mission_detail/<int:id>', methods=['POST'])
def delete_mission_detail(id):
    mission_detail = MissionDetails.query.get_or_404(id)
    db.session.delete(mission_detail)
    db.session.commit()
    return redirect(url_for('mission_details'))

@app.route('/modify_mission_detail/<int:id>', methods=['POST'])
def modify_mission_detail(id):
    mission_detail = MissionDetails.query.get_or_404(id)
    if request.method == 'POST':
        mission_detail.name = request.form['name']
        mission_detail.destination = request.form['destination']
        db.session.commit()
    return redirect(url_for('mission_details'))
if __name__ == '__main__':
    app.run(debug=True)
