#@copyrights of Aeshana Shalindra Udadeniya UoM FIT
# coding: utf8

import spacy
import re
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
import math
import numpy as np
import json
import argparse
import sys
import boto3
import pdfminer.settings
pdfminer.settings.STRICT = False
import pdfminer.high_level
import pdfminer.layout
import os.path
import multiprocessing.pool
import functools
from pdfminer.image import ImageWriter
import requests
from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
from flask_socketio import send, emit
import urllib.request
from urllib.request import urlretrieve


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


class w1(object):
    text=""
class w2(object):
    text=""
class w3(object):
    text = ""
BANKDependency=""
BANKindex=""
BODDependency=""
BODindex=""
ESTATEDependency=""
ESTATEindex=""
EXPORTDependency=""
EXPORTindex=""
LAWDependency=""
LAWindex=""
NORPDependency=""
NORPindex=""
PARTNERDependency=""
PARTNERindex=""
PRODUCTependency=""
PRODUCTindex=""

@app.route('/run', methods=['POST'])
def get_data():
   
    handle_message("Srating backend process...")
    global BANKDependency
    BANKDependency=request.args.get('BANKDependency')
    print(BANKDependency)
    global BANKindex
    BANKindex= request.args.get('BANKindex')
    print(BANKindex)
    global BODDependency
    BODDependency=request.args.get('BODDependency')
    global BODindex
    BODindex= request.args.get('BODindex')
    global ESTATEDependency
    ESTATEDependency = request.args.get('ESTATEDependency')
    global ESTATEindex
    ESTATEindex= request.args.get('ESTATEindex')
    global EXPORTDependency
    EXPORTDependency = request.args.get('EXPORTDependency')
    global EXPORTindex
    EXPORTindex = request.args.get('EXPORTindex')
    global LAWDependency
    LAWDependency = request.args.get('LAWDependency')
    global LAWindex
    LAWindex = request.args.get('LAWindex')
    global NORPDependency
    NORPDependency = request.args.get('NORPDependency')
    global NORPindex
    NORPindex = request.args.get('NORPindex')
    global PARTNERDependency
    PARTNERDependency = request.args.get('PARTNERDependency')
    global PARTNERindex
    PARTNERindex = request.args.get('PARTNERindex')
    global PRODUCTependency
    PRODUCTependency = request.args.get('PRODUCTependency')
    global PRODUCTindex
    PRODUCTindex = request.args.get('PRODUCTindex')
    print(PRODUCTindex)
    main_code(request.args.get('dir'),request.args.get('copm'),request.args.get('pdf'))
    return "done"

