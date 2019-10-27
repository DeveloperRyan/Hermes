# Consumer Side
# --------------

# App saves data based on their face
# One account for any location
# User can 

# Back End
# --------------
# First time - User image taken, account created correlated to that face.
# Any other time - Account is found based on face

# Account creation
# --------------
# Image uploaded to S3 bucket
# Search faces by finding face ID (IndexFaces)
# If match found, find corresponding data in db
# Get transcation info, update database based on transcation amount / specials


# MVP
# --------------
# Image taken > uploaded to S31
# Face ID found
# Look up face ID in database
# Fetch transaction information
# Database updated based on transaction

# Rewards as database items (stock & price)
# Users can look at and redeem rewards, updates database


import boto3

client = boto3.client('rekognition') # Connect to rekognition client
s3 = boto3.client('s3') # Connect to s3 client

# AWS information
bucket = 'image-rewards'
collection = 'registered_faces'
fileInput = ''

# Create a collection within bucket to store and search images
def create_collection(collection):
    client.create_collection(CollectionId=collection)
    print('Collection created')

# Delete a collection
def delete_collection(collection):
    client.delete_collection(CollectionId=collection)
    print('Collection deleted')

# List all created collections
def list_collections(max_results):
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
def collection_facecount(collection):
    facecount_response = client.describe_collection(CollectionId=collection)
    return facecount_response['FaceCount']

# Index a face to a collection
def index_face(image, collection):
    indexResponse = client.index_faces(CollectionId=collection,
                    Image={'S3Object':{'Bucket':bucket, 'Name':image}},
                    MaxFaces=1,
                    QualityFilter='NONE')
    return indexResponse['FaceRecords'][0]['Face']['FaceId']

# Remove a list of faces from a collection
def delete_faces(face_ids, collection): # Pass a vector of faceIDs
    client.delete_faces(CollectionId=collection,
                        FaceIds=face_ids)

# Remove a single face from a collection
def delete_face(face_id, collection):
    face_id_list = [face_id]
    client.delete_faces(CollectionId=collection,
                        FaceIds=face_id_list )

# Searches for a specific face that matches a given image
def search_for_face(input, collection):
    searchResponse = client.search_faces_by_image(CollectionId=collection,
        Image={'S3Object':{'Bucket':bucket, 'Name':input}},
        FaceMatchThreshold=80,
        MaxFaces=2)
    return searchResponse['FaceMatches'][0]['Face']['FaceId']