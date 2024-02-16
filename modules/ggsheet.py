import urequests as requests
import ujson
import os


import requests



url = "https://script.google.com/macros/s/AKfycbzyOpcjX0IqOkGYb5pbdyIyEOa73FNq8i2WugWkKrT2MS8CAzR76mRjVZWhXSKwqDhL-A/exec"
url += "?sheet_id=1JerGKakchlnlLxgWr2YC_4dBg3A3YPDc_Ai6lrptuJE&sheet_name=Sheet1&mode=updateCell&row=&column=3&data=Hello"

try:
    requests.get(url, stream=True) 

    # Continue with the rest of your code

except Exception as e:
    print("Error during GET request:", repr(e))

"""
url = "https://script.google.com/macros/s/AKfycbzyOpcjX0IqOkGYb5pbdyIyEOa73FNq8i2WugWkKrT2MS8CAzR76mRjVZWhXSKwqDhL-A/exec"
url += "?sheet_id=1JerGKakchlnlLxgWr2YC_4dBg3A3YPDc_Ai6lrptuJE&sheet_name=Sheet1&mode=updateCell&row=3&column=3&data=Hello"

try:
    print(url)
    response = requests.get("https://httpbin.org/get?param1=value1&param2=value2")
    response.status_code
    response.close()
    print(response.status_code)
except Exception as e:
    print("Error during GET request:", repr(e))
"""