def main_code(directory, company, pdf):
    

    handle_message("converting pdf to text file...")
    args = ['-o '+company , '-od '+directory, pdf]
    nlp = spacy.load('E:/L4/FYP/FYP_repo/FYP/NLP/modals/plantations/new')
    P = maketheparser()
    A = P.parse_args(args=args)
    A.files=pdf
    A.output_directory=directory
    A.outfile=company
    save_path = A.output_directory
    name_of_file = A.outfile
    raw_text_path = os.path.join(save_path+"/", name_of_file + ".txt")
    edited_text_path = os.path.join(save_path+"/", name_of_file+"_edited" + ".txt")
    A.outfile=raw_text_path


    try:
        extract_text(**vars(A))
    except:
        print("timed out")
        handle_message("problem with pdf.. timed out")
        nlp.add_pipe(remove_whitespace_entities, after='ner')
        pre_process(raw_text_path, edited_text_path)
    else:
       
        nlp.add_pipe(remove_whitespace_entities, after='ner')
        pre_process(raw_text_path,edited_text_path)
    handle_message("done extracting text.. starting entity extraction")
    TEXTS = open(edited_text_path, encoding="utf8")

    people_relations = []
    estate_relations = []
    country_relations = []
    law_relations = []
    norp_relations = []
    partner_relations=[]
    company_relations=[]
    date_relations=[]
    product_relations=[]
    bank_relations=[]

    gpe_search_list=['Estate','Estates']
    exports_search_list = ['Export', 'Exports', 'buyer','exporters']
    people_search_list = ['Director', 'Directors', 'Chairman',]
    law_search_list=[]
    norp_search_list=[]
    partner_search_list=['subsidiary','parent','partnerships','partnership']
    company_search_list = ['PLC']
    date_search_list=['period','to','financial year','for the year ended','ended']
    product_search_list=[]
    bank_search_list=['bank']

    people_token=['PERSON']
    gpe_token = ['GPE','FAC']
    org_token=['ORG']
    export_token = ['GPE','FAC']
    law_token = ['LAW']
    norp_token = ['NORP']
    date_token=['DATE']
    product_token=['PRODUCT']
    bank_token=['ORG','NORP']

    for text in TEXTS:
        doc = nlp(text)
        people_relations=extract_relations(doc,people_relations,people_search_list,people_token,0,int(BODDependency))
        estate_relations = extract_relations(doc,estate_relations,gpe_search_list,gpe_token,2,int(ESTATEDependency))
        partner_relations=extract_relations(doc,partner_relations,partner_search_list,org_token,2,int(PARTNERDependency))
        country_relations = extract_relations(doc,country_relations,exports_search_list,export_token,4,int(EXPORTDependency))
        law_relations = extract_relations(doc,law_relations,law_search_list,law_token,0,int(LAWDependency))
        norp_relations = extract_relations(doc,norp_relations,norp_search_list,norp_token,0,int(NORPDependency))
        company_relations = extract_relations(doc, company_relations, company_search_list, org_token, 1, 1)
        date_relations=extract_relations(doc,date_relations,date_search_list,date_token,3,1)
        product_relations = extract_relations(doc, product_relations, product_search_list, product_token, 0, int(PRODUCTependency))
        bank_relations = extract_relations(doc, bank_relations, bank_search_list, bank_token, 0,int(BANKDependency))

    new_people_relations=[]
    new_estate_relations = []
    new_country_relations = []
    new_law_relations = []
    new_norp_relations = []
    new_partner_relations=[]
    new_company_relations=[]
    new_date_relations=[]
    new_product_relations=[]
    new_bank_relations=[]

    print("Done extracting entities")
    handle_message("done extracting all entites..sending for similarity checks")
    similarity_check(people_relations,new_people_relations,0.6)
    print("done finding BOD")
    handle_message("done listing BOD from dependency parsing...")
    similarity_check(estate_relations, new_estate_relations, 0.6)
    print("done finding estates")
    handle_message("done listing estates from dependency parsing...")
    similarity_check(country_relations, new_country_relations, 0.6)
    print("done finding exporting cont")
    handle_message("done listing exporing parties from dependency parsing...")
    similarity_check(law_relations, new_law_relations, 0.4)
    print("done finding laws")
    handle_message("done listing laws and regulations from dependency parsing...")
    similarity_check(norp_relations, new_norp_relations, 0.6)
    print("done finding norp")
    handle_message("done listing governing bodies from dependency parsing...")
    similarity_check(partner_relations, new_partner_relations, 0.6)
    print("done finding org")
    handle_message("done listing partnering companies from dependency parsing...")
    similarity_check(company_relations, new_company_relations, 0.9)
    print("done finding company")
    handle_message("done finding focal company from dependency parsing...")
    similarity_check(date_relations,new_date_relations,0.9)
    print("done finding dates")
    handle_message("done listing date relations from dependency parsing...")
    similarity_check(product_relations, new_product_relations, 0.8)
    print("done finding products")
    handle_message("done listing all relevent products from dependency parsing...")
    similarity_check(bank_relations, new_bank_relations, 0.8)
    print("done finding banks")
    handle_message("done listing banking entites from dependency parsing...")




    outlist=[]
    append_list(new_partner_relations, outlist,1,1)
    #append_list(new_product_relations, outlist, 1, 3)
    append_list(new_estate_relations, outlist, 1, 1)
    #append_list(new_law_relations, outlist,1,2)
    #append_list(new_norp_relations, outlist,1,2)
    #append_list(new_people_relations,outlist,0,1)
    #append_list(new_country_relations, outlist,1,1)
    lists = get_date(find_highest(new_date_relations))
    for_react = [{
        "name": find_highest(new_company_relations),
        "attributes": {
            "Industry": "Plantation",
            "since": lists[1],
            "until": lists[0]
        },
        "children": [
            {
                "name": "Board of Directors",
                "attributes": convert_to_front_end(new_people_relations, 0, int(BODindex))
            },
            {
                "name": "Estates",
                "attributes": convert_to_front_end(new_estate_relations, 1, int(ESTATEindex))
            },
            {
                "name": "products",
                "attributes": convert_to_front_end(new_product_relations, 1, int(PRODUCTindex))
            },
            {
                "name": "partners",
                "attributes": convert_to_front_end(new_partner_relations, 1, int(PARTNERindex))
            },
            {
                "name": "relevant laws",
                "attributes": convert_to_front_end(new_law_relations, 1, int(LAWindex))
            },
            {
                "name": "relevant governing bodies",
                "attributes": convert_to_front_end(new_norp_relations, 1, int(NORPindex))
            },
            {
                "name": "exporting entities",
                "attributes": convert_to_front_end(new_country_relations, 1, int(EXPORTindex))
            },
            {
                "name": "relevant banks",
                "attributes": convert_to_front_end(new_bank_relations, 1, int(BANKindex))
            }
        ]
    }
    ]
    data_struct = {
        "company_name": find_highest(new_company_relations),
        "Industry":"Plantation",
        "since": lists[1],
        "until": lists[0],
        "People":new_people_relations,
        "Estates":new_estate_relations,
        "Products":new_product_relations,
        "Partners":new_partner_relations,
        "laws":new_law_relations,
        "norp":new_norp_relations,
        "exports":new_country_relations,
        "banks": new_bank_relations
    }

    data = {
        "company_name":find_highest(new_company_relations),
        "since":lists[1],
        "until":lists[0],
        "keywords":outlist
    }
    handle_message("importing results....")
    writeToJSONFile(save_path, name_of_file+"_all_key_words", data_struct)
    writeToJSONFile(save_path, name_of_file+"_for_api", data)
    writeToJSONFile(save_path, name_of_file + "_for_react", for_react)

    #writeToS3(data,"key_words_for_api")
    writeToS3(for_react, "front_end_data")
    ########################################################make post request ######################
    #if postToEndPoint('https/aaaaaaaaaa',data )==1:
    #    print("the data has been sent")
    #else:
    #    print("data could not be sent")

    print("the following are the Directors and the chairman of the organization \n")
    print_output(new_people_relations,0,int(BODindex)) # 2nd parameter is whether to remove punctuations and the 3rd is print if the entity occured more than x time
    print("the following are the locations of Estates  \n")
    print_output(new_estate_relations,1,int(ESTATEindex))
    print("the following are the Products produced by organisation   \n")
    print_output(new_product_relations, 1, int(PRODUCTindex))
    print("the following are the Exporting Countries and export related entities \n")
    print_output(new_country_relations,1,int(EXPORTindex))
    print("the following are the laws binding  \n")
    print_output(new_law_relations,1,int(LAWindex))
    print("the following are the governing bodies  \n")
    print_output(new_norp_relations,1,int(NORPindex))
    print("the following are the partner orgs and subsidiaries   \n")
    print_output(new_partner_relations,1,int(PARTNERindex))
    print("the following are the banks related to the company   \n")
    print_output(new_bank_relations, 1, int(BANKindex))
    print(find_highest(new_company_relations))
    lists=get_date(find_highest(new_date_relations))
    print(lists[0])
    print(lists[1])

    return "done"

