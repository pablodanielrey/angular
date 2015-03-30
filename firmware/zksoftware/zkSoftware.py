# -*- coding: utf-8 -*-

import http.client
import re, logging
import xmltodict
import datetime



class ZkSoftwareException(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __init__(self,msg):
        Exception.__init__(self,msg)



class ZkSoftware:


    def __init__(self,host,port):
        self.host = host
        self.port = port


    """
        envía el mensaje y recibe una respuesta. parsea la respuesta a dictionary para poder procesarla despues
    """
    def _sendAndReceive(self,xml):

        logging.debug(xml)

        conn = http.client.HTTPConnection(self.host,self.port)
        conn.request("POST", "/iWsService",body=xml,headers={"Content-type":"text/xml","SOAPAction":"uri:zksoftware"})
        r1 = conn.getresponse()

        logging.debug(r1)

        if r1.status != 200:
            raise ZkSoftwareException(r1.reason)

        #print(r1.status, r1.reason)
        #print(r1.read().decode('iso-8859-1'))

        strresponse = r1.read().decode('iso-8859-1')
        logging.debug(strresponse)

        response = xmltodict.parse(strresponse)
        return response




    """
    <GetUserInfo>
        <ArgComKey xsi:type="xsd:integer”>ComKey</ArgComKey>
        <Arg>
            <PIN xsi:type="xsd:integer”>Job Number</PIN>
        </Arg>
    </GetUserInfo>

    <GetAllUserInfo>
        <ArgComKey xsi:type="xsd:integer”>ComKey</ArgComKey>
    </GetAllUserInfo>

    <GetUserInfoResponse>
        <Row>
            <PIN>XXXXX</PIN>
            <Name>XXXX</Name>
            <Password>XXX</Password>
            <Group>X</ Group>
            <Privilege>X</ Privilege>
            <Card>XXXX </Card>
            <PIN2>XXXX </PIN2>
            <TZ1>XXX </TZ1>
            <TZ2>XXX </TZ2>
            <TZ3>XXX </TZ3>
        </Row>
    </GetUserInfoResponse>

    <GetAllUserInfoResponse>
        <Row>
            <PIN>XXXXX</PIN>
            <Name>XXXX</Name>
            <Password>XXX</Password>
            < Group>X</ Group>
            < Privilege>X</ Privilege>
            <Card>XXXX </Card>
            <PIN2>XXXX </PIN2>
            <TZ1>XXX </TZ1>
            <TZ2>XXX </TZ2>
            <TZ3>XXX </TZ3>
        </Row>
    </GetAllUserInfoResponse>
    """
    def getUserInfo(self,pin=None):

        if pin is None:
            method = "<GetAllUserInfo><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey></GetAllUserInfo>"
            response = self._sendAndReceive(method)
            return response['GetAllUserInfoResponse']['Row']

        else:
            method = "<GetUserInfo><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">{}</PIN></Arg></GetUserInfo>"
            methodWithParams = method.format(pin)
            response = self._sendAndReceive(methodWithParams)
            return response['GetUserInfoResponse']['Row']




    """
    <GetUserTemplate>
        <ArgComKey xsi:type="xsd:integer”>ComKey</ArgComKey>
        <Arg>
            <PIN xsi:type="xsd:integer”>Job Number</PIN>
            <FingerID xsi:type="xsd:integer”>Finger Number</FingerID>
        </Arg>
    </GetUserTemplate>

    <GetUserTemplateResponse>
        <Row>
            <PIN>XXXXX</PIN>
            <FingerID>XX</FingerID>
            <Size>XXX</Size>
            <Valid>X</Valid>
            <Template>XXXXXXXXXXXXXXXX....</Template>
        </Row>
    </GetUserTemplateResponse>
    """
    def getUserTemplate(self,pin=None):
        method = "<GetUserTemplate><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">{}</PIN></Arg></GetUserTemplate>"
        response = None
        if pin is not None:
            methodWithParams = method.format(pin)
            response = self._sendAndReceive(methodWithParams)
        else:
            methodWithParams = method.format('ALL')
            response = self._sendAndReceive(methodWithParams)
        return response['GetUserTemplateResponse']['Row']



    """
    <GetDate>
        <ArgComKey xsi:type="xsd:integer”>ComKey</ArgComKey>
    </GetDate>

    <GetDateResponse>
        <Row>
            <Date>YYYY-MM-DD</Date>
            <Time>HH:MM:SS</Time>
        </Row>
    </GetDateResponse>
    """
    def getDate(self):
        method = "<GetDate><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey></GetDate>"
        response = self._sendAndReceive(method)
        date = response['GetDateResponse']['Row']
        pDate = datetime.datetime.strptime(date['Date'] + ' ' + date['Time'],'%Y-%m-%d %H:%M:%S')
        return pDate


    """
    <SetDate>
        <ArgComKey xsi:type="xsd:integer”>ComKey</ArgComKey>
        <Arg>
            <Date xsi:type="xsd:string”>YYYY-MM-DD</Date>
            <Time xsi:type="xsd:string”>HH:MM:SS</Time>
        </Arg>
    </SetDate>

    <SetDateResponse>
        <Row>
            <Result>1</Result>
        </Row>
    </SetDateResponse>
    """
    def setDate(self,date):
        method = "<SetDate><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><Date xsi:type=\"xsd:string\">{}</Date><Time xsi:type=\"xsd:string\">{}</Time></Arg></SetDate>"
        methodWithParams = method.format(date.strftime('%Y-%m-%d'),date.strftime('%H:%M:%S'))
        response = self._sendAndReceive(methodWithParams)
        result = response['SetDateResponse']['Row']['Result']
        if result != '1':
            raise ZkSoftwareException('SetDateResponse == {}'.format(result))


    """
    <GetAttLog>
        <ArgComKey xsi:type="xsd:integer”>ComKey</ArgComKey>
        <Arg>
            <PIN xsi:type="xsd:integer”>Job Number</PIN>
        </Arg>
    </GetAttLog>

    <GetAttLogResponse>
        <Row>
            <PIN>XXXXX</PIN>
            <DateTime >YYYY-MM-DD HH:MM:SS</DateTime>
            <Verified>X</Verified>
            <Status>X</Status>
            <WorkCode>XXXXX</WorkCode>
        </Row>
    </GetAttLogResponse>
    """
    def getAttLog(self,pin=None):
        method = "<GetAttLog><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><PIN xsi:type=\"xsd:integer\">{}</PIN></Arg></GetAttLog>"
        methodWithParams = method.format('ALL' if pin is None else pin)
        response = self._sendAndReceive(methodWithParams)
        if response is None:
            return []

        if 'GetAttLogResponse' in response and 'Row' not in response['GetAttLogResponse']:
            """
                el reloj no tiene logs. respuesta =
                <GetAttLogResponse>
                </GetAttLogResponse>
            """
            return []


        rows = response['GetAttLogResponse']['Row']
        logging.debug(rows)
        datedResponse = []
        for r in rows:
            d = {
                'PIN':r['PIN'],
                'DateTime':datetime.datetime.strptime(r['DateTime'],'%Y-%m-%d %H:%M:%S').replace(microsecond=0,tzinfo=None),
                'Verified':r['Verified'],
                'Status':r['Status'],
                'WorkCode':r['WorkCode']
            }
            datedResponse.append(d)
        return datedResponse



    """
     *      1 - usuarios + templates
	 * 		2 - templates
	 * 		3 - logs

    <ClearData>
        <ArgComKey xsi:type="xsd:integer”>ComKey</ArgComKey>
        <Arg>
            <Value xsi:type="xsd:integer”>3</Value>
        </Arg>
    </ClearData>

    <ClearDataResponse>
        <Row>
            <Result>1</Result>
        </Row>
    </ClearData>
    """
    def _clearData(self,param=3):
        method = "<ClearData><ArgComKey xsi:type=\"xsd:integer\">0</ArgComKey><Arg><Value xsi:type=\"xsd:integer\">{}</Value></Arg></ClearData>"
        methodWithParams = method.format(param)
        response = self._sendAndReceive(methodWithParams)
        result = response['ClearDataResponse']['Row']['Result']
        if result != '1':
            raise ZkSoftwareException('ClearDataResponse == {}'.format(result))


    def clearTemplates(self):
        self._clearData(2)

    def clearAttLogs(self):
        self._clearData(3)

    def clearUsers(self):
        self._clearData(1)
