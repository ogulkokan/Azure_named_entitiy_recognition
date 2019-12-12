# -*- coding: utf-8 -*-
import os
import csv
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from tqdm import tqdm
import re
import pandas as pd
import shutil

### Split "doc.txt" file into smaller chunks--------------------------------------------------------------------------------
path = "doc.txt"
def split_doc():
    os.mkdir('splitted_doc')
    def chunks(l, n):
    #Chunks iterable into n sized chunks
        for i in range(0, len(l), n):
            yield l[i:i + n]

    # Collect all lines, without loading whole file into memory
    lines = []
    with open(path) as main_file:
        for line in main_file:
            lines.append(line)

    # Write each group of lines to separate files
    for i, group in enumerate(chunks(lines, n=15), start=1):
        with open('splitted_doc/File%d.txt' % i, mode="w") as out_file:
            for line in group:
                out_file.write(line)
#######------------------------------------------------------------------------------------------------------------------------


####### Azure Cognitive Services --------------------------------------------------------------------------
subscription_key = '02d27236595e4de1b00fb1805582c2a8'
endpoint = 'https://francecentral.api.cognitive.microsoft.com/'

def authenticateClient():
    credentials = CognitiveServicesCredentials(subscription_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credentials=credentials)
    return text_analytics_client

def entity_recognition():
    client = authenticateClient()

    datafolder = 'splitted_doc'
    #Finds all files in datafolder
    filenames = os.listdir(datafolder)
    
    entities = {}

    for filename in tqdm(filenames):
        if filename in ('.DS_Store'):
            continue
        # print(filename) 
        path = os.path.join(datafolder,filename)
        with open(path, "r") as f:
            fileText = f.read()
        
        try:
            documents = [{"id": "1", "language": "de", "text": fileText}]
            response = client.entities(documents=documents)
        except Exception as err:
            print("Encountered exception. {}".format(err))

                        
        for document in response.documents:
            for entity in document.entities:
                if (entity.name not in entities.keys()) & (entity.name not in ['','.']):
                    entities[entity.name] = [entity.name,entity.type,entity.sub_type]
        
            filename_out = 'output.csv'

    try:
        os.remove(filename_out)
    except:
        print('no such file')

    with open(filename_out, 'a', newline='') as open_writable_file:
        writer = csv.writer(open_writable_file)
        # writer.writeheader(['name', 'type','sub_type'])  # write a row the fieldnames
        for key in entities.keys():
            row = entities[key]
            writer.writerow(row)
    
    
    return

#######------------------------------------------------------------------------------------------------------------------------


##### Replace entities inside original documents ----------------------------------------------------------------------------------

def replace_entities(path_to_doc,path_to_cleaned_doc):
    """

    df ıs df of entıtıes and replace name
    """
    df = pd.read_csv('output.csv',header=None,names=('Entity','type','sub_type'))

    df.sort_values(by='type',inplace=True)
    groups=df.groupby('type', as_index=False)

    df['col_c']=groups.cumcount()

    df['replace_name']=df.type.str.cat(df.col_c.astype(str), sep="_")
    df.drop(['col_c'],axis=1)

    df.to_csv('entities_table.csv',index=False)

    drop_rows = 'entities_table.csv'
    df = pd.read_csv('entities_table.csv')

    df = df[df.type != 'DateTime']  #drop rows if type column has DateTime
    df= df[df.type != 'Organization'] #drop rows if type column has Organization
    df= df[df.type != 'Quantity']   #drop rows if type column has Quantitiy
    df= df[df.type != 'URL'] #drop rows if type column has URL
    df= df[df.type != 'Phone_Number'] #drop rows if type column has phone number
    df= df[df.type != 'Email'] #drop rows if type column has email
    df= df[df.type != 'IP_Adress'] #drop rows if type column has email
    df= df.drop(['sub_type'], axis=1) #for only name and location we dont need subtype because it is empty column always
    df=df.drop(['col_c'], axis=1) #this column assign numbers only so for the final output it doesn't necessary
    df.to_csv('entities_table.csv',index=False)


    with open(path_to_doc,'r') as f:
        book=f.read()


    for i in tqdm(range(df.shape[0])):
        p = re.compile((r'(\b' + df.iloc[i].Entity + r'\b)|(\b' \
            + df.iloc[i].Entity + r'[s]\b)'))
        book = p.sub('[' + df.iloc[i].replace_name + ']',book)
        

    with open(path_to_cleaned_doc,'w') as f:
        f.write(book)

    shutil.rmtree('splitted_doc')
    os.remove('output.csv')


#######------------------------------------------------------------------------------------------------------------------------

