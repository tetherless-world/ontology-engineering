from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import OWL, RDF
import pandas as pd
import numpy as np



def createNode(namespace, name):
    # return exec("{}/{}".format(namespace, name))
    return URIRef(f"{namespace}{name}")

def importHouseElection(rdf, districtDF, year, namespaces, stateDistrict, verbose=False):

    PJ, PJE, RnC = namespaces

    #create political office in rdf {State, YYYY, FederalRepresentative, District}
    politicalOfficeName = districtDF['STATE'].values[0].replace(" ","") + str(year) + "FederalRepresentative" + stateDistrict.strip()
    politicalOffice = createNode(PJE, politicalOfficeName)
    rdf.add((politicalOffice, RDF.type, PJ.FederalRepresentative))
    #create general election
    generalElectionName = politicalOfficeName + "GeneralElection"
    generalElection = createNode(PJE, generalElectionName)
    rdf.add((generalElection, RDF.type, PJ.GeneralElection))
    rdf.add((generalElection, PJ.isElectionFor, politicalOffice))

    #compute and add election margin
    if len(marginNums := districtDF['GENERAL %'].unique()) > 1:
        v1, v2 = -np.sort(-(marginNums))[:2]
        marginNum = (v1 - v2)
        if marginNum < .02:
            rdf.add((generalElection, PJ.hasElectionMargin, PJ.NarrowMargin))
        elif marginNum < .05:
            rdf.add((generalElection, PJ.hasElectionMargin, PJ.CompetitiveMargin))
        elif marginNum < .15:
            rdf.add((generalElection, PJ.hasElectionMargin, PJ.SubstantialMargin))
        else:
            rdf.add((generalElection, PJ.hasElectionMargin, PJ.LandslideMargin))
    else:
        rdf.add((generalElection, PJ.hasElectionMargin, PJ.LandslideMargin))


    for i, row in districtDF.iterrows():
        if isinstance(row["CANDIDATE NAME (First)"], str) and ('R' in row["PARTY"] or 'D' in row["PARTY"]):
            personName = (row["CANDIDATE NAME (First)"] + row["CANDIDATE NAME (Last)"]).replace(".", "").replace(" ", "").replace("\"", "")
            print(str(personName.encode('ascii', 'ignore')) + "  ", end='')
            #create person with given name in rdf
            person = createNode(PJE, personName)
            rdf.add((person, RDF.type, PJ.Person))
            #create candidacy
            candidate = createNode(PJE, "Candidate" + personName + str(year))
            rdf.add((candidate, RDF.type, PJ.PoliticalCandidate))
            rdf.add((person, RnC.hasRole, candidate))
            rdf.add((candidate, PJ.isRunningFor, politicalOffice))

            party = 'R' if 'R' in row["PARTY"] else 'D'
            primaryElection = None

            if row["GE WINNER INDICATOR"] == 'W':
                print("General Winner  ", end='')
                #mark as winner of general election
                rdf.add((generalElection, PJ.hasElectionWinner, candidate))
            if row["PE WINNER INDICATOR"] == 'W':
                print("Primary Winner  ", end='')
                #add as candidate to general election, if not already
                if not (generalElection, PJ.hasElectionWinner, candidate) in rdf:
                    rdf.add((generalElection, PJ.hasElectionCandidate, candidate))
                #create primary election if not exist
                primaryElectionName = politicalOfficeName + "PrimaryElection" + party
                primaryElection = createNode(PJE, primaryElectionName)
                if not (primaryElection, None, None) in rdf:
                    rdf.add((primaryElection, RDF.type, PJ.PrimaryElection))
                    if len((marginNums := districtDF['PRIMARY %'].unique())) > 1:
                        v1, v2 = -np.sort(-(marginNums))[:2]
                        marginNum = (v1 - v2)
                        if marginNum < .02:
                            rdf.add((primaryElection, PJ.hasElectionMargin, PJ.NarrowMargin))
                        elif marginNum < .05:
                            rdf.add((primaryElection, PJ.hasElectionMargin, PJ.CompetitiveMargin))
                        elif marginNum < .15:
                            rdf.add((primaryElection, PJ.hasElectionMargin, PJ.SubstantialMargin))
                        else:
                            rdf.add((primaryElection, PJ.hasElectionMargin, PJ.LandslideMargin))
                    else:
                        rdf.add((primaryElection, PJ.hasElectionMargin, PJ.LandslideMargin))
                #add as winner to primary election
                rdf.add((primaryElection, PJ.hasElectionWinner, candidate))
            if party == 'R' and primaryElection:
                print("Rep Candidate  ", end='')
                #add to Rep primary
                if not (primaryElection, PJ.hasElectionWinner, candidate) in rdf:
                    rdf.add((primaryElection, PJ.hasElectionCandidate, candidate))
                if not (PJ.RepublicanParty, RDF.type, PJ.PoliticalParty) in rdf:
                    rdf.add((PJ.RepublicanParty, RDF.type, PJ.PoliticalParty))
                rdf.add((candidate, PJ.hasPoliticalParty, PJ.RepublicanParty))
            elif party == 'D' and primaryElection:
                print("Dem Candidate  ", end='')
                #add to Dem primary
                if not (primaryElection, PJ.hasElectionWinner, candidate) in rdf:
                    rdf.add((primaryElection, PJ.hasElectionCandidate, candidate))
                if not (PJ.DemocratParty, RDF.type, PJ.PoliticalParty) in rdf:
                    rdf.add((PJ.DemocratParty, RDF.type, PJ.PoliticalParty))
                rdf.add((candidate, PJ.hasPoliticalParty, PJ.DemocratParty))
            print()
            if verbose:
                for s, p, o in rdf.triples((person, None, None)):
                    print(f"{s}, {p}, {o}")
                    print()
    if verbose:
        for s, p, o in rdf.triples((generalElection, None, None)):
            print(f"{s}, {p}, {o}")
            print()
        for s, p, o in rdf.triples((createNode(PJE, primaryElectionName[:-1] + "R"), None, None)):
            print(f"{s}, {p}, {o}")
            print()
        for s, p, o in rdf.triples((createNode(PJE, primaryElectionName[:-1] + "D"), None, None)):
            print(f"{s}, {p}, {o}")
            print()

