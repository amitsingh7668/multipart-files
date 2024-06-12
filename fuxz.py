import time 
import sys
from pip._internal import main
from sample_questions import question_answer_pair

main(['install', '-I', '-q','thefuzz', '--target', '/tmp/',
     '--no-cache-dir', '--disable-pip-version-check'])
     
sys.path.insert(0, '/tmp/')

from thefuzz import fuzz,process


def fuzz_algorithm(prompt_question,MAX_RESULTS): 
#     list_of_questions = [
# 'Number of US clinical samples that were reported in 2023',
# 'Quarterly breakdown of unique HCPs ordering for breast cancer patients from Q1 2022 – Q2 2023',
# 'please pull the US KRAS G12C NSCLC volumes for 2021, 2022, and 2023 (year to date)?',
# 'would you be able to pull the list of IDH1+ cholangiocarcinoma patients over the last 12 months (July 22 - June 23) from the clinical database and their HCP zip code? I need to generate a heat-map output to support an alerts proposal. I would just need alert (IDH1+ cholangiocarcinoma) + practice zip code',
# 'How many unique US NSCLC NPI #s (providers) do we have in the clinical database for the last 12 months (Nov 22 – Oct 23)?Essentially can we pull how many unique NPI #s there that ordered a G360 test in the US for a NSCLC patient (regardless of biomarker) in the last 12 months)?',
# 'How many unique NSCLC practices are there with this same criteria (ordered a G360 test for a NSCLC patient in the US in the last 12 months)?',
# 'Can we please pull  How many unique Cholangiocarcioma reported practices are there within the clinical database for the last 12 months (Nov 22 – Oct 23)',
# 'Get TRF version of each valid CA Clinical G360 tests reported since June 2023',
# "count of all 'newly diagnosed' tests reported between April 2022 to March 2023. If multiple tests were ordered for the same patient during that period, only consider the first test", 'List of matches within Feb 2023 for Thyroid cancer and NSCLC tests detected with RET fusion, or thyroid medullary carcinoma tests with RET snv alteration',
# 'Quarterly breakdown of US vs non-US, newly diagnosed vs not responding to therapy CRC patients from Jan 21 to Mar 23',
# 'Lines of therapy breakdown of all NSCLC patients detected with KRAS G12C from Jan 21 to Mar 23',
# 'Quarterly distribution of newly diagnosed NSCLC patients who were detected with EGFR Exon 19 deletion between Q2 2022 to Q1 2023. If multiple tests were ordered for the same patient during that period, only consider the first test',
# 'Generate a monthly CA zip level breakdown of April 2023 of the following -: 1. number of unique physicians ordered Guardant tests, 2. number of total NSCLC KRAS G12C positive samples, 3. number of NSCLC KRAS G12C positive samples that are 1L (newly diagnosed), 4. number of NSCLC KRAS G12C positive samples that are 2L+ (not responding to therapy)',
# 'Get the number of patients who were detected with EGFR Exon 20 insertion between Q2 2022 to Q1 2023',
# 'Get the number of patients who were detected with ERBB2 Exon 19 deletion between Q2 2022 to Q1 2023',
# 'Get the number of HCP who ordered a test with RET fusion detected between Q1 2022 to Q2 2023',
# 'Get the number of HCP who ordered a test with ROS1 fusion detected between Q1 2022 to Q2 2023',
# 'List of top 10 HCPs who ordered the most BRAF fusion tests from Q2  Q4 2022'
# ]

    list_of_questions = list(question_answer_pair.keys())
    question_dict = {}
    question_dict_temp = {}
    for que in list_of_questions:
        if que != prompt_question:
                question_dict_temp[que] = int(fuzz.token_set_ratio(que,prompt_question))
    sorted_dict = sorted(question_dict_temp.items(), key=lambda x: x[1], reverse=True)
    question_dict[prompt_question] = dict(sorted_dict[:MAX_RESULTS])
    return question_dict
