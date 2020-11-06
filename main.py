import csv

office = 'President of the United States 4 Year Term (1) Position'
congress = 'District Representative in Congress 2 Year Term (1) Position'
counties = []
current_county = ''
congress_county = ''
results_dict = {}


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


with open('MI_results.csv', newline='') as csvfile:
    res_reader = csv.DictReader(csvfile, delimiter='\t')

    for row in res_reader:
        if row['OfficeDescription'] == office:
            if current_county != row['CountyName']:
                # create the dict of the county with first candidate in csv and store it in the results dict
                results_dict[row['CountyName']] = {
                    row['CandidateLastName']: row['CandidateVotes']
                }
                counties.append(current_county)  # create a list of counties
                current_county = row['CountyName']  # update the current county
                total_votes = int(row['CandidateVotes'])  # start the county vote count
            else:
                # add candidate's votes to the county dict
                results_dict[row['CountyName']][row['CandidateLastName']] = row['CandidateVotes']
                # add the total votes in the county
                total_votes += int(row['CandidateVotes'])
                # add total votes to the county dict (updates on last iteration to correct count)
                results_dict[row['CountyName']]['TotalVotes'] = total_votes
        elif congress in row['OfficeDescription']:
            if congress_county != row['CountyName']:
                congress_county = row['CountyName']
                total_congress = int(row['CandidateVotes'])
                cong_key = row['PartyName'] + 'Congress'
                results_dict[congress_county][cong_key] = row['CandidateVotes']
            else:
                cong_key = row['PartyName'] + 'Congress'
                results_dict[congress_county][cong_key] = row['CandidateVotes']
                total_congress += int(row['CandidateVotes'])
                results_dict[row['CountyName']]['TotalCongress'] = total_congress

# add the official number of registered voters to the dict
with open('voters.csv', newline='') as csvfile:
    v_reader = csv.DictReader(csvfile, delimiter=',')
    for row in v_reader:
        key = row['CountyName']
        results_dict[key]['VotersRegistered'] = row['Voters']
        turnout = int(results_dict[key]['TotalVotes']) / int(row['Voters'])
        results_dict[key]['Turnout'] = "{:.2%}".format(turnout)

# calculate percentages of votes per county and add to county dicts in results_dict
with open('MI_results.csv', newline='') as csvfile:
    res_reader = csv.DictReader(csvfile, delimiter='\t')
    for row2 in res_reader:
        if row2['OfficeDescription'] == office:
            key1 = row2['CountyName']
            key2 = row2['CandidateLastName'] + 'Percent'
            candidate_percent = int(row2['CandidateVotes']) / int(results_dict[row2['CountyName']]['TotalVotes'])
            results_dict[key1][key2] = "{:.2%}".format(candidate_percent)

        if congress in row2['OfficeDescription']:
            party_key = row2['PartyName'] + 'CongressPercent'
            party_percent = int(row2['CandidateVotes']) / int(results_dict[row2['CountyName']]['TotalCongress'])
            results_dict[row2['CountyName']][party_key] = "{:.2%}".format(party_percent)

for k, v in results_dict.items():
    results_dict[k]['DEMDifference'] = int(results_dict[k]['Biden']) - int(results_dict[k]['DEMCongress'])
    results_dict[k]['REPDifference'] = int(results_dict[k]['Trump']) - int(results_dict[k]['REPCongress'])
print('{} ######################################################################### {}'.format(bcolors.RED, bcolors.ENDC))
print(' *********{} 2020 Michigan General Election Results by County{} *********'.format(bcolors.BOLD, bcolors.ENDC))
print('{} ######################################################################### {}\n'.format(bcolors.BLUE, bcolors.ENDC))
while True:
    print('Enter a county name or one of the below options to continue:\n')
    print('q: Quit\nall: List all results\nl: List all counties\n')
    county_query = input('Enter a county or option: ')
    county_query = county_query.upper()
    if county_query == 'Q':
        break
    if county_query == 'ALL':
        print('\n Results for all Counties: \n')
        for k, v in results_dict.items():
            print(k.capitalize(), ' County: ')
            for k2, v2 in v.items():
                print(k2, ': ', v2)
    if county_query == 'L':
        print('List of all counties:\n')
        for k, v in results_dict.items():
            print(k.capitalize())
    else:
        print('\n Results for ', county_query, ' County: \n')
        if county_query not in results_dict:
            print("{} {} County not found. Please try again.{}{}".format(bcolors.WARNING, bcolors.BOLD, bcolors.ENDC, bcolors.ENDC))
            continue
        for k, v in results_dict[county_query].items():
            if k == 'Trump' or k == 'TrumpPercent':
                print('{}{}{} : {}{}\n############'.format(bcolors.RED, bcolors.BOLD,  k, v, bcolors.ENDC))
            elif k == 'Biden' or k == 'BidenPercent':
                print('{}{}{} : {}{}\n############'.format(bcolors.BLUE, bcolors.BOLD, k, v, bcolors.ENDC))
            elif k == 'REPCongress' or k == 'REPCongressPercent':
                print('{}{}{} : {}{}\n############'.format(bcolors.RED, bcolors.BOLD, k, v, bcolors.ENDC))
            elif k == 'DEMCongress' or k == 'DEMCongressPercent':
                print('{}{}{} : {}{}\n############'.format(bcolors.BLUE, bcolors.BOLD, k, v, bcolors.ENDC))
            elif k == 'REPDifference':
                print('{}{}{} : {}{}\n############'.format(bcolors.RED, bcolors.BOLD,  k, v, bcolors.ENDC))
            elif k == 'DEMDifference' or k == 'DEMCongressPercent':
                print('{}{}{} : {}{}\n############'.format(bcolors.BLUE, bcolors.BOLD, k, v, bcolors.ENDC))

        print('{}Total Votes: {}{}'.format(bcolors.BOLD, results_dict[county_query]['TotalVotes'], bcolors.ENDC))
        print('{}Total Congress Votes: {}{}'.format(bcolors.BOLD, results_dict[county_query]['TotalCongress'], bcolors.ENDC))
        print('{}Registered Voters: {}{}'.format(bcolors.BOLD, results_dict[county_query]['VotersRegistered'], bcolors.ENDC))
        print('{}{}Turnout: {}{}\n'.format(bcolors.BOLD, bcolors.CYAN, results_dict[county_query]['Turnout'], bcolors.ENDC))