@socketio.on('message')
def handle_message(message):
    socketio.emit('message',message,broadcast=True)
    print("socket active")

def timeout(max_timeout):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator

def convert_to_front_end(list,filters,prominant):
    pl = []
    for r1, r2, r3 in list:
        if len(r2) > 5 and r1:
            if filters == 1:
                if prominant < 2:
                    pl.append([re.sub(r'[^\w\s]', '', r2), r3])
                elif r3 >= prominant:
                    pl.append([re.sub(r'[^\w\s]', '', r2), r3])
            else:
                if prominant < 2:
                    pl.append([r2, r3])
                elif r3 >= prominant:
                    pl.append([r2, r3])
    b = dict(pl)
    return b

def pre_process(in_file,out_file):
    totDoc = ""
    with open(in_file, "r", encoding="utf8") as ins:
        s = ""
        for line in ins:
            if len(line) >= 5 and line.isdigit() == False:
                if bool(re.match('^(?=.*[a-zA-Z])', line)) == True:
                    line_new = line.rstrip()
                    search_list = ['Ltd.', 'Mr.', 'Rs.', 'Mrs.', 'No.', 'Dr.', 'Inc.', '.com', 'BSc.', 'Contd.', 'www.','etc.','Miss.','miss.']
                    if line_new.find('.') != -1:  # found full stop
                        c, d = line_new.split('.', 1)
                        x=len(c)
                        if x>0:
                            if re.compile('|'.join(search_list), re.IGNORECASE).search(line_new) or c[x-1].isdigit():
                                s += line_new + ' '
                            else:
                                a, b = line_new.split('.', 1)
                                s += a + '.\n'
                                totDoc += s
                                s = b + ' '
                        else:
                            if re.compile('|'.join(search_list), re.IGNORECASE).search(line_new):
                                s += line_new + ' '
                            else:
                                a, b = line_new.split('.', 1)
                                s += a + '.\n'
                                totDoc += s
                                s = b + ' '
                    else:
                        s += line_new + ', '
    write = open(out_file, 'w', encoding="utf8")
    write.write(totDoc)
    write.close()
    print("Done pre-processing text")

