
# Azure Named Entitiy Recognition Service - Phyton

* ## Setting up:
        pip install --upgrade azure-cognitiveservices-language-textanalytics

For more information please read following link.
* ### Quickstart: Use the Text Analytics client library [(link)](https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/text-analytics-sdk?pivots=programming-language-python)

--------
## Python requirements
This code was tested on 
* Python 3.7
* TensorFlow 1.15
* Anaconda 2019.10
--------

## How to Use

* To use Azure named entitiy recognition, your text max. should be 5000 character and should be in plain text format (.txt)

* There are 3 main function in this repo
** split_doc(): split text document into smaller chunks (It will create new "splitted_doc/" folder and store all pieces into it)
** entity_recognition(): get entities in the text and create a csv table
** create_csv_with_number(): modify csv file and assign number to entities before replacement
** replace_entities('doc.txt','doc_NER.txt'): replace entities with assigned keyword and create new .txt file on main directory

* Rename your text file as: "doc.txt" and paste into main directory then run main.py

* It will automatically split your document and do the rest of the process and after the process it will remove temporary folders and files created during run.

* After the process there will be 2 new files. "doc_NER.txt" and "entities.csv"
        ** "doc_NER.txt": new text file replaced with keywords
        ** "entities.csv": list of the entities

## Possible issues

* ### Encountered exception. Operation returned an invalid status code 'Quota Exceeded' azure:


* Faced with this issue when try to run this code with 700 pages text file. It splited document into 4623 pieces and encountered after the half of the process.If you face with it don't stop process because at the end it will work without problem. 
        
     * Most probably after that you will face with new problem during run even if every line is right.(ie: UnboundLocalError: local variable 'response' referenced before assignment)-- It occurs due to quota exceeded. So you should create new Named Entitiy Recognition resource from Azure portal and paste new subscription_key and endpoint in the functions.py file.ck

     * Encountered exception. Unauthorized. Access token is missing, invalid, audience is incorrect (https://cognitiveservices.azure.com), or have expired.

     * Encountered exception. Error occurred in request., ConnectionError: HTTPSConnectionPool(host='er.cognitiveservices.azure.com', port=443): Max retries exceeded with url: /text/analytics/v2.1/entities (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x1140def10>: Failed to establish a new connection: [Errno 8] nodename nor servname provided, or not known'))

     * Possible solution: [(link)](https://gist.github.com/ejdoh1/3d1badd1fb20ea83ffa9415737b84584)
 
