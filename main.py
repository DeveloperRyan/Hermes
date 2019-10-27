import boto3
from STVNetworkClass import CustomerDataTable as db
from datetime import datetime
import math

client = boto3.client('rekognition') # Connect to rekognition client
s3 = boto3.client('s3') # Connect to s3 client

# AWS information
bucket = 'image-rewards'
collection = 'registered_faces'
image_input = ''

# Create a collection within bucket to store and search images
def createCollection(collection):
    client.create_collection(CollectionId=collection)
    print('Collection created')

# Delete a collection
def deleteCollection(collection):
    client.delete_collection(CollectionId=collection)
    print('Collection deleted')

# List all created collections
def listCollections(max_results):
    collection_response = client.list_collections(MaxResults=max_results)
    collection_list = []

    # If not all collections were output, loop through and add the
    done = False
    for collection in collection_response['CollectionIds']:
        collection_list.append(collection)

    while done == False:
        if 'NextToken' in collection_response:
            nextToken = collection_response['NextToken']
            collection_response = client.list_collections(NextToken=nextToken)
            for collection in collection_response['CollectionIds']:
                 collection_list.append(collection)
        else:
            done = True
    return collection_list

# Get number of faces in a collection
def collectionFacecount(collection):
    facecount_response = client.describe_collection(CollectionId=collection)
    return facecount_response['FaceCount']

# Index a face to a collection
def indexFace(image, collection):
    index_response = client.index_faces(CollectionId=collection,
                    Image={'S3Object':{'Bucket':bucket, 'Name':image}},
                    MaxFaces=1,
                    ExternalImageId=image,
                    QualityFilter='NONE')
    id = index_response['FaceRecords'][0]['Face']['FaceId']
    db.addFaceID(id)
    return index_response['FaceRecords'][0]['Face']['FaceId']

# Remove a list of faces from a collection
def deleteFaces(face_ids, collection): # Pass a vector of faceIDs
    client.delete_faces(CollectionId=collection,
                        FaceIds=face_ids)

# Remove a single face from a collection
def deleteFace(face_id, collection):
    face_id_list = [face_id]
    client.delete_faces(CollectionId=collection,
                        FaceIds=face_id_list )
    db.removeFaceID(face_id)

# Searches for a specific face that matches a given image
def searchForFace(input, collection):
    search_response = client.search_faces_by_image(CollectionId=collection,
        Image={'S3Object':{'Bucket':bucket, 'Name':input}},
        FaceMatchThreshold=80,
        MaxFaces=1)
    
    response_list = [search_response['FaceMatches'][0]['Face']['FaceId'], search_response['FaceMatches'][0]['Face']['ExternalImageId']]
    print('FaceId: {} ImageId: {}'.format(response_list[0], response_list[1]))
    return response_list[0] # return faceId

# Returns list of all faceId's in a collection
def listFaces(collection):
    faces = {}
    list_response = client.list_faces(CollectionId=collection)
    for face in list_response['Faces']:
        faces.update({face['ExternalImageId'] : face['FaceId']})
    return faces

# Transaction Data
def create_transaction(face_id, price):
    db.addPoints(face_id, price_to_points(price))

# Convert dollar amount to price
def price_to_points(price):
    return math.floor(price * 10)

# Rewards Data
def redeem_points(face_id, price):
    db.removePoints(face_id, price)


# MAIN EXECUTION #
print('Welcome to Hermes, a project created at HackGT6!')
print('Hermes is a rewards program that uses facial recognition to give you rewards for all your shopping locations')
print('Hermes was developed by: Ryan Elliott & Sterling Cole with design help from Yash Vagal and Dakota Survance')
print('-------------------------------')

indexFace("2.jpg", collection)
print(db.getPoints(searchForFace("3.jpg", collection)))
db.addPoints(searchForFace("3.jpg", collection), 10000)
print(db.getPoints(searchForFace("3.jpg", collection)))