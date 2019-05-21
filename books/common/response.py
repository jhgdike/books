# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask import jsonify


def json_success(data=''):
    resp_json = {
        'code': 0,
        'data': data,
    }
    return jsonify(**resp_json)


def json_err(err, msg=''):
    resp_json = {
        'code': err,
        'msg': msg or err.label,
    }
    return jsonify(**resp_json)
