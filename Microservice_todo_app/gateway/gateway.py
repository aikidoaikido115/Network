from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

USER_SERVICE_URL = os.getenv('USER_SERVICE_URL')


#เดี๋ยวทำระบบสมาชิกเพื่อบันทึกข้อมูลก่อน