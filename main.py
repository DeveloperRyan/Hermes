import boto3

client = boto3.client('rekognition')
s3 = boto3.client('s3')

bucket = 'image-rewards'
collection = 'registered_faces'
fileInput = ''



def create_collection(collection):
    client.create_collection(CollectionId=collection)
    print('Collection created')

def delete_collection(collection):
    client.delete_collection(CollectionId=collection)
    print('Collection deleted')

def list_collections(max_results):
    collection_response = client.list_collections(MaxResults=max_results)
    collection_list = []

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
    return(collection_list)


def index_face(image, collection):
    indexResponse = client.index_faces(CollectionId=collection,
                    Image={'S3Object':{'Bucket':bucket, 'Name':image}},
                    MaxFaces=1,
                    QualityFilter='NONE')
    return indexResponse['FaceRecords'][0]['Face']['FaceId']

def delete_faces(faceIds, collection): # Pass a vector of faceIDs
    client.delete_faces(CollectionId=collection,
                                FaceIds=faceIds)

def search_for_face(image, collection):
    searchResponse = client.search_faces_by_image(CollectionId=collection,
                Image={'S3Object':{'Bucket':bucket, 'Name':fileInput}},
                FaceMatchThreshold=80,
                MaxFaces=2)
    return searchResponse['FaceMatches'][0]['Face']['FaceId']