def importHouseElections(rdf, houseDF, year, namespaces, verbose=False):

    PJ, PJE, RnC = namespaces

    for stateAbbrev in houseDF['STATE ABBREVIATION'].unique()[1:]:
        if verbose: print(stateAbbrev)
        for stateDistrict in (stateDF := houseDF.loc[houseDF['STATE ABBREVIATION'] == stateAbbrev])['DISTRICT'].unique()[:-1]:
            if verbose: print(stateDistrict)
            districtDF = stateDF.loc[stateDF['DISTRICT'] == stateDistrict]
            importHouseElection(rdf, districtDF, year, namespaces, stateDistrict, verbose=verbose)

def importSenateElection(rdf, stateDF, year, namespaces, verbose=False):
    PJ, PJE, RnC = namespaces

    #create political office in rdf ( State, YYYY, FederalSenator)
    politicalOfficeName = stateDF['STATE'].values[0].replace(" ","") + str(year) + "FederalSenator"
    politicalOffice = createNode(PJE, politicalOfficeName)
    rdf.add((politicalOffice, RDF.type, PJ.FederalSenator))

    #create general election
    generalElectionName = politicalOfficeName + "GeneralElection"
    generalElection = createNode(PJE, generalElectionName)
    rdf.add((generalElection, RDF.type, PJ.GeneralElection))
    rdf.add((generalElection, PJ.isElectionFor, politicalOffice))

    #compute and add election margin
    if len(marginNums := stateDF['GENERAL %'].unique()) > 1:
        v1, v2 = -np.sort(-(marginNums))[:2]
        marginNum = (v1 - v2)
        if marginNum < .02:
            rdf.add((generalElection, PJ.hasElectionMargin, PJ.NarrowMargin))
        elif marginNum < .05:
            rdf.add((generalElection, PJ.hasElectionMargin, PJ.CompetitiveMargin))
        elif marginNum < .15:
            rdf.add((generalElection, PJ.hasElectionMargin, PJ.SubstantialMargin))
        else:
            rdf.add((generalElection, PJ.hasElectionMargin, PJ.LandslideMargin))
    else:
        rdf.add((generalElection, PJ.hasElectionMargin, PJ.LandslideMargin))

    for i, row in stateDF.iterrows():
        if isinstance(row["CANDIDATE NAME (First)"], str) and ('R' in row["PARTY"] or 'D' in row["PARTY"]):
            personName = (row["CANDIDATE NAME (First)"] + row["CANDIDATE NAME (Last)"]).replace(".", "").replace(" ", "").replace("\"", "")
            print(str(personName.encode('ascii', 'ignore')) + "  ", end='')
            #create person with given name in rdf
            person = createNode(PJE, personName)
            rdf.add((person, RDF.type, PJ.Person))
            #create candidacy
            candidate = createNode(PJE, "Candidate" + personName + str(year))
            rdf.add((candidate, RDF.type, PJ.PoliticalCandidate))
            rdf.add((person, RnC.hasRole, candidate))
            rdf.add((candidate, PJ.isRunningFor, politicalOffice))

            party = 'R' if 'R' in row["PARTY"] else 'D'
            primaryElection = None

            if row["GE WINNER INDICATOR"] == 'W':
                print("General Winner  ", end='')
                #mark as winner of general election
                rdf.add((generalElection, PJ.hasElectionWinner, candidate))
            if row["PE WINNER INDICATOR"] == 'W':
                print("Primary Winner  ", end='')
                #add as candidate to general election, if not already
                if not (generalElection, PJ.hasElectionWinner, candidate) in rdf:
                    rdf.add((generalElection, PJ.hasElectionCandidate, candidate))
                #create primary election if not exist
                primaryElectionName = politicalOfficeName + "PrimaryElection" + party
                primaryElection = createNode(PJE, primaryElectionName)
                if not (primaryElection, None, None) in rdf:
                    rdf.add((primaryElection, RDF.type, PJ.PrimaryElection))
                    if len((marginNums := stateDF['PRIMARY %'].unique())) > 1:
                        v1, v2 = -np.sort(-(marginNums))[:2]
                        marginNum = (v1 - v2)
                        if marginNum < .02:
                            rdf.add((primaryElection, PJ.hasElectionMargin, PJ.NarrowMargin))
                        elif marginNum < .05:
                            rdf.add((primaryElection, PJ.hasElectionMargin, PJ.CompetitiveMargin))
                        elif marginNum < .15:
                            rdf.add((primaryElection, PJ.hasElectionMargin, PJ.SubstantialMargin))
                        else:
                            rdf.add((primaryElection, PJ.hasElectionMargin, PJ.LandslideMargin))
                    else:
                        rdf.add((primaryElection, PJ.hasElectionMargin, PJ.LandslideMargin))
                #add as winner to primary election
                rdf.add((primaryElection, PJ.hasElectionWinner, candidate))
            if party == 'R' and primaryElection:
                print("Rep Candidate  ", end='')
                #add to Rep primary
                if not (primaryElection, PJ.hasElectionWinner, candidate) in rdf:
                    rdf.add((primaryElection, PJ.hasElectionCandidate, candidate))
                if not (PJ.RepublicanParty, RDF.type, PJ.PoliticalParty) in rdf:
                    rdf.add((PJ.RepublicanParty, RDF.type, PJ.PoliticalParty))
                rdf.add((candidate, PJ.hasPoliticalParty, PJ.RepublicanParty))
            elif party == 'D' and primaryElection:
                print("Dem Candidate  ", end='')
                #add to Dem primary
                if not (primaryElection, PJ.hasElectionWinner, candidate) in rdf:
                    rdf.add((primaryElection, PJ.hasElectionCandidate, candidate))
                if not (PJ.DemocratParty, RDF.type, PJ.PoliticalParty) in rdf:
                    rdf.add((PJ.DemocratParty, RDF.type, PJ.PoliticalParty))
                rdf.add((candidate, PJ.hasPoliticalParty, PJ.DemocratParty))
            print()
            if verbose:
                for s, p, o in rdf.triples((person, None, None)):
                    print(f"{s}, {p}, {o}")
                    print()
    if verbose:
        for s, p, o in rdf.triples((generalElection, None, None)):
            print(f"{s}, {p}, {o}")
            print()
        for s, p, o in rdf.triples((createNode(PJE, primaryElectionName[:-1] + "R"), None, None)):
            print(f"{s}, {p}, {o}")
            print()
        for s, p, o in rdf.triples((createNode(PJE, primaryElectionName[:-1] + "D"), None, None)):
            print(f"{s}, {p}, {o}")
            print()


