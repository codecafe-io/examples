# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.
 
import sys
from datetime import datetime, timedelta
import utils
 
BUCKET_NAME = utils.LAB_S3_BUCKET_NAME
BUCKET_REGION = utils.LAB_S3_BUCKET_REGION
 
PATIENT_REPORT_PREFIX = utils.LAB_S3_PATIENT_REPORT_PREFIX
TABLE_NAME = utils.LAB_S3_INFECTIONS_TABLE_NAME
 
HTTP_STATUS_SUCCESS = 200
 
#Sample reports exist for patient ids 1, 2, 3
def linkPatientReport(tableName=TABLE_NAME):
    #Update Infections table item for patient ids 1, 2, 3 with the report url
    try:
        for i in range(1, 4):
            objectKey = PATIENT_REPORT_PREFIX + str(i) + ".txt";
            #STUDENT TODO: Construct the URL for the patient report.
            reportUrl = "https://s3-{0}.amazonaws.com/{1}/{2}".format(BUCKET_REGION, BUCKET_NAME, objectKey)    #@Del
            updateItemWithLink(i, reportUrl, tableName)
    except Exception as err:
        print("Error Message: {0}".format(err))
     
def updateItemWithLink(patientId, reportUrl, tableName):
    dynamodb = utils.connect2Service('dynamodb')
    myTable = dynamodb.Table(tableName)
    try:
        #STUDENT TODO: Update PatientReportUrl for the input PatientId 
        resp = myTable.update_item(                                         #@Del
                            Key={'PatientId': str(patientId)},        #@Del 
                            UpdateExpression='set PatientReportUrl=:val1',        #@Del 
                            ExpressionAttributeValues={':val1':{'S': reportUrl}})        #@Del
        print("Updated item:")
        print("PatientId:{0}, PatientReportUrl:{1}".format(patientId, reportUrl))
    except Exception as err:
        print("Error Message: {0}".format(err))
 
if __name__ == '__main__':
    print("Update report url for patient ids 1, 2, 3:")
    linkPatientReport()