def get_date(date_in_words):
    year=""
    day=""
    month=""
    days=[]
    day_list=['31','30','29','28','st']
    month_list=['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    words=date_in_words.split("_")
    for r in words:
        if '20' in r:
            years=re.findall(r'\d+',r)
            if years[0]:
                year = str(years[0])
        for dd in day_list:
            if dd in r:
                daily=re.findall(r'\d+',r)
                if daily[0]:
                    day=str(daily[0])
        for dd in month_list:
            if dd in r.lower():
                s = r.strip()[:3].lower()
                month=str(month_list.index(s)+1)
    out=year+"-"+month+"-"+day
    days.append(out)
    if(int(month)==12):
        days.append((year + "-" + "01" + "-" + "01"))
    else:
        new_month=str(int(month) +1)
        new_year=str(int(year)-1)
        out= new_year+"-"+new_month+"-01"
        days.append(out)
    return days

def find_highest(entity_list):
    temp=0
    entity=""
    for r1,r2,r3 in entity_list:
        if r3>temp:
            temp=r3
            entity=r2
    out=re.sub(r'[^\w\s]','',entity)
    return out.replace(" ","_")

def append_list(in_inst,out_list,filters,prominant):
    for r1,r2,r3 in in_inst:
        if len(r2)>5 and r1:
            if filters==1:
                if prominant<2:
                    out_list.append(re.sub(r'[^\w\s]','',r2))
                elif r3>=prominant:
                    out_list.append(re.sub(r'[^\w\s]', '', r2))
            else:
                if prominant < 2:
                    out_list.append(r2)
                elif r3 >= prominant:
                    out_list.append(r2)

def similarity_check(list_of_items,new_list_of_items,threshold):
    for i in range(len(list_of_items)):
        a = 1
        if i < len(list_of_items) and list_of_items[i].ent_type_:
            b=0
            for j in range(i + 1, len(list_of_items)+b):
                if j < len(list_of_items)+b:
                    if similarity(re.sub(r'[^\w\s]','',(list_of_items[i].text.lower())), re.sub(r'[^\w\s]','',(list_of_items[j-b].text.lower())), True) > threshold: # remove translate part if dont need to remove punctuations
                        a += 1
                        if len(list_of_items[i].text) > len(list_of_items[j-b].text):
                            del list_of_items[j-b]
                            b +=1
                        else:
                            list_of_items[i] = list_of_items[j-b]
                            del list_of_items[j-b]
                            b += 1
        if i < len(list_of_items) and list_of_items[i].text != 'applied':
            new_list_of_items.append((list_of_items[i].ent_type_,list_of_items[i].text, a))

def print_output(lists,filters,prominant):
    for r1, r2,r3 in lists:
        if len(r2)>5 and r1:
            if filters==1:
                if prominant<2:
                    print('{:<10}\t{}\t{}'.format(r1, re.sub(r'[^\w\s]','',r2),r3))
                elif r3>=prominant:
                    print('{:<10}\t{}\t{}'.format(r1, re.sub(r'[^\w\s]', '', r2), r3))
            else:
                if prominant < 2:
                    print('{:<10}\t{}\t{}'.format(r1, r2,r3))
                elif r3 >= prominant:
                    print('{:<10}\t{}\t{}'.format(r1, r2, r3))
    print("\n")

def merge_list(doc):
    # merge entities and noun chunks into one token
    spans = list(doc.ents) + list(doc.noun_chunks)
    for span in spans:
        span.merge()

def extract_relations(doc,relations,search_list_normal,token,search_level,advanced_filter):
    # merge entities and noun chunks into one token
    merge_list(doc)
    search_list = [x.lower() for x in search_list_normal]
    if advanced_filter==1:
        for entity in filter(lambda w: w.ent_type_ in token, doc):
            if re.compile('|'.join(search_list), re.IGNORECASE).search(entity.text):
                subject1 = [w for w in entity.lefts if w.text.lower() in search_list]
                subject2 = [w for w in entity.rights if w.text.lower() in search_list]
                split = entity.text.split(' ')
                subject3 = [w3 for w3.text in split if w3.text.lower() in search_list]
                if subject1 or subject2 or subject3:
                    relations.append(entity)
            else:
                subject1 = [w for w in entity.lefts if w.text.lower() in search_list]
                subject2 = [w for w in entity.rights if w.text.lower() in search_list]
                if search_level > 0:
                    listt = add_head(entity,search_level)#2
                    subject3= [w for w in listt if re.compile('|'.join(search_list), re.IGNORECASE).search(w.text)]
                    if subject1 or subject2 or subject3:
                        relations.append(entity)
                else:
                    if subject1 or subject2:
                        relations.append(entity)
    else:
        for entity in filter(lambda w: w.ent_type_ in token, doc):
            relations.append(entity)

    return relations

def add_head(root,level):
    # loop  to generate the number of heads needed fo the root to check for keywords
    heads=[]
    for x in range(level): #form 0 to x-1
        root=root.head
        heads.append(root)
    return heads

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)

