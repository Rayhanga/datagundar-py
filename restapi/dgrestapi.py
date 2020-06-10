from flask import Flask, request, jsonify, abort
from werkzeug.exceptions import HTTPException
from datagundar import Jadwal, SAP, Vclass

app = Flask('DataGundar REST API')

@app.before_request
def only_json():
    if not request.is_json:     
        return abort(400)


@app.errorhandler(HTTPException)
def handleException(e):
    return (
        jsonify({
            "error":{
                "error_code": e.code,
                "error_name": e.name,
                "error_description": e.description,
            }
        }), 
        e.code
    )

@app.route('/api/jadwal/jadkul/<kelas>')
def cipetJadkul(kelas):
    jd = Jadwal()
    jadkul = jd.getJadwalKelas(kelas)
    jd.close()
    if jadkul:
        return jsonify({'data': jadkul})
    
    return abort(404)

@app.route('/api/sap/<jurusan>')
def cipetSAPJurusan(jurusan):
    sap = SAP()
    sapJurusan = sap.getSAPJurusan(jurusan.replace('_', ' '))
    sap.close
    if sapJurusan:
        return jsonify({'data': sapJurusan})
    
    return abort(404)

@app.route('/api/vclass/upcoming_tasks')
def cipetUpcomingTasks():
    if request and ('uname' or 'pwd') in request.json:
        creds = request.json
        vc = Vclass()
        vc.login(creds["uname"], creds["pwd"])
        if vc.auth:
            upcomingTasks = vc.getUpcomingTasks()
            vc.close
            return jsonify({'data': upcomingTasks})
        else:
            vc.close()
            return abort(404)
        
    return abort(400)