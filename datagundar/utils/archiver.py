import hashlib
import json

def postArchiveData(data, data_tag, archive_path):
    json_data=json.dumps(data)
    digest_data=hashlib.sha256(json_data.encode(encoding='UTF-8',errors='strict')).hexdigest()

    archive_data={
        "data": json_data,
        "digest": digest_data
    }

    with open(archive_path+data_tag+'.dga', 'w') as f:
        json.dump(archive_data, f, indent=2)

def getArchiveData(data_tag, archive_path):
    with open(archive_path+data_tag+'.dga') as json_data:
        return json.load(json_data)