class MicroGoogleSheet():    
    
    def __init__(self):       
        googleSheetURL = "https://docs.google.com/spreadsheets/d/1JerGKakchlnlLxgWr2YC_4dBg3A3YPDc_Ai6lrptuJE/edit#gid=0"
        sheet_name = "Sheet1"
        deploymentID = "AKfycbzyOpcjX0IqOkGYb5pbdyIyEOa73FNq8i2WugWkKrT2MS8CAzR76mRjVZWhXSKwqDhL-A"        
        self.sheetID = self.get_googleSheetID(googleSheetURL)
        self.sheetName = str(sheet_name)
        self.deploymentID = str(deploymentID)
       
    def get_googleSheetID(self, url):
        start_index = url.find('/d/') + 3
        end_index = url.find('/edit')
        sheet_id = url[start_index:end_index]
        return sheet_id

    def encoding_url(self, data):
        encoded_text = ujson.dumps(data)[1:-1]
        encoded_text = ujson.loads('"' + encoded_text + '"')
        encoded_text = encoded_text.replace('\\u', '%u')
        encoded_text = encoded_text.replace('"', '')
        encoded_text = encoded_text.replace('+', ' ')
        encoded_text = encoded_text.encode('utf-8')
        encoded_text = ''.join(['%' + ('%02X' % b) for b in encoded_text])
        return encoded_text

    def set_DeploymentID(self, deployment_id):
        self.deploymentID = str(deployment_id)

    def set_SheetName(self, sheetName):
        self.sheetName = str(sheetName)

    def updateCell(self, row=1, column=1, data=""):
        try:
            sheet_name = self.encoding_url(self.sheetName)
            mode = "updateCell"
            url = "https://script.google.com/macros/s/{}/exec?sheet_id={}&sheet_name={}&mode={}&row={}&column={}&data={}".format(
                self.deploymentID, self.sheetID, sheet_name, mode, row, column, self.encoding_url(
                    str(data))
            )
            print(url)
            response = requests.get(url)
            response.close()
            return response.status_code
        except Exception as e:
            print("Error during GET request:", repr(e))

    def updateRow(self, row=1, data=[]):
        sheet_name = self.encoding_url(self.sheetName)
        mode = "updateRow"
        url = "https://script.google.com/macros/s/{}/exec?sheet_id={}&sheet_name={}&mode={}&row={}".format(
            self.deploymentID, self.sheetID, sheet_name, mode, row)
        for i in range(len(data)):
            url += "&data{}={}".format(i, self.encoding_url(str(data[i])))
        response = requests.get(url)
        response.close()
        return response.status_code

    def appendRow(self, row=0, data=[]):
        sheet_name = self.encoding_url(self.sheetName)
        mode = "appendRow"
        url = "https://script.google.com/macros/s/{}/exec?sheet_id={}&sheet_name={}&mode={}&row={}".format(
            self.deploymentID, self.sheetID, sheet_name, mode, row)
        for i in range(len(data)):
            url += "&data{}={}".format(i, self.encoding_url(str(data[i])))
        response = requests.get(url)
        response.close()
        return response.status_code

    def appendColumn(self, column=1, data=[]):
        sheet_name = self.encoding_url(self.sheetName)
        mode = "appendColumn"
        url = "https://script.google.com/macros/s/{}/exec?sheet_id={}&sheet_name={}&mode={}&column={}".format(
            self.deploymentID, self.sheetID, sheet_name, mode, column)
        for i in range(len(data)):
            url += "&data{}={}".format(i, self.encoding_url(str(data[i])))
        response = requests.get(url)
        response.close()
        return response.status_code

    def updateColumn(self, column=1, data=[]):
        sheet_name = self.encoding_url(self.sheetName)
        mode = "updateColumn"
        url = "https://script.google.com/macros/s/{}/exec?sheet_id={}&sheet_name={}&mode={}&column={}".format(
            self.deploymentID, self.sheetID, sheet_name, mode, column)
        for i in range(len(data)):
            url += "&data{}={}".format(i, self.encoding_url(str(data[i])))
        response = requests.get(url)
        response.close()
        return response.status_code

    def getCell(self, row=1, column=1):
        sheet_name = self.encoding_url(self.sheetName)
        mode = "getCell"
        url = "https://script.google.com/macros/s/{}/exec?sheet_id={}&sheet_name={}&mode={}&row={}&column={}".format(
            self.deploymentID, self.sheetID, sheet_name, mode, row, column
        )
        response = requests.get(url)
        responseCode = response.status_code

        if responseCode > 0:
            html_code = response.text
            start_index = html_code.find('start')
            end_index = html_code.find('finish')
            script_content = html_code[start_index:end_index]
            return script_content[29:-24]
        else:
            return "Error Code:{}".format(responseCode)

    def getRow(self, row=1):
        sheet_name = self.encoding_url(self.sheetName)
        mode = "getRow"
        url = "https://script.google.com/macros/s/{}/exec?sheet_id={}&sheet_name={}&mode={}&row={}".format(
            self.deploymentID, self.sheetID, sheet_name, mode, row)
        response = requests.get(url)
        responseCode = response.status_code
        if responseCode > 0:
            html_code = response.text
            start_index = html_code.find('start')
            end_index = html_code.find('finish')
            script_content = html_code[start_index:end_index]
            return script_content[29:-24]
        else:
            return "Error Code:{}".format(responseCode)

    def getColumn(self, column=1):
        sheet_name = self.encoding_url(self.sheetName)
        mode = "getColumn"
        url = "https://script.google.com/macros/s/{}/exec?sheet_id={}&sheet_name={}&mode={}&column={}".format(
            self.deploymentID, self.sheetID, sheet_name, mode, column)
        response = requests.get(url)
        responseCode = response.status_code
        if responseCode > 0:
            html_code = response.text
            start_index = html_code.find('start')
            end_index = html_code.find('finish')
            script_content = html_code[start_index:end_index]
            return script_content[29:-24]
        else:
            return "Error Code:{}".format(responseCode)
    
    def deleteCell(self,row=1,column=1):
        sheet_name = self.encoding_url(self.sheetName)
        mode = "deleteCell"
        url = "https://script.google.com/macros/s/{}/exec?sheet_id={}&sheet_name={}&mode={}&row={}&column={}".format(
            self.deploymentID, self.sheetID, sheet_name, mode, row, column)
        response = requests.get(url)
        response.close()
        return response.status_code
    
    def deleteRow(self,row=1):
        sheet_name = self.encoding_url(self.sheetName)
        mode = "deleteRow"
        url = "https://script.google.com/macros/s/{}/exec?sheet_id={}&sheet_name={}&mode={}&row={}".format(
            self.deploymentID, self.sheetID, sheet_name, mode, row)
        response = requests.get(url)
        response.close()
        return response.status_code
    
    def deleteColumn(self,column=1):
        sheet_name = self.encoding_url(self.sheetName)
        mode = "deleteColumn"
        url = "https://script.google.com/macros/s/{}/exec?sheet_id={}&sheet_name={}&mode={}&column={}".format(
            self.deploymentID, self.sheetID, sheet_name, mode, column)
        response = requests.get(url)
        response.close()
        return response.status_code