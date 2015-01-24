"""
Testing module for the process module
"""
from ..process import _extract_amount, _extract_company_roots

from nltk import sent_tokenize


class TestContractsJson(object):
    """
    Check that the final single-entry contracts json is as expected when given
    a list of contract blobs contained in date -> <departments> -> <blobs>
    hierarchy.
    """
    def setUp(self):
        # load some from file with known successful results
        self.blob_lines = ["Delbert P.Q. Imfeld, Co., got a\
                            bunch of money to do something",
                           "That amount was $250,034,000.",
                           "But then it took a while for them and it was more \
                            difficult than expected, so we're giving them \
                            another $1,020,000"]

        self.blob = ' '.join(self.blob_lines)

        self.multicomp_blob = u'Booz Allen Hamilton, Inc., McLean, Virginia (W911S0-15-D-0001); Cubic Applications, Inc., San Diego, California (W911S0-15-D-0002); and Janus Research Group, Appling, Georgia (W911S0-15-D-0003), were awarded a $240,000,000 order-dependent contract for mission support services to the Army Capabilities Integration Center. Funding and work location will be determined with each order, with an estimated completion date of Dec. 18, 2019. Bids were solicited via the Internet, with seven received. Army Contracting Command, Fort Eustis, Fort Eustis, Virginia, is the contracting activity.'

        self.multcomp_blob_lines = sent_tokenize(self.multicomp_blob)

    def test_extract_amount(self):
        "Correctly compute the total dollar amount from an announcement"
        assert _extract_amount(self.blob_lines) == 250034000 + 1020000

    def test_extract_company_roots(self):
        "Extract company roots pre-build of normalized list"
        generated = _extract_company_roots(self.blob)
        expected = [["Delbert ", "P.Q. ", "Imfeld"]]
        assert generated == expected, "%s, %s" % (generated, expected)

        generated = _extract_company_roots(self.multicomp_blob)
        expected = [["Booz ", "Allen ", "Hamilton"],
                    ["Cubic ", "Applications"],
                    ["Janus ", "Research ", "Group"]]
        assert generated == expected, "%s, %s" % (generated, expected)

    def test_normalize_companies(self):
        "Given a list of companies, properly normalize the company names"
        assert False

    def test_build_json(self):
        "The entire, compnay-normalized JSON is successfully built"
        assert False

    def test_build_csv(self):
        "The entire, compnay-normalized CSV is successfully built"
        assert False
