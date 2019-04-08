#from models.event import Event
#from models.host import Host
from models.user import User # done
from models.user_tokens import UserTokens # done
#from models.event_attendees import EventAttendees
from exceptions.user_authentication_exception import UserAuthenticationException # done
#from exceptions.host_authentication_exception import HostAuthenticationException

def is_numeric(string):
    try:
        float(string)
        return True
    except:
        return False

def strings_not_empty(*strings):
    for string in strings:
        if len(string) == 0:
            return False
    return True

def boolean(string):
    if string in [1, '1', True, 'True', 'true', 't', 'T', 'y', 'Y', 'yes', 'Yes']:
        return True
    elif string in [0, '0', False, 'False', 'false', 'f', 'F', 'n', 'N', 'no', 'No']:
        return False
    raise Exception("Couldn't cast {} to a boolean".format(string))

# TODO: need to decide if we are going to use tokens from spotify or ours.
def authenticate_user(user_id, token, event_id=None):
    #user = User.query.filter(User.id == user_id, User.token == token).first()
    user_token = UserTokens.query.filter(
        UserTokens.user_id == user_id,
        UserTokens.token == token,
        UserTokens.deleted == False
    ).first()
    if user_token == None:
        raise UserAuthenticationException()
    #if event_id != None:
    #    event = EventAttendees.query.filter(
    #        EventAttendees.user_id == user_id,
    #        EventAttendees.event_id == event_id
    #    ).first()
    #    if event == None:
    #        raise UserAuthenticationException()
    return True

# def authenticate_host(host_id, token, event_id=None):
#     host_id = int(host_id)
#     host = Host.query.filter(Host.id == host_id, Host.token == token).first()
#     if host == None:
#         raise HostAuthenticationException()
#     if event_id != None:
#         event = Event.query.filter(
#             Event.id == event_id
#         ).first()
#         if event.host_id != host_id:
#             raise HostAuthenticationException()
#     return True
