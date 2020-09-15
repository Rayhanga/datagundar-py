import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SAP_DIR = os.path.join(ROOT_DIR, 'SAP')

if not os.path.exists(SAP_DIR):
    os.makedirs(SAP_DIR)