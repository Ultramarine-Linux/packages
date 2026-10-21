#!/usr/bin/python
# vim:set et sw=4:
#
# certdata2pem.py - splits certdata.txt into multiple files
#
# Copyright (C) 2009 Philipp Kern <pkern@debian.org>
# Copyright (C) 2013 Kai Engert <kaie@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301,
# USA.

import base64
import os.path
import re
import sys
import textwrap
import subprocess
import getopt
import asn1
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from datetime import datetime
from dateutil.parser import parse

objects = []

pemcerts = []

certdata='./certdata.txt'
pem='./cert.pem'
output='./certdata_out.txt'
trust='CKA_TRUST_CODE_SIGNING'
merge_label="Non-Mozilla Object Signing Only Certificate"
dateString='thisyear'

trust_types = {
  "CKA_TRUST_SERVER_AUTH",
  "CKA_TRUST_EMAIL_PROTECTION",
  "CKA_TRUST_CODE_SIGNING"
}

attribute_types = {
    "CKA_CLASS" : "CK_OBJECT_CLASS",
    "CKA_TOKEN" : "CK_BBOOL",
    "CKA_PRIVATE" : "CK_BBOOL",
    "CKA_MODIFIABLE" : "CK_BBOOL",
    "CKA_LABEL" : "UTF8",
    "CKA_CERTIFICATE_TYPE" : "CK_CERTIFICATE_TYPE",
    "CKA_SUBJECT" : "MULTILINE_OCTAL",
    "CKA_ID" : "UTF8",
    "CKA_CERT_SHA1_HASH" : "MULTILINE_OCTAL",
    "CKA_CERT_MD5_HASH" : "MULTILINE_OCTAL",
    "CKA_ISSUER" : "MULTILINE_OCTAL",
    "CKA_SERIAL_NUMBER" : "MULTILINE_OCTAL",
    "CKA_VALUE" : "MULTILINE_OCTAL",
    "CKA_NSS_MOZILLA_CA_POLICY" : "CK_BBOOL",
    "CKA_NSS_SERVER_DISTRUST_AFTER" : "Distrust",
    "CKA_NSS_EMAIL_DISTRUST_AFTER" : "Distrust",
    "CKA_TRUST_SERVER_AUTH" : "CK_TRUST",
    "CKA_TRUST_EMAIL_PROTECTION" : "CK_TRUST",
    "CKA_TRUST_CODE_SIGNING" : "CK_TRUST",
    "CKA_TRUST_STEP_UP_APPROVED" : "CK_BBOOL"
}

def printable_serial(obj):
  return ".".join([str(x) for x in obj['CKA_SERIAL_NUMBER']])

def getSerial(cert):
    encoder = asn1.Encoder()
    encoder.start()
    encoder.write(cert.serial_number)
    return encoder.output()

def dumpOctal(f,value):
    for i in range(len(value)) :
        if  i % 16 == 0 :
            f.write("\n")
        f.write("\\%03o"%int.from_bytes(value[i:i+1],sys.byteorder))
    f.write("\nEND\n")

# in python 3.8 this can be replaced with return byteval.hex(':',1)
def formatHex(byteval) :
    string=byteval.hex()
    string_out=""
    for i in range(0,len(string)-2,2) :
         string_out += string[i:i+2] + ':'
    string_out += string[-2:]
    return string_out

def getdate(dateString):
    print("dateString= %s"%dateString)
    if dateString.upper() == "THISYEAR":
        return datetime(datetime.today().year,12,31,11,59,59,9999)
    if dateString.upper() == "TODAY":
        return datetime.today()
    return parse(dateString, fuzzy=True);

def getTrust(objlist, serial, issuer) :
    for obj in objlist:
        if obj['CKA_CLASS'] == 'CKO_NSS_TRUST' and obj['CKA_SERIAL_NUMBER'] == serial and obj['CKA_ISSUER'] == issuer:
            return obj
    return None

def isDistrusted(obj) :
    if (obj == None):
        return False
    return obj['CKA_TRUST_SERVER_AUTH'] == 'CKT_NSS_NOT_TRUSTED' and obj['CKA_TRUST_EMAIL_PROTECTION'] == 'CKT_NSS_NOT_TRUSTED' and obj['CKA_TRUST_CODE_SIGNING'] == 'CKT_NSS_NOT_TRUSTED'