def postToEndPoint(url,payload):
    r = requests.post(url, data=json.dump(payload))
    if r.status_code == requests.codes.ok:
        return 1
    else:
        return 0


def read_json(path, fileName):
    filePathNameWExt = path + '/' + fileName + '.json'
    with open(filePathNameWExt) as f:
        data = json.load(f)
    return data

def writeToS3(json_data,name):
    session = boto3.Session(
        aws_access_key_id='AKIAJC7S24JKRFDQAGVA',
        aws_secret_access_key='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',
    )
    s3 = session.resource("s3")

    #s3.Bucket('finalyearprojectresources').put_object(Key='test.jpg', Body=data)

    s3object = s3.Object('finalyearprojectresources', name+'.json')

    s3object.put(
        Body=(bytes(json.dumps(json_data).encode('UTF-8')))
    )
############################################################################################################3json##############################################################

################################################semantic similarity ###################################################################

# Parameters to the algorithm. Currently set to values that was reported
# in the paper to produce "best" results.
ALPHA = 0.2
BETA = 0.45
ETA = 0.4
PHI = 0.2
DELTA = 0.85

brown_freqs = dict()
N = 0


######################### word similarity ##########################

def get_best_synset_pair(word_1, word_2):
    max_sim = -1.0
    synsets_1 = wn.synsets(word_1)
    # print "line 26..........synset ...."+ str(synsets_1)
    synsets_2 = wn.synsets(word_2)

    if len(synsets_1) == 0 or len(synsets_2) == 0:
        return None, None
    else:
        max_sim = -1.0
        best_pair = None, None
        for synset_1 in synsets_1:
            for synset_2 in synsets_2:
                sim = wn.path_similarity(synset_1, synset_2)
                if sim == None:
                    sim = 0
                if sim > max_sim:
                    max_sim = sim
                    best_pair = synset_1, synset_2
        return best_pair