def importSenateElections(rdf, senateDF, year, namespaces, verbose=False):
    PJ, PJE, RnC = namespaces

    for stateAbbrev in senateDF['STATE ABBREVIATION'].unique()[1:]:
        if verbose: print(stateAbbrev)
        stateDF = senateDF.loc[senateDF['STATE ABBREVIATION'] == stateAbbrev]
        importSenateElection(rdf, stateDF, year, namespaces, verbose=verbose)

def importElections(rdfFilename, dataFilename, year):
    # senateSheet, houseSheet = "US Senate Results by State", "US House Results by State"
    # data_dict = pd.read_excel(dataFilename, [senateSheet, houseSheet])
    dataDict = pd.read_excel(dataFilename, [11, 12])
    rdf = Graph()
    rdf.parse(rdfFilename)
    rdf.bind("owl", OWL)
    PJ = Namespace("https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism#")
    rdf.bind("pj", PJ)
    PJE = Namespace("https://tw.rpi.edu/ontology-engineering/oe2024/political-journalism/PoliticalJournalism-Election-Individuals#")
    rdf.bind("pje", PJE)
    RnC = Namespace("https://www.omg.org/spec/Commons/RolesAndCompositions/")
    rdf.bind('rnc', RnC)
    rdf.bind('rdf', RDF)


    importHouseElections(rdf, dataDict[12], year, (PJ, PJE, RnC))

    importSenateElections(rdf, dataDict[11], year, (PJ, PJE, RnC))

    rdf.serialize(destination="../PoliticalJournalism-Election-Individuals.rdf", format='xml')


def main():
    importElections("../PoliticalJournalism.rdf", "federalelections2020.xlsx", 2020)

if __name__ == '__main__':
    main()
