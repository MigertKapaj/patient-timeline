from flask import Flask
from flask.ext import restful
import json, datetime

app = Flask(__name__)
api = restful.Api(app)

database = json.load(open('data.json'))

def reindex(data=database, key='patient_id', primary_key=True):
    """
    Given the database index first by id then by data for use by the frontend
    :return:
    """
    if primary_key:
        indexed = {}
    else:
        indexed = []

    for record in data:
        record = dict(record)

        if primary_key:
            if record[key] not in indexed.keys():
                indexed[record[key]] = []

            indexed[record[key]].append({'date': record['date'], "element": [record]}) # hack this should be all records!
        else:
            indexed.append({'date': record['date'], "element": [record]})

    # sort the records by date
    # for subject in indexed:
    #     sorted_entries = []
    #
    #     for record in subject:
    #         record = sorted(record, key=lambda k: k['date'])
    #         sorted_entries.append(record)
    #
    #     sorted_indexed[subject] = sorted_indexed
    #
    # indexed = sorted_indexed

    return indexed

def sort_by_value():
    pass

class PatientRecords(restful.Resource):
    def get(self):
        """
        Get the patient record
        :return:
        """
        return reindex(database)

class PatientID(restful.Resource):
    def get(self, patient_id):
        """
        Given a patient ID, check the records and append records that match the
        patient id
        :param patient_id:
        :return:
        """
        response = []
        for record in database:
            record = dict(record)
            if int(record['patient_id']) == patient_id:
                response.append(record)

        return sorted(reindex(response, 'date', False), key=lambda x: x['date'])

# API endpoints
api.add_resource(PatientRecords, '/')
api.add_resource(PatientID, '/patient/<int:patient_id>/')


if __name__ == '__main__':
    app.run(debug=True)