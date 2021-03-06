# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Blueprint for version 1 of API
"""
import logging

from flask.ext.httpauth import HTTPBasicAuth
from flask import Blueprint
import flask
from oslo.config import cfg

from yabgp.api import utils as api_utils

LOG = logging.getLogger(__name__)
blueprint = Blueprint('v1', __name__)
auth = HTTPBasicAuth()


@auth.get_password
def get_pw(username):
    if username == cfg.CONF.rest.username:
        return cfg.CONF.rest.password
    return None


@blueprint.route('/')
def root():
    """
    v1 api root. Get the api status.

    **Example request**:

    .. sourcecode:: http

      GET /v1 HTTP/1.1
      Host: example.com
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json
      {
        "status": "stable",
        "updated": "2015-01-22T00:00:00Z",
        "version": "v1"
      }

    :status 200: the api can work.
    """
    intro = {
        "status": "stable",
        "updated": "2015-01-22T00:00:00Z",
        "version": "v1"}
    return flask.jsonify(intro)


@blueprint.route('/peers',  methods=['GET'])
@auth.login_required
def peers():
    """
    Get all peers realtime running information, include basic configurations and fsm state.

    **Example request**

    .. sourcecode:: http

      GET /v1/peers HTTP/1.1
      Host: example.com
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json

      {
          "peers": [
              {
                  "fsm": "ESTABLISHED",
                  "local_addr": "100.100.0.1",
                  "local_as": 65022,
                  "remote_addr": "100.100.9.1",
                  "remote_as": 65022,
                  "uptime": 106810.47324299812
              },
              {
                  "fsm": "ESTABLISHED",
                  "local_addr": "100.100.0.1",
                  "local_as": 65022,
                  "remote_addr": "100.100.9.1",
                  "remote_as": 65022,
                  "uptime": 106810.47324299812
              }
          ]
      }

    :status 200: the api can work.
    """
    return flask.jsonify(api_utils.get_peer_conf_and_state())


@blueprint.route('/peer/<peer_ip>/state')
@auth.login_required
def peer(peer_ip):
    """
    Get one peer's running information, include basic configurations and fsm state.

    **Example request**

    .. sourcecode:: http

      GET /v1/peer/10.124.1.245/state HTTP/1.1
      Host: example.com
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json
      {
        "peer": {
            "fsm": "ESTABLISHED",
            "local_addr": "10.75.44.11",
            "local_as": 23650,
            "remote_addr": "10.124.1.245",
            "remote_as": 23650,
            "uptime": 7.913731813430786
            }
        }

    :param peer_ip: peer ip address
    :status 200: the api can work.

    """
    return flask.jsonify(api_utils.get_peer_conf_and_state(peer_ip))


@blueprint.route('/peer/<peer_ip>/statistic')
@auth.login_required
def get_peer_statistic(peer_ip):
    """
    Get one peer's message statistic, include sending and receiving.

    **Example request**

    .. sourcecode:: http

      GET /v1/peer/10.124.1.245/statistic HTTP/1.1
      Host: example.com
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/json
      {
          "receive": {
              "Keepalives": 3,
              "Notifications": 0,
              "Opens": 1,
              "Route Refresh": 0,
              "Updates": 5
          },
          "send": {
              "Keepalives": 3,
              "Notifications": 0,
              "Opens": 1,
              "Route Refresh": 0,
              "Updates": 0
          }
      }

    :param peer_ip: peer ip address
    :status 200: the api can work.

    """
    return flask.jsonify(api_utils.get_peer_msg_statistic(peer_ip))
