import xml.etree.ElementTree as ET
from typing import Dict

class XMLScoring:
    def __init__(self, xml_file: str = 'results.xml'): # make default 'results.xml``
        self.xml_file = xml_file
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
    
    def get_test_results(self) -> Dict[str, int]:
        '''
        Parse XML and return dict with test file names as keys and 1 (pass) or 0 (fail) as values.
        All tests in a file must pass for the file to be marked as 1.

        Returns:
            dict: Maps test file names to pass (1) or fail (0) status.
        '''
        results = {}
        
        # iterate through test case elements
        for testcase in self.root.findall('.//testcase'):
            classname = testcase.get('classname', '')
            filename = classname.split('.')[0] if '.' in classname else classname
            
            # check if there is a failure child element
            has_failure = testcase.find('failure') is not None
            has_error = testcase.find('error') is not None
            test_passed = 0 if (has_failure or has_error) else 1
            
            if filename not in results:
                results[filename] = test_passed
            else: # mark as failed if any test fails
                results[filename] = results[filename] and test_passed
        
        return results

# # test funciton
# scorer = XMLScoring('results/results.xml')
# results_dict = scorer.get_test_results()
# print(results_dict)
