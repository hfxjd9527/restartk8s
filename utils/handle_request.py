# coding: utf-8
from flask import request


def get_data_from_requst():
    return request.get_json(force=True)
