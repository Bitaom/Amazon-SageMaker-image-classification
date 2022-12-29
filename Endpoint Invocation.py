import json
import numpy as np

runtime = boto3.client(service_name="sagemaker-runtime")


s3_bucket, s3_key = '', ''
s3 = boto3.resource('s3')
img = s3.Bucket(s3_bucket).download_file(s3_key, '/tmp/test.jpg')
file_name = '/tmp/test.jpg'
# test image
from IPython.display import Image
Image(file_name)
endpoint_name = " "
with open(file_name, 'rb') as f:
    payload = f.read()
    payload = bytearray(payload)
response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    Body=payload,
    ContentType='application/x-image',
)

result = response['Body'].read()
# result will be in json format and convert it to ndarray
result = json.loads(result)
print(result)
# the result will output the probabilities for all classes
# find the class with maximum probability and print the class index
index = np.argmax(result)
object_categories = ['negative', 'possitive']
print("Result: label - " + object_categories[index] + ", probability - " + str(result[index]))
