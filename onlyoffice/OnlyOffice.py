# Gery Casiez
# 2022

import requests
import json
import time

class OnlyOffice:
    username = ''
    password = ''
    baseurl = ''
    authorization = ''
    auth = ''

    def __init__(self, baseurl: str, username: str, password: str):
        self.username = username
        self.password = password
        self.baseurl = baseurl
        self.authenticate(username, password, baseurl)

    # https://api.onlyoffice.com/portals/method/authentication/post/api/2.0/authentication
    def authenticate(self, username: str, password: str, baseurl: str):
        self.username = username
        self.password = password
        self.baseurl = baseurl
        r = requests.post('%s/api/2.0/authentication'%baseurl, \
            data={'username': username, 'password': password})
        j = json.loads(r.text)
        self.authorization = j['response']['token']
        self.auth = {'Authorization': j['response']['token']}
        return j

    def downloadFile(self, fileid, filename:str):
        r = requests.get('%s/Products/Files/HttpHandlers/filehandler.ashx?action=download&fileid=%s'%(self.baseurl, fileid), headers=self.auth)
        open(filename, "wb").write(r.content)


    # https://api.onlyoffice.com/portals/method/files/get/api/2.0/files/fileops
    def getFileops(self):
        finished = True
        r = requests.get('%s/api/2.0/files/fileops'%(self.baseurl), headers=self.auth)
        j = json.loads(r.text)     
        for item in j['response']:
            if not(item['finished']):
                finished = False
        return (finished, j)   

    # https://api.onlyoffice.com/portals/method/files/put/api/2.0/files/fileops/bulkdownload
    def download(self, fileids: list, filename:str):
        r1 = requests.put('%s/api/2.0/files/fileops/bulkdownload'%(self.baseurl), \
            data={'fileIds': fileids}, headers=self.auth) 

        # Wait for operation to finish, up to 120 s
        i = 0
        while (i < 60) and not(self.getFileops()[0]):
            time.sleep(2)
            print("Sleep %s"%i)
            i += 1

        if not(self.getFileops()[0]):
            ok = False
        else:
            r = requests.get('%s/Products/Files/HttpHandlers/filehandler.ashx?action=bulk&ext=.zip'%(self.baseurl), headers=self.auth)
            open(filename, "wb").write(r.content)
            ok = True

        return ok

    # https://api.onlyoffice.com/portals/method/files/post/api/2.0/files/%7bfolderid%7d/upload
    def upload(self, dirID: str, filename: str):
        with open(filename,'rb') as payload:
            # TODO: support other file types with content-type
            headers = {'content-type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'Content-Disposition': 'inline; filename="%s"'%filename, 'Authorization': self.authorization}
            r = requests.post('%s/api/2.0/files/%s/upload'%(self.baseurl, dirID),
                            data=payload, verify=False, headers=headers)
            j = json.loads(r.text)
            return j
    
    # https://api.onlyoffice.com/portals/method/files/get/api/2.0/files/%7bfolderid%7d
    def getFileList(self, folderId:str):
        r = requests.get('%s/api/2.0/files/%s'%(self.baseurl, folderId), headers=self.auth)
        j = json.loads(r.text)
        files = j['response']['files']
        fileList = []
        for f in files:
            fileList.append(f['id'])
        return (fileList, j)       

    # https://api.onlyoffice.com/portals/method/files/delete/api/2.0/files/file/%7bfileid%7d
    def deleteFile(self, fileId: str, deleteAfter: bool, immediately: bool):
        headers = {'deleteAfter': '%s'%deleteAfter, 'immediately': '%s'%immediately, 'Authorization': self.authorization}
        r = requests.delete('%s/api/2.0/files/file/%s'%(self.baseurl, fileId), headers=headers)
        j = json.loads(r.text)
        return j     


    # https://api.onlyoffice.com/portals/method/files/put/api/2.0/files/fileops/terminate
    def terminate(self):
        r = requests.put('%s/api/2.0/files/fileops/terminate'%self.baseurl, headers=self.auth)
        j = json.loads(r.text)
        return j

    # def __del__(self):
    #     self.terminate()