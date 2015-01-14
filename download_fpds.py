"""
Some sloppy functions to download all the files from FPDS government contract
website. There is a loop below that will download them all.
"""
import wget

DEPARTMENTS_DICT =\
    {
        '1700': "1700-DEPARTMENTOFTHENAVY",
        '2100': "2100-DEPARTMENTOFTHEARMY",
        '5700': "5700-DEPARTMENTOFTHEAIRFORCE",
        '7000': "7000-HOMELANDSECURITYDEPARTMENTOF",
        '7100': "7100-OVERSEASPRIVATEINVESTMENTCORPORATION",
        '97AS': "97AS-DEFENCELOGISTICSAGENCY",
        '97MISC': "OTHER_DOD_AGENCIES"
    }


def url(fiscal_year, dept_str=DEPARTMENTS_DICT['1700']):
    """
    modify the URL
    "https://www.fpds.gov/ddps/FY06-V1.4/1700-DEPARTMENTOFTHENAVY/1700-DEPARTMENTOFTHENAVY-DEPT-10012005TO09302006-Archive.zip"
    to be correct for the `fiscal_year` given.
    """
    assert type(fiscal_year) is str, "fiscal year must be string"
    assert int(fiscal_year) > 0 and int(fiscal_year) < 100

    prev_year = str(int("20" + fiscal_year) - 1)
    dept_str = DEPARTMENTS_DICT[k]

    return "https://www.fpds.gov/ddps/FY" + fiscal_year + \
           "-V1.4/" + dept_str + \
           "/" + dept_str + "-DEPT-" +\
           "1001" + prev_year + "TO093020" + fiscal_year + "-Archive.zip"


def new_url(fiscal_year, dept_str=DEPARTMENTS_DICT['1700']):
    """
    modify the URL
    https://www.fpds.gov/ddps/FY07-V1.4/1700-DEPARTMENTOFTHENAVY/1700-DEPARTMENTOFTHENAVY-DEPTOctober2006-Archive.zip
    to be correct for the `fiscal_year` given.
    """
    assert type(fiscal_year) is str, "fiscal year must be string"
    assert int(fiscal_year) > 0 and int(fiscal_year) < 100

    prev_year = str(int("20" + fiscal_year) - 1)
    dept_str = DEPARTMENTS_DICT[k]

    return "https://www.fpds.gov/ddps/FY" + fiscal_year + \
           "-V1.4/" + dept_str +\
           "/" + dept_str + "-DEPTOctober"\
           + prev_year + "-Archive.zip"

for k in DEPARTMENTS_DICT.keys():

    print k

    if k != "1700":
        for y in ("04", "05", "06", "07", "08", "09", "10",
                  "11", "12", "13", "14", "15"):

            print "Downloading FY 20" + y + \
                  " For department: " + DEPARTMENTS_DICT[k]

            if int(y) > 6:
                print new_url(y, k)
                wget.download(new_url(y, k))

            else:
                print url(y, k)
                wget.download(url(y, k))