def length_dist(synset_1, synset_2):
    l_dist = sys.maxsize
    if synset_1 is None or synset_2 is None:
        return 0.0
    if synset_1 == synset_2:
        # if synset_1 and synset_2 are the same synset return 0
        l_dist = 0.0
    else:
        wset_1 = set([str(x.name()) for x in synset_1.lemmas()])
        wset_2 = set([str(x.name()) for x in synset_2.lemmas()])
        if len(wset_1.intersection(wset_2)) > 0:
            # if synset_1 != synset_2 but there is word overlap, return 1.0
            l_dist = 1.0
        else:
            # just compute the shortest path between the two
            l_dist = synset_1.shortest_path_distance(synset_2)
            if l_dist is None:
                l_dist = 0.0
    # normalize path length to the range [0,1]
    return math.exp(-ALPHA * l_dist)


def hierarchy_dist(synset_1, synset_2):
    h_dist = sys.maxsize
    if synset_1 is None or synset_2 is None:
        return h_dist
    if synset_1 == synset_2:
        # return the depth of one of synset_1 or synset_2
        h_dist = max([x[1] for x in synset_1.hypernym_distances()])
    else:
        # find the max depth of least common subsumer
        hypernyms_1 = {x[0]: x[1] for x in synset_1.hypernym_distances()}
        hypernyms_2 = {x[0]: x[1] for x in synset_2.hypernym_distances()}
        lcs_candidates = set(hypernyms_1.keys()).intersection(
            set(hypernyms_2.keys()))
        if len(lcs_candidates) > 0:
            lcs_dists = []
            for lcs_candidate in lcs_candidates:
                lcs_d1 = 0
                if lcs_candidate in hypernyms_1:
                    lcs_d1 = hypernyms_1[lcs_candidate]
                lcs_d2 = 0
                if lcs_candidate in hypernyms_2:
                    lcs_d2 = hypernyms_2[lcs_candidate]
                lcs_dists.append(max([lcs_d1, lcs_d2]))
            h_dist = max(lcs_dists)
        else:
            h_dist = 0
    return ((math.exp(BETA * h_dist) - math.exp(-BETA * h_dist)) /
            (math.exp(BETA * h_dist) + math.exp(-BETA * h_dist)))


def word_similarity(word_1, word_2):
    synset_pair = get_best_synset_pair(word_1, word_2)
    return (length_dist(synset_pair[0], synset_pair[1]) *
            hierarchy_dist(synset_pair[0], synset_pair[1]))


######################### sentence similarity ##########################

def most_similar_word(word, word_set):
    max_sim = -1.0
    sim_word = ""
    for ref_word in word_set:
        sim = word_similarity(word, ref_word)
        if sim > max_sim:
            max_sim = sim
            sim_word = ref_word
    return sim_word, max_sim


def info_content(lookup_word):
    global N
    if N == 0:
        # poor man's lazy evaluation
        for sent in brown.sents():
            for word in sent:
                word = word.lower()
                if word not in brown_freqs:
                    brown_freqs[word] = 0
                brown_freqs[word] = brown_freqs[word] + 1
                N = N + 1
    lookup_word = lookup_word.lower()
    n = 0 if lookup_word not in brown_freqs else brown_freqs[lookup_word]
    return 1.0 - (math.log(n + 1) / math.log(N + 1))


