from flask_restful import reqparse, inputs

#  Doctor Args
doctor_args = reqparse.RequestParser()
doctor_args.add_argument("name", type=str, help="Nome é obrigatório", required=True)
doctor_args.add_argument("crm", type=str, help="CRM é obrigatório", required=True)
doctor_args.add_argument("crmUf", type=str, help="CRM é obrigatório", required=True)
#  Doctor Args

# Patient Args
patient_args = reqparse.RequestParser()
patient_args.add_argument("name", type=str, help="Nome é obrigatório", required=True)
patient_args.add_argument("birthdate", type=inputs.datetime_from_iso8601, help="Data de Nascimento é obrigatória", required=True)
patient_args.add_argument("cpf", type=str, help="CPF é obrigatório", required=True)
patient_args.add_argument("idDoctor", type=int, help="Um médico precisa ser indicado para conclusão do cadastro", required=True) # Todo paciente deve estar vinculado a um médico
# Patient Args

# Patient Filter Args
patient_filter_args = reqparse.RequestParser()
patient_filter_args.add_argument("idDoctor", type=int, help="ID DOCTOR IS REQUIRED", required=True)
# Patient Fitler Args


# Medical Appointment
medicappoint_args = reqparse.RequestParser()
medicappoint_args.add_argument("description", help="Descrição é obrigatória", type=str, required=True)
medicappoint_args.add_argument("schedule", help="Agendamento é obrigatório", type=inputs.datetime_from_iso8601, required=True)
medicappoint_args.add_argument("idDoctor", help="Indicar um Médico é obrigatório", type=int, required=True)
medicappoint_args.add_argument("idPatient", help="Indicar um Paciente é obrigatório", type=int, required=True)
# Medical Appointment