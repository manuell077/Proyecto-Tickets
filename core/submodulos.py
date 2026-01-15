from tickets.models import tickets 

def queryset_tickets(usuario):
    return tickets.objects.filter(
        account_user_entity_id=usuario.id
    )

#Este es un diccionario que se guardo para pasarle el contexto necesario a cada formato cuando se vaya a mostrar los tickets ya creados
#Los keys principales como lo son 'manejo_tickets' son los nombres de los submodulos
SUBMODULOS = {
    'manejo_tickets':{
        'queryset': queryset_tickets,
        'formatos' : {
                    'hardware_revision': {
                    'nombre': 'Revision Hardware',
                    'fecha': lambda t: t.hardware_revision.created_at,
                    'observacion': lambda t: (
                    t.historial.order_by('-date_change').first().observation
                    if t.historial.exists() else ''
                   )
                },
                'low_team': {
                    'nombre': 'Baja de equipo',
                    'fecha': lambda t: t.low_team.created_at,
                     'observacion': lambda t: (
                    t.historial.order_by('-date_change').first().observation
                    if t.historial.exists() else ''
                   )
                },
                'equipment_delivery': {
                    'nombre': 'Entrega de equipos',
                    'fecha': lambda t: t.equipment_delivery.created_at,
                     'observacion': lambda t: (
                     t.historial.order_by('-date_change').first().observation
                     if t.historial.exists() else ''
                   )
                },
                'request_tics': {
                    'nombre': 'Solicitudes Tics',
                    'fecha': lambda t: t.request_tics.created_at,
                     'observacion': lambda t: (
                    t.historial.order_by('-date_change').first().observation
                    if t.historial.exists() else ''
                   )
                },
    }
 }
}