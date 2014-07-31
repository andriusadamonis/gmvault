'''
    Gmvault: a tool to backup and restore your gmail account.
    Copyright (C) <2011-2013>  <guillaume Aubert (guillaume dot aubert at gmail do com)>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import unittest
import base64
import shutil
import os

import gmv.gmvault_export as gmvault_export
import gmv.gmvault_utils as gmvault_utils


def delete_db_dir(a_db_dir):
    """
       delete the db directory
    """
    gmvault_utils.delete_all_under(a_db_dir, delete_top_dir = True)


class TestMBox(unittest.TestCase):

    def __init__(self, stuff):
        """ constructor """
        super(TestMBox, self).__init__(stuff)

        self.mbox = None
        self.db_dir = "../etc/tests/test_export"
        self.output_dir = "gmvault_export_test_dir/mbox_dir"

        
    def setUp(self): #pylint:disable-msg=C0103

        gmvault_utils.makedirs(self.output_dir)
        self.mbox = gmvault_export.MBox(self.output_dir)


    def tearDown(self):

        self.mbox = None
        #delete_db_dir(self.output_dir)


    def test_no_export(self):

        self.assertFalse(os.path.exists('%s/MBOX' % (self.output_dir)))

    def test_export_one_msg(self):
       
        message = """
Received: by 10.10.10.10 with HTTP; Fri, 11 Jan 2008 09:14:33 -0800 (PST)
Message-ID: <c77dbaf40801110914q64f55a25ua2e9fd741696158f@mail.gmail.com>
Date: Fri, 11 Jan 2008 19:14:33 +0200
From: "BC" <sender@example.com>
To: receiver@example.com
Subject: =?ISO-8859-1?Q?Subject?=
MIME-Version: 1.0
Content-Type: text/plain
Delivered-To: receiver@example.com

test

"""
        self.mbox.add(message, '', gmvault_export.GMVaultExporter.GM_SEEN)

        self.assertTrue(os.path.exists('%s/MBOX' % (self.output_dir)))
    

class MaildirMock(gmvault_export.MBox):
    """ Class for temporary saving and testing """
    #def root_is_maildir(self):
    #    return True


class TestGMVaultExporter(unittest.TestCase): #pylint:disable-msg=R0904
    """
       Current Main test class
    """

    def __init__(self, stuff):
        """ constructor """
        super(TestGMVaultExporter, self).__init__(stuff)

        self.gexp = None
        self.db_dir = '../etc/tests/test_export'
        self.output_dir = 'gmvault_export_test_dir\output-dir'

        
    def setUp(self): #pylint:disable-msg=C0103
        
        gmvault_utils.makedirs(self.output_dir)
        self.maildir = MaildirMock(self.output_dir)
        self.gexp = gmvault_export.GMVaultExporter(self.db_dir, self.maildir)
        # labels = None, froms = None, xfroms = None, ccs = None, xccs = None):

        # shutil.copyfile('../etc/tests/test_few_days_syncer/2384403887202624608.eml.gz','%s/2384403887202624608.eml.gz' % (storage_dir))
        # shutil.copyfile('../etc/tests/test_few_days_syncer/2384403887202624608.meta','%s/2384403887202624608.meta' % (storage_dir))
        

    def tearDown(self):

        self.gexp = None
        self.maildir = None
        #delete_db_dir(self.output_dir)
        

    def ztest_export_default(self):
        """
           Export all messages with default settings
        """
        self.gexp.export()
        self.assertTrue(os.path.exists('%s/MBOX' % (self.output_dir)))


    def ztest_retrieve_gmail_ids(self):
        """
           Get all uid before Sep 2004
           Retrieve all GMAIL IDs 
        """
        gimap = imap_utils.GIMAPFetcher('imap.gmail.com', 993, self.login, self.passwd)
        
        gimap.connect()
       
        criteria = ['Before 1-Oct-2004']
        #criteria = ['ALL']
        ids = gimap.search(criteria)
        
        res = gimap.fetch(ids, [gimap.GMAIL_ID])
        
        self.assertEquals(res, {27362: {'X-GM-MSGID': 1147537963432096749L, 'SEQ': 14535}, 27363: {'X-GM-MSGID': 1147537994018957026L, 'SEQ': 14536}})
        
        
        

def tests():
    """
       main test function
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGMVaultExporter)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestMBox)
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([suite, suite2]))
 
if __name__ == '__main__':
    
    tests()
