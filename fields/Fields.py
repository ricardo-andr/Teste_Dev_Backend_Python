from flask_restful import fields

doctor_fields = {
    'id': fields.String,
    'name': fields.String,
    'crm': fields.String,
    'crmUf': fields.String
}

patient_fields = {
    'id': fields.String,
    'name': fields.String,
    'birthdate': fields.DateTime,
    'cpf': fields.String,
    'idDoctor': fields.Integer
}

medicappoint_fields = {
    'id': fields.String,
    'description': fields.String,
    'schedule': fields.DateTime,
    'idDoctor': fields.Integer,
    'idPatient': fields.Integer
}