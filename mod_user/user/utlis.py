from random import randint
import smtplib
from email.message import EmailMessage
from flask import url_for
from app import redis, mail, Configs

from .models import User

def add_to_redis(user:User, mode:str)->int:
    token = randint(100_000, 999_999)
    name = f'{user.id}_{mode.lower()}'
    redis.set(
        name=name, value=token, ex=14400)
    
    return token


def get_from_redis(user:User, mode:str)->int|str:
    name = f'{user.id}_{mode.lower()}'
    return redis.get(name=name)

def delete_from_redis(user:User, mode:str)->None:
    name = f'{user.id}_{mode.lower()}'
    redis.delete(name)

def send_registration_message(user:User, token:int):
    msg  = EmailMessage()
    msg['Subject'] = 'Welcoome - Your email verification code'
    msg['From'] = Configs.MAIL_USERNAME
    msg['To'] = user.email
    msg.set_content(
        f"""Your email verification code : {
            url_for(
                'user.confirm_registration', 
                email=user.email, token=token,
                _external=True
                )}""")
    
    with smtplib.SMTP_SSL(
        host=Configs.MAIL_SERVER, port=Configs.MAIL_PORT) as server:

        server.login(Configs.MAIL_USERNAME,
                            Configs.MAIL_PASSWORD)
        
        server.send_message(msg)

