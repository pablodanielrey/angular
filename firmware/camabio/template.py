# -*- coding: utf-8 -*-
import codecs, logging

class Templates:

    def __generate_template(self,userId,number,template):
        id = str(uuid.uuid4())
        mapping = {
            'number':number,
            'id': id
        }
        tmpl = {
            'id': id,
            'template':template,
            'algorithm':'Camabio-SM20',
            'userId':userId
        }
        return (mapping,tmpl)