def semantic_vector(words, joint_words, info_content_norm):
    sent_set = set(words)
    semvec = np.zeros(len(joint_words))
    i = 0
    for joint_word in joint_words:
        if joint_word in sent_set:
            semvec[i] = 1.0
            if info_content_norm:
                semvec[i] = semvec[i] * math.pow(info_content(joint_word), 2)
        else:
            sim_word, max_sim = most_similar_word(joint_word, sent_set)
            semvec[i] = PHI if max_sim > PHI else 0.0
            if info_content_norm:
                semvec[i] = semvec[i] * info_content(joint_word) * info_content(sim_word)
        i = i + 1
    return semvec


def semantic_similarity(sentence_1, sentence_2, info_content_norm):
    words_1 = nltk.word_tokenize(sentence_1)
    words_2 = nltk.word_tokenize(sentence_2)
    joint_words = set(words_1).union(set(words_2))  # returns the set of unique words
    vec_1 = semantic_vector(words_1, joint_words, info_content_norm)
    vec_2 = semantic_vector(words_2, joint_words, info_content_norm)
    if np.linalg.norm(vec_1) * np.linalg.norm(vec_2) != 0:
        return np.dot(vec_1, vec_2.T) / (np.linalg.norm(vec_1) * np.linalg.norm(vec_2))  # cosine similarity
    else:
        return np.dot(vec_1, vec_2.T) / 0.1  # cosine similarity


######################### word order similarity ##########################

def word_order_vector(words, joint_words, windex):
    wovec = np.zeros(len(joint_words))  # give a array of zeros of the length of the joint word array
    i = 0
    wordset = set(words)
    for joint_word in joint_words:
        if joint_word in wordset:
            wovec[i] = windex[joint_word]  # if the word is there in the sentence record that index value
        else:
            sim_word, max_sim = most_similar_word(joint_word,
                                                  wordset)  # find the most similar word to a given word from the wordset
            if max_sim > ETA:
                wovec[i] = windex[sim_word]
            else:
                wovec[i] = 0
        i = i + 1
    return wovec


def word_order_similarity(sentence_1, sentence_2):  # breaks sentnse in to token arrays

    words_1 = nltk.word_tokenize(sentence_1)
    words_2 = nltk.word_tokenize(sentence_2)
    joint_words = list(set(words_1).union(set(words_2)))  # words comman to both sentences in one array
    windex = {x[1]: x[0] for x in enumerate(joint_words)}  # number the words in the array
    r1 = word_order_vector(words_1, joint_words, windex)
    r2 = word_order_vector(words_2, joint_words, windex)
    if np.linalg.norm(r1 + r2) != 0:
        return 1.0 - (np.linalg.norm(r1 - r2) / np.linalg.norm(
            r1 + r2))  # https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.linalg.norm.html  returns norm of a matrix
    else:
        return 1.0 - (np.linalg.norm(r1 - r2) / 0.1)

######################### overall similarity ##########################

def similarity(sentence_1, sentence_2, info_content_norm):
    return DELTA * semantic_similarity(sentence_1, sentence_2, info_content_norm) + \
           (1.0 - DELTA) * word_order_similarity(sentence_1, sentence_2)

##################################################################################PDF MINER##############################################################33

def remove_whitespace_entities(doc):
    doc.ents = [e for e in doc.ents if not e.text.isspace()]
    return doc

