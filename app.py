from flask import Flask
from flask_restful import Resource, Api, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from ValidarCPF import ValidarCpf

# Fields
from fields.Fields import *
# Fields

# Args
from arguments.Arguments import *
# Args

app = Flask(__name__)

# Banco de Dados ( MySQL )
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@127.0.0.1/kogui' # USER | PASS | SERVER | DATABASE #
db = SQLAlchemy(app)

migrate = Migrate(app, db) # Instancia Migrate 
# Banco de Dados ( MySQL )

#API
api = Api(app) # Instância API

# Models API

# Model Doctor
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    crm = db.Column(db.String(10), nullable=False)
    crmUf = db.Column(db.String(2), nullable=False)
    medicalAppointments = db.relationship('MedicalAppointment', backref="doctor")
    
    def __str__(self):
        return "MÉDICO - Nome: {} CRM: {}-{}".format(self.name, self.crm, self.crmUf)
    
    def __repr__(self):
        return "MÉDICO - Nome: {} CRM: {}-{}".format(self.name, self.crm, self.crmUf)

# Model Patient
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    birthdate = db.Column(db.DateTime, nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    medicalAppointments = db.relationship('MedicalAppointment', backref="patient")
    
    def __str__(self):
         return "Paciente - Nome: {} CPF: {}".format(self.name, self.cpf)
     
    def __repr__(self):
         return "Paciente - Nome: {} CPF: {}".format(self.name, self.cpf)
     
# Model Medical Appointment
class MedicalAppointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(127), nullable=True)
    schedule = db.Column(db.DateTime, nullable=True)
    idDoctor = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    idPatient = db.Column(db.Integer, db.ForeignKey('patient.id'))
    
# Models API

#EndPoints

# Doctor - EndPoints
class DoctorAPI(Resource):
    @marshal_with(doctor_fields)
    def get(self):
        doctors = Doctor.query.all()
        if doctors.count == 0:
            return abort(400, message="Não existem registros cadastrados no momento")
        return doctors
    
    @marshal_with(doctor_fields)
    def post(self):
        args = doctor_args.parse_args()
        
        doctortmp = Doctor.query.filter_by(crm=args['crm'], crmUf=args['crmUf']).first()
        if doctortmp:
            abort(400, message="Já existe médico com CRM: {}-{} cadastrado".format(args['crm']. args['crmUf']))
            
        doctor = Doctor(name=args['name'], crm=args['crm'], crmUf=args['crmUf'])
        db.session.add(doctor)
        db.session.commit()
        return doctor, 201

class DoctorIdAPI(Resource):
    @marshal_with(doctor_fields)
    def get(self, id):
        doctor = Doctor.query.filter_by(id=id).first()
        if not doctor:
            abort(400, message="Não foi possível encontrar Médico pelo ID em questão")
        return doctor
    
    @marshal_with(doctor_fields)
    def put(self, id):
        args = doctor_args.parse_args()
        doctor = Doctor.query.filter_by(id=id).first()
        if not doctor:
            abort(400, message="Não foi possível encontrar um Médico pelo ID em questão")
        
        if args['name']:
            doctor.name = args['name']
        if args['crm']:
            doctor.crm = args['crm']
        if args['crmUf']:
            doctor.crmUf = args['crmUf']
            
        db.session.commit()
        return doctor
    
    @marshal_with(doctor_fields)
    def delete(self, id):
        doctor = Doctor.query.filter_by(id=id).first()
        if not doctor:
            abort(400, message="Não foi possível encontrar um Médico pelo ID em questão")
        
        medicAppointList = MedicalAppointment.query.filter_by(idDoctor=id)
        if medicAppointList.count!=0:
            abort(400, message="Não é possível Excluir Registro. Motivo: Médico possui agendamentos")
        
        db.session.delete(doctor)
        db.session.commit()
        return "Registro Excluído com Sucesso", 204
# Doctor - EndPoints

