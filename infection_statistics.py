# Copyright 2015 Amazon Web Services, Inc. or its affiliates. All rights reserved.
 
from boto3.dynamodb.conditions import Key
import sys
from datetime import datetime, timedelta
import utils
 
INFECTIONS_TABLE_NAME = utils.LAB_S3_INFECTIONS_TABLE_NAME
CITY_DATE_INDEX_NAME = "InfectionsByCityDate"
 
 
def queryByCity(tableName=INFECTIONS_TABLE_NAME, cityName="Boston"):
    #Query Infections table based on the input city and counts number of infections
    countForCity = 0
    try:
        dynamodb = utils.connect2Service('dynamodb')
        myTable = dynamodb.Table(tableName)
        #STUDENT TODO: Query the Infections table with the tableName and region given as parameters
        recs = myTable.query(                                        #@Del
                            IndexName=CITY_DATE_INDEX_NAME,         #@Del
                            KeyConditionExpression=Key('City').eq(cityName),          #@Del
                            )        #@Del
        print("City: {0}".format(cityName))
        #Retrieves and prints from recs dictionary returned by the query.
        for rec in recs['Items']:
            print("\t", rec['PatientId'], rec['Date'])
        countForCity = len(recs['Items'])
        print("Count of Infections in the city:{0}".format(countForCity))
    except Exception as err:
        print("Error Message: {0}".format(err))
    return countForCity
 
 
if __name__ == '__main__':
    print("Query the table for a city:")
    queryByCity(cityName="Austin")