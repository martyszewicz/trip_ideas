from flask import Flask, render_template, request, flash
import csv
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "Something"

class NewTrip:
    def __init__(self, trip_name, email, description, completness, contact_ok, file):
        self.trip_name = trip_name
        self.email = email
        self.description = description
        self.file = file
        self.completness = completness
        self.contact_ok = contact_ok
        self.trip = [self.trip_name, self.email, self.description, self.completness, self.contact_ok]

    def save_trip(self):
        with open(self.file, "r", encoding="utf-8-sig") as csvfile:
            csvreader = (csv.reader(csvfile, delimiter=","))
            for row in csvreader:
                if self.trip_name in row:
                    return False
            with open(self.file, "a+", encoding="utf-8", newline="") as csvfile:
                csvwriter = (csv.writer(csvfile))
                csvwriter.writerow(self.trip)

class Trips:
    def __init__(self, file):
        self.file = file
        self.list_of_trips = []
    def load_trips(self):
        with open (self.file, "r", encoding="utf-8-sig") as csvfile:
            csvreader = (csv.reader(csvfile, delimiter=","))
            for row in csvreader:
                self.list_of_trips.append(NewTrip(row[0], row[1], row[2], row[3], row[4], file))
        return self.list_of_trips

file = os.path.join(app.static_folder, "trips.csv")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/", methods=["GET"])
def index():
    trips = Trips(file)
    trips.load_trips()
    return render_template("index.html", list_of_trips=trips.list_of_trips)

@app.route("/checking_trip", methods=["POST"])
def checking_trip():
    trips = Trips(file)
    trips.load_trips()
    checking_trip = request.form["checking_trip"] if "checking_trip" in request.form else ""
    for trip in trips.list_of_trips:
        if trip.trip_name == checking_trip:
            newtrip = trip
            return render_template("checking_trip.html", newtrip=newtrip)

@app.route("/new_trip", methods=["GET", "POST"])
def new_trip():
    global completness, contact_ok
    if request.method == 'GET':
        return render_template("new_trip.html")
    else:
        trip_name = request.form["trip_name"] if "trip_name" in request.form else ""
        email = request.form["email"] if "email" in request.form else ""
        description = request.form["description"] if "description" in request.form else ""
        if "submit_button" in request.form:
            completness = request.form["completness"] if "completness" in request.form else "0"
            contact_ok = request.form["contact_ok"] if "contact_ok" in request.form else "0"

        # compl_value = request.form["completness"]
        # completness = True if compl_value == "yes" else False
        # contact_value = request.form["contact_ok"] if "contact_ok" in request.form else "no"
        # contact_ok = True if contact_value == "yes" else False

        newtrip = NewTrip(trip_name=trip_name, email=email, description=description, completness=completness,
                          contact_ok=contact_ok, file=file)

        if newtrip.save_trip() == False:
            flash("Wycieczka o podanej nazwie już istnieje w katalogu, podaj inną nazwę")
            return render_template ('trip_correct.html', newtrip=newtrip)
        else:
            newtrip.save_trip()
            flash(f"Wycieczka została zapisana pomyślnie")

        return render_template("checking_trip.html", newtrip=newtrip)

if __name__ == "__main__":
    app.run()

