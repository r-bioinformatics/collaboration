"""
A simple client for accessing cBioPortal from python
"""
import requests
import csv
import pandas as pd
import io


class CGDS:

    def __init__(self, url="http://www.cbioportal.org", verbose=False):
        """
        CGDS

        :param url: the url to access data from, defaults to main cBioPortal
        """
        self.url = url
        self.verbose = verbose

    def process_data(self, data):
        return pd.read_csv(io.StringIO(data.text), sep="\t", comment="#")

    def api_request(self, api_request):
        url = self.url + api_request
        if self.verbose:
            print("making request to " + url)
        request = requests.get(url, stream=True)
        request.raise_for_status()
        return request

    def get_cancer_studies(self):
        result = self.api_request("/webservice.do?cmd=getCancerStudies&")
        return self.process_data(result)

    def get_cancer_types(self):
        result = self.api_request("/webservice.do?cmd=getTypesOfCancer&")
        return self.process_data(result)

    def get_genetic_profiles(self, cancer_study_id):
        result = self.api_request(f"/webservice.do?cmd=getGeneticProfiles&cancer_study_id={cancer_study_id}")
        return self.process_data(result)

    def get_case_lists(self, cancer_study_id):
        result = self.api_request(f"/webservice.do?cmd=getCaseLists&cancer_study_id={cancer_study_id}")
        return self.process_data(result)

    def get_profile_data(self, case_set_id, genetic_profile_id, genes):
        if (isinstance(genes, str)):
            genes = [genes]
        if (isinstance(genetic_profile_id, str)):
            genetic_profile_id = [genetic_profile_id]
        genetic_profile_id = ",".join(genetic_profile_id)
        genes = ",".join(genes)
        result = self.api_request(
            f"/webservice.do?cmd=getProfileData&case_set_id={case_set_id}&genetic_profile_id={genetic_profile_id}&gene_list={genes}")
        return self.process_data(result)
