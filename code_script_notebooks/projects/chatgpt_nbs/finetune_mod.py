"""This file will contain the functions that is used for fine tuning"""
import openai, requests,json

def finetune_get(ftId,api_key):
    header = {'Content-Type':'application/json',
              'Authorization':f'Bearer {api_key}'}
    resp = requests.request(method='GET',
                url=f'https://api.openai.com/v1/fine-tunes/{ftId}',
                           headers=header,timeout=40)
    print(resp.json())
    
def finetune_event(ftId,api_key):
    header = {'Content-Type':'application/json',
              'Authorization':f'Bearer {api_key}'}
    resp = requests.request(method='GET',
                url=f'https://api.openai.com/v1/fine-tunes/{ftId}/events',
                           headers=header,timeout=40)
    print(resp.json())
    
def finetune_model(fileId,api_key,suffix,model='davinci'):
    header = {'Content-Type':'application/json',
              'Authorization':f'Bearer {api_key}'}
    payload = {'training_file':fileId,'model':model,'suffix':suffix}
    resp = requests.request(method='POST',
                            url='https://api.openai.com/v1/fine-tunes',
                           headers=header,
                           json=payload,timeout=40)
    print(resp.json())
    
    
def file_upload(filename, purpose='fine-tune'):
    resp = openai.File.create(purpose=purpose,file=open(file=filename,
                                                        mode='rb'))
    #print(resp)
    return resp

def file_list():
    #print(openai.File.list())
    return openai.File.list()
