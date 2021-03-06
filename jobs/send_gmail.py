# -*- coding: utf-8 -*-
# encoding: utf-8
from __future__ import print_function
import httplib2

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
from apiclient import errors

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
#SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'resources/client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        resource_path = os.path.join(os.path.split(__file__)[0], CLIENT_SECRET_FILE)
        flow = client.flow_from_clientsecrets(resource_path, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  
  message['from'] = sender
  message['to'] = to
  message['cc'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError, error:
    print('An error occurred: %s' % error)


def get_service_gmail():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    return service

def send(to, subject, sheet_id, txt_error):

    from_mail = 'mlacerda@ciandt.com'
    #to_mail = 'mlacerda@ciandt.com'  
    to_mail = '%s@ciandt.com' % to

    msg = 'Encontramos um erro ao processar o Mapa de Conhecimento Técnico do seu projeto \n\n'
    msg += 'https://docs.google.com/spreadsheets/d/%s \n\n' % str(sheet_id) 
    msg += 'Problema encontrado:\n\n'
    msg += '  %s\n\n' % txt_error
    msg += 'Possíveis soluções: \n\n'    
    msg += '  Erro [HttpError 403 when requesting]: Solução: Compartilhar acesso de leitura na planilha para mlacerda@ciandt.com ou para todos os usuarios do dominio ciandt \n\n'
    msg += '  Erro [could not convert string to float: #DIV/0!]: Solução: Revisar as fórmulas das colunas escondidas do lado direito da sheet Tecnology. Provavelmente você inclui novas linhas e não copiou as fórmulas dessas colunas. \n\n'
    msg += '  Erro [list index out of range]: Solução: Revisar as fórmulas das colunas escondidas do lado direito da sheet Tecnology. Provavelmente você inclui novas linhas e não copiou as fórmulas dessas colunas. \n\n\n\n'

    msg += 'Se o seu projeto não estiver utilizando essa planilha, pode removê-la. Obs: Lembre de exclui-la da lixeira do seu gdrive.\n\n'
    msg += 'Se o problema persistir entre em contato com Marcus Lacerda <mlacerda@ciandt.com> ou Leonel Togniolli <ltogniolli@ciandt.com>'

    service = get_service_gmail()

    message = create_message(from_mail, to_mail, subject, msg)
    send_message(service, from_mail, message)
    
if __name__ == '__main__':
    subject = 'ACTION REQUIRED: Tech Gallery'
    send('mlacerda', subject, '1MAyEuRubYjzELnfbPnO8YPjS9jW-Xm26xTSXQdO_EWM', "texto erro")