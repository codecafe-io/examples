# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.
 
import time
import utils
from botocore.exceptions import EndpointConnectionError
 
INFECTIONS_TABLE_NAME = utils.LAB_S3_INFECTIONS_TABLE_NAME
CITY_DATE_INDEX_NAME = "InfectionsByCityDate"
HTTP_STATUS_SUCCESS = 200
  
def removeTable(tableName=INFECTIONS_TABLE_NAME):
    #Removes the tableName from the region given as input
    rval = True
    if utils.isTableActive(tableName):
        try:
            rval = False
            dynamoDB = utils.connect2Service('dynamodb')
            table = dynamoDB.Table(tableName)
            resp = table.delete()
            if resp['ResponseMetadata']['HTTPStatusCode'] == HTTP_STATUS_SUCCESS:
                rval = True
                time.sleep(5)
                print("{0} Table has been deleted.".format(tableName))
        except Exception as err:
            print("Existing table deletion failed:{0} Table".format(tableName))
            print("Error Message: {0}".format(err))
            rval = False
    return rval
 
def createInfectionsTable(tableName=INFECTIONS_TABLE_NAME):
    rval = False
    dynamoDB = utils.connect2Service('dynamodb')
    #removeTable method is provided to clean up the created DynamoDB tables every time you run the code.
    if removeTable(tableName):
        try:
            #STUDENT TODO: Create Infections table with the fields, 'PatientId', 'City', and 'Date'
            #Specify the GlobalAllIndex name in the query
            table = dynamoDB.create_table(TableName=tableName,        #@Del         
                        KeySchema=[{'AttributeName':'PatientId', 'KeyType':'HASH'}],        #@Del         
                        AttributeDefinitions=[{'AttributeName':'PatientId', 'AttributeType':'S'},        #@Del
                                    {'AttributeName':'City', 'AttributeType':'S'},        #@Del
                                    {'AttributeName':'Date', 'AttributeType':'S'}],        #@Del
                        GlobalSecondaryIndexes=[{'IndexName': CITY_DATE_INDEX_NAME,        #@Del
                                    'KeySchema':[{'AttributeName': 'City', 'KeyType': 'HASH'},          #@Del
                                                {'AttributeName': 'Date', 'KeyType': 'RANGE'}],         #@Del 
                                    'Projection':{'ProjectionType': 'ALL'},      #@Del
                                    'ProvisionedThroughput':{'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5} }],      #@Del
                        ProvisionedThroughput={'ReadCapacityUnits':5, 'WriteCapacityUnits':10}         #@Del
                        )         #@Del
            #Wait for the table creation and the status to become active.
            time.sleep(5)
            if utils.isTableActive(tableName):
                rval = True
        except Exception as err:
            print("{0} Table could not be created".format(tableName))
            print("Error Message: {0}".format(err))
    return rval
 
if __name__ == '__main__':
    print("Infections Table creation:")
    isTableCreated = createInfectionsTable()
    print("Table created::{0}".format(isTableCreated))