#@timeout(90.0)
def extract_text(files=[], outfile='-',
            _py2_no_more_posargs=None,  # Bloody Python2 needs a shim
            no_laparams=False, all_texts=None, detect_vertical=None, # LAParams
            word_margin=None, char_margin=None, line_margin=None, boxes_flow=None, # LAParams
            output_type='text', codec='utf-8', strip_control=False,
            maxpages=0, page_numbers=None, password="", scale=1.0, rotation=0,
            layoutmode='normal', output_dir=None, debug=False,
            disable_caching=False, **other):
    print("start extarct")
    if _py2_no_more_posargs is not None:
        raise ValueError("Too many positional arguments passed.")
    if not files:
        raise ValueError("Must provide files to work upon!")

    if not no_laparams:
        laparams = pdfminer.layout.LAParams()
        for param in ("all_texts", "detect_vertical", "word_margin", "char_margin", "line_margin", "boxes_flow"):
            paramv = locals().get(param, None)
            if paramv is not None:
                setattr(laparams, param, paramv)
    else:
        laparams = None

    imagewriter = None
    if output_dir:
        imagewriter = ImageWriter(output_dir)

    if output_type == "text" and outfile != "-":
        for override, alttype in (  (".htm", "html"),
                                    (".html", "html"),
                                    (".xml", "xml"),
                                    (".tag", "tag") ):
            if outfile.endswith(override):
                output_type = alttype

    if outfile == "-":
        outfp = sys.stdout
        if outfp.encoding is not None:
            codec = 'utf-8'
    else:
        outfp = open(outfile, "wb")

    urlretrieve(files, "document.pdf")
    #response = urllib.request.urlopen(files)
    #file = open("document.pdf", 'wb')
    #file.write(response.read())
    #file.close()
    with open("document.pdf", "rb") as fpp:
       pdfminer.high_level.extract_text_to_fp( fpp, **locals())

    outfp.close()
    print("Done extracting text")



def maketheparser():
    parser = argparse.ArgumentParser(description=__doc__, add_help=True)
    parser.add_argument("files", type=str, default=None, nargs="+", help="File to process.")
    parser.add_argument("-d", "--debug", default=False, action="store_true", help="Debug output.")
    parser.add_argument("-p", "--pagenos", type=str, help="Comma-separated list of page numbers to parse. Included for legacy applications, use --page-numbers for more idiomatic argument entry.")
    parser.add_argument("--page-numbers", type=int, default=None, nargs="+", help="Alternative to --pagenos with space-separated numbers; supercedes --pagenos where it is used.")
    parser.add_argument("-m", "--maxpages", type=int, default=0, help="Maximum pages to parse")
    parser.add_argument("-P", "--password", type=str, default="", help="Decryption password for PDF")
    parser.add_argument("-o", "--outfile", type=str, default="-", help="Output file (default \"-\" is stdout)")
    parser.add_argument("-oo", "--outfile-edited", type=str, default="-", help="Output file (default \"-\" is stdout)")
    parser.add_argument("-mj", "--module-json", type=str, default="-", help="Output file (default \"-\" is stdout)")
    parser.add_argument("-oj", "--output-json", type=str, default="-", help="Output file (default \"-\" is stdout)")
    parser.add_argument("-od", "--output-directory", type=str, default="-", help="Output file (default \"-\" is stdout)")
    parser.add_argument("-t", "--output_type", type=str, default="text", help="Output type: text|html|xml|tag (default is text)")
    parser.add_argument("-c", "--codec", type=str, default="utf-8", help="Text encoding")
    parser.add_argument("-s", "--scale", type=float, default=1.0, help="Scale")
    parser.add_argument("-A", "--all-texts", default=None, action="store_true", help="LAParams all texts")
    parser.add_argument("-V", "--detect-vertical", default=None, action="store_true", help="LAParams detect vertical")
    parser.add_argument("-W", "--word-margin", type=float, default=None, help="LAParams word margin")
    parser.add_argument("-M", "--char-margin", type=float, default=None, help="LAParams char margin")
    parser.add_argument("-L", "--line-margin", type=float, default=None, help="LAParams line margin")
    parser.add_argument("-F", "--boxes-flow", type=float, default=None, help="LAParams boxes flow")
    parser.add_argument("-Y", "--layoutmode", default="normal", type=str, help="HTML Layout Mode")
    parser.add_argument("-n", "--no-laparams", default=False, action="store_true", help="Pass None as LAParams")
    parser.add_argument("-R", "--rotation", default=0, type=int, help="Rotation")
    parser.add_argument("-O", "--output-dir", default=None, help="Output directory for images")
    parser.add_argument("-C", "--disable-caching", default=False, action="store_true", help="Disable caching")
    parser.add_argument("-S", "--strip-control", default=False, action="store_true", help="Strip control in XML mode")
    return parser


if __name__ == '__main__':
    #app.run(debug=True)
    socketio.run(app)
	
#@copyrights of Aeshana Shalindra Udadeniya UoM FIT