# Patient - EndPoints
class PatientAPI(Resource):
    @marshal_with(patient_fields)
    def get(self):
        patients = Patient.query.all()
        if patients.count == 0:
            return abort(400, message="Não existem registros cadastrados no momento")
        return patients
    
    @marshal_with(patient_fields)
    def post(self):
        args = patient_args.parse_args()
        
        cpf = args['cpf']
        if not ValidarCpf.isValid(cpf):
            abort(400, message="CPF Inválido")
        
        doctor = Doctor.query.filter_by(id=args['idDoctor']).first()
        if not doctor:
            return abort(400, message="Médico Não Existe")
        
        patienttmp = Patient.query.filter_by(cpf=args['cpf']).first()
        if patienttmp:
            return abort(400, message="Paciente com o CPF: {} já existe".format(args['cpf']))
        
        patient = Patient(name=args['name'], birthdate=args['birthdate'], cpf=cpf)
        db.session.add(patient)
        db.session.flush()
        db.session.commit()
        
        medicappoint = MedicalAppointment(idDoctor=doctor.id, idPatient=patient.id)
        db.session.add(medicappoint)
        db.session.commit()
        
        return patient, 201
    
class PatientIdAPI(Resource):
    @marshal_with(patient_fields)
    def get(self, id):
        patient = Patient.query.filter_by(id=id).first()
        if not patient:
            abort(400, message="Não foi possível encontrar um Paciente pelo ID em questão")
        return patient
    
    @marshal_with(patient_fields)
    def put(self, id):
        args = patient_args.parse_args()
        
        cpf = args['cpf']
        if not ValidarCpf.isValid(cpf):
            abort(400, message="CPF Inválido")
        
        patient = Patient.query.filter_by(id=id).first()
        if not patient:
            abort(404, message="Não foi possível encontrar um Médico pelo ID em questão")
        
        if args['name']:
            patient.name = args['name']
        if args['birthdate']:
            patient.birthdate = args['birthdate']
        if args['cpf']:
            patient.cpf = cpf
            
        db.session.commit()
        return patient
    
    @marshal_with(patient_fields)
    def delete(self, id):
        patient = Patient.query.filter_by(id=id).first()
        if not patient:
            abort(400, message="Não foi possível encontrar um Médico pelo ID em questão")
        
        db.session.delete(patient)
        db.session.commit()
        return "Registro Excluído com Sucesso", 204
    
class PatientFilterAPI(Resource):
    def get(self):    
        args = patient_filter_args.parse_args()
        doctor = Doctor.query.filter_by(id=args['idDoctor']).first()
        if not doctor:
            abort(400, message="Médico não encontrado")
        
        listPatients = []
        for medcappoint in doctor.medicalAppointments:
            patient = Patient.query.filter_by(id=medcappoint.idPatient).first()
            listPatients.append({"id":patient.id,"name":patient.name, "birthdate":patient.birthdate.strftime("%Y-%m-%dT%H:%M:%S"), "cpf":patient.cpf})
            
        return listPatients, 201
    
# Patient - EndPoints

# Medical Appointment - EndPoints
class MedicalAppointmentAPI(Resource):
    @marshal_with(medicappoint_fields)
    def get(self):
        list = MedicalAppointment.query.all()
        if list.count == 0:
            return abort(400, message="Não existem registros cadastrados no momento")
        return list
    
    @marshal_with(medicappoint_fields)
    def post(self):
        args = medicappoint_args.parse_args()
        medicappoint = MedicalAppointment(description=args['description'], schedule =args['schedule'], idDoctor=args['idDoctor'], idPatient=args['idPatient'])
        db.session.add(medicappoint)
        db.session.commit()
        return medicappoint, 201
# Medical Appointment - EndPoints

#EndPoints

# PATHs

#Doctor
api.add_resource(DoctorAPI, "/api/doctor")
api.add_resource(DoctorIdAPI, "/api/doctor/<int:id>")

# Patient
api.add_resource(PatientAPI, "/api/patient")
api.add_resource(PatientIdAPI, "/api/patient/<int:id>")

api.add_resource(PatientFilterAPI, "/api/patient/filter")
# PATHs

#API

if __name__ == '__main__':
      app.run(host='127.0.0.1', port=6663)