#Import the necessary libraries
from Utils.Genes import Genes
from Utils.Logger import Logger
import json
import random
import math
import os

#Initial Setup
Logger.debug = True

#Fetch Configurations
Settings = {}
targetDir = os.path.join(os.path.dirname(__file__), 'Utils\\settings.json')
Logger.logln(f"[PAI][GENOMES SEQUENCER]: Fetching settings from {targetDir}")
with open(targetDir) as f:
    Settings = json.load(f)

class Genome:
    """
    This class represents a simple example. hereditary information unique to each agent. 
    It encodes genetic traits that influence behavior, decision-making, and performance in various states 
    in the form of a readable string sequence.

    Attributes:
        
    """
    
    def __str__(self):
        sequenceString = ""
        
        # Iterate through each gene in the sequence
        for geneName, gene in self.Sequence.items():
            # Format the gene value based on the rules:
            geneAbbr = geneName[:4]

            # Determine the first two characters for positive/negative and range status
            signChar = geneAbbr[0].upper() if gene['value'] > 0 else geneAbbr[0].lower()
            rangeChar = geneAbbr[1].upper() if gene['genomicrange'][0] <= gene['value'] <= gene['genomicrange'][1] else geneAbbr[1].lower()

            # Get the numerical value (formatted to one decimal place if it's a float)
            numValue = f"{gene['value']:.1f}"
            valueChars = numValue[:3] if numValue[1] == '.' else numValue

            # If the value is a whole number, add a fourth character
            formattedGene = signChar + rangeChar + valueChars + geneAbbr[2:4]

            # Add the formatted gene to the sequence string
            sequenceString += formattedGene
        return sequenceString
    
    def __init__(self, ParentGenome = None, MutationRate = Settings['DefaultParentMutationRate'], geneLength = Settings['GenomeLength']):
        self.Sequence = self.GenerateGenome(ParentGenome, MutationRate, geneLength)
        
        pass


    @staticmethod
    def GenerateGenome(ParentGenome=None, MutationRate = Settings['DefaultParentMutationRate'], geneLength = Settings['GenomeLength']):
        """
        Generate a genome sequence based on the parent genome(if applicable) and mutation rate
        """
        sequence = {}
        allGenes = Genes.Genes
        selectedGenes = list(allGenes.keys())

        Logger.logln(f"[PAI][GENOMES SEQUENCER]: Generating genome sequence with {geneLength} genes")
        # shuffle the gene pool to select random genes
        random.shuffle(selectedGenes)
        
        #Limit the genes selected to the geneLength
        selectedGenes = selectedGenes[:geneLength]
        
        #Iterate through the selected genes
        for gene in selectedGenes:
            geneData = allGenes[gene]
            
            #Check for base value
            basevalue = geneData.get('baseValue', None)
            if basevalue is None:
                Logger.logln(f"[PAI][GENOMES SEQUENCER]: No base value for gene: {gene}")
                continue
            
            Logger.logln(f"[PAI][GENOMES SEQUENCER]: Generating gene: {gene}")
            #Check for parent genome
            parentValue = 0
            if(ParentGenome is not None):
                #Check If the parent genome has the gene
                if gene in ParentGenome:
                    Logger.logln(f"[PAI][GENOMES SEQUENCER]: Parent genome has gene: {gene}")
                    parentValue = ParentGenome[gene].get('value')
            Logger.logln(f"[PAI][GENOMES SEQUENCER]: Parent value is {parentValue} {'Meaning there is no parent gene' if parentValue == 0 else ''}")
            
            #Initial genome value
            newValue = geneData.get('baseValue')
            Logger.logln(f"[PAI][GENOMES SEQUENCER]: Initial value for gene: {gene} is {newValue}")
            
            #Mutate the gene value
            newValue = newValue + random.uniform(-geneData.get('deviation', 0)*Settings['NaturalMutationRate'], geneData.get('deviation', 1)*Settings['NaturalMutationRate'])

            Logger.logln(f"[PAI][GENOMES SEQUENCER]: Mutated value for gene: {gene} is {newValue}")
            
            #Influence from parent value
            if parentValue != 0:
                #Dividers for Logger.logln output
                Logger.logln(f"[PAI][GENOMES SEQUENCER]: Parent value for gene: {gene} is {parentValue}")
                newValue = (newValue * abs(MutationRate - 1)) + (parentValue * MutationRate)
            Logger.logln(f"[PAI][GENOMES SEQUENCER]: Final value for gene: {gene} is {newValue}")
            
            #Get the gene value in the sequence
            sequence[gene] = {
                'value': newValue,
                'baseValue': basevalue,
                'deviation': geneData.get('deviation'),
                'description': geneData.get('description'),
                'genomicrange': geneData.get('genomicrange')
            }
            Logger.logln(f"[PAI][GENOMES SEQUENCER]: Gene {gene} added to sequence\n")
            
        return sequence
    
    def getpureSequence(self):
        """
        Get the pure genome sequence without any formatting
        """
        return self.Sequence
    
    def mutateGene(self, geneName, mutationRate):
        """
        Mutate a gene in the genome sequence
        """
        gene = self.Sequence.get(geneName)
        if gene:
            self.Sequence[geneName] = Genes.mutate_gene(gene, mutationRate)
            # Ensure the gene value stays within the genomic range, This is commented out because i want to see the effect of the mutation given drastic conditions
            # gene['value'] = max(gene['genomicrange'][0], min(gene['value'], gene['genomicrange'][1]))
        else:
            Logger.logln(f"[PAI][GENOMES SEQUENCER]: Could not mutate gene: {geneName} because it does not exist.")

Logger.logln(f"[PAI][GENOMES SEQUENCER]: Creating Agent A", True)
AgentA = {
    'Name': "Agent A",
    'Genome': Genome(),
}
Logger.logln(f"[PAI][GENOMES SEQUENCER]: Creating Agent B, with Agent A as parent", True)
AgentB = {
    'Name': "Agent A",
    'Genome': Genome(AgentA['Genome'].getpureSequence()),
}



