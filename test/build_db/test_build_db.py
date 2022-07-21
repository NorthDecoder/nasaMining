# test_build_db.py

'''
   End to end test that writes some bogus json data to a
   MongoDB collection

   Prerequisites
    1) MongoDB database to be available.
    2) MongoDB authentication parameters in .env file
    3) test/data/list_10_documents.json file
    4) relative path to the script under test is
       ../../mongoWork/buildDB.py

    TODO:
    At the end of the test the bogus test collection is
    removed using the force delete feature of buildDB.
'''

import json
import unittest
import os
from pathlib import Path
import subprocess

#

relative_path_to_sut = "../../mongoWork/buildDB.py"

parent_directory = str( Path(__file__).parent )
absolute_path_object_to_sut= Path( os.path.join( parent_directory, relative_path_to_sut ) )
absolute_path_to_sut = str( absolute_path_object_to_sut.resolve() )

print("absolute_path_to_sut: ", absolute_path_to_sut)


class TestAugmentedHelp( unittest.TestCase ):

    def test_augmented_help(self):
        augmented_help_output = subprocess.run( [absolute_path_object_to_sut,
                                                "--augmented_help"],
                                                capture_output=True )

        self.assertEqual( type(augmented_help_output).__name__,
                          "CompletedProcess",
                          "Subprocess run buildDB.py should return a completed process" )

        self.assertTrue( b"Help on function buildDB_augmented_help in module __main__"
                         in augmented_help_output.stdout,
                         "Expecting beginning help string to match" )



class TestSaveJsonToDB( unittest.TestCase ):

    def test_loaded_list(self):


        built_list_10 = subprocess.run( [absolute_path_to_sut,
                                 "--inpath", "../test/data/list_10_documents.json",
                                 "--environment", "production",
                                 "--keyname", "dataset",
                                 "--collection_name",  "list_10",
                                 "--force_delete","yes"],
                                 capture_output=True  )

        # not sure why the result is in stderr, just rolling with it for now
        self.assertTrue( b"'list_10' now contains 10 documents"
                         in built_list_10.stderr,
                         "Expecting part of the successful load message" )

    #

    def test_loaded_dict(self):


        built_dict_10 = subprocess.run( [absolute_path_to_sut,
                                 "--inpath", "../test/data/dict_10_documents.json",
                                 "--environment", "production",
                                 "--keyname", "dataset",
                                 "--collection_name",  "list_10",
                                 "--force_delete","yes"],
                                 capture_output=True  )

        # not sure why the result is in stderr, just rolling with it for now
        self.assertTrue( b"'list_10' now contains 10 documents"
                         in built_dict_10.stderr,
                         "Expecting part of the successful load message" )












#
if __name__ == '__main__':
    unittest.main()