def stripQuotes(label) :
    if label[:1] == "\"" :
        label=label[1:]
    if label[-1] == "\"" :
        label = label[:-1]
    return label

# another object of the same class has the same label
def labelExists(objlist, obj) :
    for iobj in objlist:
        if obj['CKA_CLASS'] == iobj['CKA_CLASS'] and obj['CKA_LABEL'] == iobj['CKA_LABEL']:
            return True
    return False

# add an object, make sure that label is unique
def addObj(objlist, newObj, specialLabel, drop) :
    label = stripQuotes(newObj['CKA_LABEL'])
    count=1
    if specialLabel != None :
        count=0
        label=label+' '+specialLabel
    # make sure the label is unique
    while labelExists(objlist, newObj) :
        if drop :
            return 'DROPPED'
        if count != 0 :
            newObj['CKA_LABEL'] = "\"%s %d\""%(label,count)
        else :
            newObj['CKA_LABEL'] = "\"%s\""%label
        count=count+1
    objlist.append(obj)
    return stripQuotes(newObj['CKA_LABEL'])

try:
    opts, args = getopt.getopt(sys.argv[1:],"c:o:p:t:l:x:",)
except getopt.GetoptError as err:
    print(err)
    print(sys.argv[0] + ' [-c certdata] [-p pem] [-o certdata_target] [-t trustvalue] [-l merge_label]')
    print('-c certdata         certdata file to merge to (default="'+certdata+'")');
    print('-p pem              pem file with CAs to merge from (default="'+pem+'")');
    print('-o certdata_target  resulting output file (default="'+output+'")');
    print('-t trustvalue       what these CAs are trusted for (default="'+trust+'")');
    print('-l merge_label      what label CAs that aren\'t in certdata (default="'+merge_label+'")');
    print('-x date             remove all certs that expire before data (default='+dateString+')');
    sys.exit(2)

for opt, arg in opts:
    if opt == '-c' :
        certdata = arg
    elif opt == '-p' :
        pem = arg
    elif opt == '-o' :
        output = arg
    elif opt == '-t' :
        trust = arg
    elif opt == '-l' :
        merge_label = arg
    elif opt == '-x' :
        dateString = arg

# parse dateString
print ("datastring=",dateString)
verifyDate = True
if dateString.upper() == "NEVER":
   verifyDate = False
else:
   date = getdate(dateString)
print ("verifyDate=",verifyDate)


# read the pem file
in_cert, certvalue = False, ""
for line in open(pem, 'r'):
    if not in_cert:
       if line.find("BEGIN CERTIFICATE") != -1:
            in_cert = True;
       continue
    # Ignore comment lines and blank lines.
    if line.startswith('#'):
        continue
    if len(line.strip()) == 0:
        continue
    if line.find("END CERTIFICATE") != -1 :
       pemcerts.append(certvalue);
       certvalue = "";
       in_cert = False;
       continue
    certvalue += line;

# read the certdata.txt file
in_data, in_multiline, in_obj = False, False, False
field, ftype, value, binval, obj = None, None, None, bytearray(), dict()
header, comment = "", ""
for line in open(certdata, 'r'):
    # Ignore the file header.
    if not in_data:
        header += line
        if line.startswith('BEGINDATA'):
            in_data = True
        continue
    # Ignore comment lines. 
    if line.startswith('#'):
        comment += line
        continue

    # Empty lines are significant if we are inside an object.
    if in_obj and len(line.strip()) == 0:
        # collect all the inline comments in this object
        obj['Comment'] += comment
        comment = ""
        addObj(objects, obj, None, False)
        obj = dict()
        in_obj = False
        continue
    if len(line.strip()) == 0:
        continue
    if in_multiline:
        if not line.startswith('END'):
            if ftype == 'MULTILINE_OCTAL':
                line = line.strip()
                for i in re.finditer(r'\\([0-3][0-7][0-7])', line):
                    integ = int(i.group(1), 8)
                    binval.extend((integ).to_bytes(1, sys.byteorder))
                obj[field] = binval
            else:
                value += line
                obj[field] = value
            continue
        in_multiline = False
        continue
    if line.startswith('CKA_CLASS'):
        in_obj = True
        obj['Comment'] = comment
        comment = ""
    line_parts = line.strip().split(' ', 2)
    if len(line_parts) > 2:
        field, ftype = line_parts[0:2]
        value = ' '.join(line_parts[2:])
    elif len(line_parts) == 2:
        field, ftype = line_parts
        value = None
    else:
        raise NotImplementedError('line_parts < 2 not supported.\n' + line)
    if ftype == 'MULTILINE_OCTAL':
        in_multiline = True
        value = ""
        binval = bytearray()
        continue
    obj[field] = value

