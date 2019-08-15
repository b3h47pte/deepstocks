#!/usr/bin/env python

import argparse
from flask import Flask, jsonify, request
import deepstocks.data
app = Flask('apiServer')

parser = argparse.ArgumentParser()
parser.add_argument('--db', required=True)
args = parser.parse_args()

deepstocks.data.connectToDatabase(args.db)
session = deepstocks.data.createSession()

@app.route('/search')
def search():
    from deepstocks.data import findClosestNameSymbolMatch
    foundResults = findClosestNameSymbolMatch(
        session=session,
        inp=request.args.get('inp'),
        limit=request.args.get('limit', 10))
    return jsonify(foundResults)

if __name__ == '__main__':
    app.run()
