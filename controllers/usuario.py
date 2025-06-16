from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from utils import db, lm
from schemas.mensagem_schema import MensagemSchema

bp_usuario = Blueprint()