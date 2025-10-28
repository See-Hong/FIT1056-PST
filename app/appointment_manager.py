from app.models import Appointment, db

def create_new_appointment(date, time, reason, created_by, status, patient_id, doctor_id=None):
    """Created a new appointment from given parameters and commits to db"""
    new_appointment = Appointment(
                                date=date,
                                time=time,
                                reason=reason,
                                created_by=created_by,
                                status=status,
                                patient_id=patient_id,
                                doctor_id=doctor_id
                            )
    db.session.add(new_appointment)
    db.session.commit()
    return new_appointment

def appointment_cancel(appointment_id):
    """Cancels an appointment"""
    appointment = db.session.get(Appointment, appointment_id)
    if appointment:
        appointment.status = "Cancelled"
        db.session.commit()
        return appointment
    else:
        raise ValueError("Appointment not found")

def appointment_accept(appointment_id, doctor_id):
    """Marks an appointment as scheduled"""
    appointment = db.session.get(Appointment, appointment_id)
    if not appointment:
        raise ValueError
    appointment.doctor_id = doctor_id
    appointment.status = "Scheduled"
    db.session.commit()
    return appointment

def appointment_complete(appointment_id):
    """Marks an appointment as complete"""
    appointment = db.session.get(Appointment, appointment_id)
    if not appointment:
        raise ValueError
    appointment.status = "Completed"
    db.session.commit()
    return appointment