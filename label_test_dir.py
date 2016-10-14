#!/usr/bin/env python
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This script uses the Vision API's label detection capabilities to find a label
based on an image's content.

To run the example, install the necessary libraries by running:

    pip install -r requirements.txt

Run the script on an image to get a label, E.g.:

    ./label_test_dir.py <source-dir-with-images-to-classify> <destination-folder>
"""

# [START import_libraries]
import argparse
import base64
import os
import shutil

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
# [END import_libraries]

    # [START Main function containing 3 method calls]
def main(photo_source_dir,photo_classification_dir):
    """Run a label request on a multiple images in a folder"""
    service = authenticate()
    all_responses=vision_api_request(photo_source_dir,photo_classification_dir,service)
    classify_into_folders(photo_classification_dir,all_responses)
    # [END Main function containing 3 method calls]

def authenticate ():
    # [START authenticate]
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)
    return service;
    # [END authenticate]

def vision_api_request(photo_source_dir,photo_classification_dir,service):
    files=os.listdir(photo_source_dir)
     # [START Get list of all files in the dir with absolute path]
    counter=0
    responses=[]
    for index in range(len(files)):
        responses.append([])

    for file in files:
        abs_file=os.path.abspath(os.path.join(photo_source_dir, file))
       
        # [START construct_request]
        with open(abs_file, 'rb') as image:
            image_content = base64.b64encode(image.read())
            service_request = service.images().annotate(body={
                'requests': [{
                    'image': {
                        'content': image_content.decode('UTF-8')
                    },
                    'features': [{
                        'type': 'LABEL_DETECTION',
                        'maxResults': 1
                    }]
                }]
            })
        # [END construct_request] 
        
        # [START parse_response]
            response = service_request.execute()
            label = response['responses'][0]['labelAnnotations'][0]['description']
            #print('Found label: %s for %s' % (label, abs_file))
            responses[counter].append(label)
            responses[counter].append(abs_file)
        counter=counter+1
        print (responses)
        # [END parse_response]

        # [START create Classification Folder]
    return responses
def classify_into_folders(photo_classification_dir,all_responses):
    abs_dest_folder=os.path.abspath(photo_classification_dir)
    for response in all_responses:
        print (response)
        label_dir= os.path.join(abs_dest_folder,response[0])
        try:
            os.makedirs(label_dir)
        except OSError:
            pass
        shutil.copy(response[1],label_dir)
            # [END create Classification Folder]
      
    print ('Files can be found at %s' % (abs_dest_folder))


# [START run_application]
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_source_dir', help='The dir containing images you\'d like to label.')
    parser.add_argument('image_classify_dir', help='The dir will be the destination for folders created for Classification')
    args = parser.parse_args()
    main(args.image_source_dir, args.image_classify_dir)
# [END run_application]