if len(list(obj.items())) > 0:
    addObj(objects, obj, None, False)

# strip out expired certificates from certdata.txt
if verifyDate :
    for obj in objects:
        if obj['CKA_CLASS'] == 'CKO_CERTIFICATE' :
            cert = x509.load_der_x509_certificate(bytes(obj['CKA_VALUE']))
            if (cert.not_valid_after <= date) :
                trust_obj = getTrust(objects,obj['CKA_SERIAL_NUMBER'],obj['CKA_ISSUER'])
                # we don't remove distrusted expired certificates
                if  not isDistrusted(trust_obj) :
                    print("  Remove cert %s"%obj['CKA_LABEL'])
                    print("     Expires: %s"%cert.not_valid_after.strftime("%m/%d/%Y"))
                    print("     Prune time %s: "%date.strftime("%m/%d/%Y"))
                    obj['Comment'] = None;
                    if (trust_obj != None):
                        trust_obj['Comment'] = None;

# now merge the results
for certval in pemcerts:
    certder = base64.b64decode(certval)
    cert = x509.load_der_x509_certificate(certder)
    try:
        label=cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)[0].value
    except:
        try:
            label=cert.subject.get_attributes_for_oid(x509.oid.NameOID.ORGANIZATION_UNIT_NAME)[0].value
        except:
            try:
                label=cert.subject.get_attributes_for_oid(x509.oid.NameOID.ORGANIZATION_NAME)[0].value
            except:
                label="Unknown Certificate"
    if verifyDate :
        if cert.not_valid_after <= date:
            print("  Skipping code signing cert %s"%label)
            print("     Expires: %s"%cert.not_valid_after.strftime("%m/%d/%Y"))
            print("     Prune time %s: "%date.strftime("%m/%d/%Y"))
            continue
    certhashsha1 = cert.fingerprint(hashes.SHA1())
    certhashmd5 =  cert.fingerprint(hashes.MD5())
    
    
    found = False
    # see if it exists in certdata.txt
    for obj in objects:
        # we only need to check the trust objects, because
        # that is the object we would modify if it exists
        if obj['CKA_CLASS'] != 'CKO_NSS_TRUST':
            continue
        # explicitly distrusted certs don't have a hash value
        if not 'CKA_CERT_SHA1_HASH' in obj:
            continue
        if obj['CKA_CERT_SHA1_HASH'] != certhashsha1:
            continue
        obj[trust] = 'CKT_NSS_TRUSTED_DELEGATOR'
        found = True
        print('Updating "'+label+'" with code signing');
        break
    if  found :
        continue

    # check for almost duplicates, certs with the same subject and key, but
    # different values. If they exist, treat them as the same certificate
    for obj in objects:
        if obj['CKA_CLASS'] != 'CKO_CERTIFICATE':
            continue
        # do they have the same subject?
        if obj['CKA_SUBJECT'] != cert.subject.public_bytes():
            continue
        # do they have the same public key?
        cert2 = x509.load_der_x509_certificate(bytes(obj['CKA_VALUE']))
        if cert2.public_key().public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo) != cert.public_key().public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo) :
            continue
        #found now update trust record
        trust_obj = getTrust(objects,obj['CKA_SERIAL_NUMBER'],obj['CKA_ISSUER'])
        if trust_obj is None :
            print('Couldn\'t find trust object for "'+obj['CKA_LABEL']);
            exit
        trust_obj[trust] = 'CKT_NSS_TRUSTED_DELEGATOR'
        found = True
        print('Updating sister certificate "'+obj['CKA_LABEL']+'" with code signing based on Microsoft "'+label+'"');
        break
        if found :
            break
    if  found :
        continue
    # append this certificate
    obj=dict()
    time='%a %b %d %H:%M:%S %Y'
    comment  = '# ' + merge_label + '\n# %s "'+label+'"\n'
    comment +=  '# Issuer: ' + cert.issuer.rfc4514_string() + '\n'
    comment +=  '# Serial Number:'
    sn=cert.serial_number
    if sn < 0x100000:
        comment +=  ' %d (0x%x)\n'%(sn,sn)
    else:
        comment +=  formatHex(sn.to_bytes((sn.bit_length()+7)//8,"big")) + '\n'
    comment +=  '# Subject: ' + cert.subject.rfc4514_string() + '\n'
    comment +=  '# Not Valid Before: ' + cert.not_valid_before.strftime(time) + '\n'
    comment +=  '# Not Valid After: ' + cert.not_valid_after.strftime(time) + '\n'
    comment +=  '# Fingerprint (MD5): ' + formatHex(certhashmd5) + '\n'
    comment +=  '# Fingerprint (SHA1): ' + formatHex(certhashsha1) + '\n'
    obj['Comment']= comment%"Certificate"
    obj['CKA_CLASS'] = 'CKO_CERTIFICATE'
    obj['CKA_TOKEN'] = 'CK_TRUE'
    obj['CKA_PRIVATE'] = 'CK_FALSE'
    obj['CKA_MODIFIABLE'] = 'CK_FALSE'
    obj['CKA_LABEL'] = '"' + label + '"'
    obj['CKA_CERTIFICATE_TYPE'] = 'CKC_X_509'
    obj['CKA_SUBJECT'] = cert.subject.public_bytes()
    obj['CKA_ID'] = '"0"'
    obj['CKA_ISSUER'] = cert.issuer.public_bytes()
    obj['CKA_SERIAL_NUMBER'] = getSerial(cert)
    obj['CKA_VALUE'] = certder
    obj['CKA_NSS_MOZILLA_CA_POLICY'] = 'CK_FALSE'
    obj['CKA_NSS_SERVER_DISTRUST_AFTER'] = 'CK_FALSE'
    obj['CKA_NSS_EMAIL_DISTRUST_AFTER'] = 'CK_FALSE'
    label = addObj(objects, obj, 'CodeSigning', True)
    if label == 'DROPPED' :
        continue

    # append the trust values
    obj=dict()
    obj['Comment']= comment%"Trust for"
    obj['CKA_CLASS'] = 'CKO_NSS_TRUST'
    obj['CKA_TOKEN'] = 'CK_TRUE'
    obj['CKA_PRIVATE'] = 'CK_FALSE'
    obj['CKA_MODIFIABLE'] = 'CK_FALSE'
    obj['CKA_LABEL'] = '"' + label + '"'
    obj['CKA_CERT_SHA1_HASH'] = certhashsha1
    obj['CKA_CERT_MD5_HASH'] = certhashmd5
    obj['CKA_ISSUER'] = cert.issuer.public_bytes()
    obj['CKA_SERIAL_NUMBER'] = getSerial(cert)
    for t in list(trust_types):
       if t == trust:
          obj[t] = 'CKT_NSS_TRUSTED_DELEGATOR'
       else:
          obj[t] = 'CKT_NSS_MUST_VERIFY_TRUST'
    obj['CKA_TRUST_STEP_UP_APPROVED'] = 'CK_FALSE'
    label = addObj(objects, obj, 'CodeSigning', True)
    print('Adding code signing cert "'+label+'"');

# now dump the results
f = open(output, 'w')
f.write(header)
for obj in objects:
    if 'Comment' in obj:
        # if comment is None, we've deleted the entry above
        if obj['Comment'] == None:
            continue
        f.write(obj['Comment'])
    else:
        print("Object with no comment!!")
        print(obj)
    for field in list(attribute_types.keys()):
        if not field in obj:
            continue
        ftype = attribute_types[field];
        if ftype == 'Distrust':
            if obj[field] == 'CK_FALSE':
                ftype = 'CK_BBOOL'
            else:
                ftype = 'MULTILINE_OCTAL'
        f.write("%s %s"%(field,ftype));
        if ftype == 'MULTILINE_OCTAL':
           dumpOctal(f,obj[field])
        else:
           f.write(" %s\n"%obj[field])
    f.write("\n")
f.close
