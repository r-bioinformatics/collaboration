import unittest
from pycgds import CGDS


class TestFormats(unittest.TestCase):

    def test_case_format(self):
        header = ["cancer_study_id", "name", "description"]
        result = CGDS().get_cancer_studies()
        self.assertTrue(result.columns.all(header))

    def test_type_format(self):
        header = ["type_of_cancer_id", "name"]
        result = CGDS().get_cancer_types()
        self.assertTrue(result.columns.all(header))

    def test_get_genetic_profiles(self):
        header = ["genetic_profile_id", "genetic_profile_name", "genetic_profile_description", "cancer_study_id",
                  "genetic_alteration_type", "show_profile_in_analysis_tab"]
        result = CGDS().get_genetic_profiles("gbm_tcga")
        self.assertTrue(result.columns.all(header))

    def test_get_case_list(self):
        header = ["case_list_id", "case_list_name", "case_list_description", "cancer_study_id", "case_ids"]
        result = CGDS().get_case_lists("gbm_tcga")
        self.assertTrue(result.columns.all(header))

    def test_get_rna(self):
        result = CGDS().get_profile_data(case_set_id="gbm_tcga_all", genetic_profile_id="gbm_tcga_mrna",
                                         genes=["EGFR", "ERBB2"])
        self.assertTrue(result.columns.any(["GENE_ID", "COMMON"]))


if __name__ == "__main__":
    unittest.main()
