from Utils.Genes import Genes
import random
import math

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
    
    def __init__(self, ParentGenome = None, MutationRate = 0.5, geneLength = 4):
        self.Sequence = self.GenerateGenome(ParentGenome, MutationRate, geneLength)
        
        pass


    @staticmethod
    def GenerateGenome(ParentGenome=None, MutationRate = 0.5, geneLength = 4):
        """
        Generate a genome sequence based on the parent genome(if applicable) and mutation rate
        """
        sequence = {}
        allGenes = Genes.Genes
        selectedGenes = list(allGenes.keys())

        print(f"[PAI][GENOMES SEQUENCER]: Generating genome sequence with {geneLength} genes")
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
                print(f"[PAI][GENOMES SEQUENCER]: No base value for gene: {gene}")
                continue
            
            print(f"[PAI][GENOMES SEQUENCER]: Generating gene: {gene}")
            #Check for parent genome
            parentValue = ParentGenome.get(gene, None) if ParentGenome is not None else 0
            
            #Initial genome value
            newValue = geneData.get('baseValue')
            print(f"[PAI][GENOMES SEQUENCER]: Initial value for gene: {gene} is {newValue}")
            
            #Mutate the gene value
            if random.random() < MutationRate:
                newValue = newValue + random.uniform(-geneData.get('deviation', 0), geneData.get('deviation', 1))

            print(f"[PAI][GENOMES SEQUENCER]: Mutated value for gene: {gene} is {newValue}")
            
            #Influence from parent value
            if parentValue != 0:
                print(f"[PAI][GENOMES SEQUENCER]: Parent value for gene: {gene} is {parentValue}")
                newValue = (newValue * abs(MutationRate - 1)) + (parentValue * MutationRate)
            print(f"[PAI][GENOMES SEQUENCER]: Final value for gene: {gene} is {newValue}")
            
            #Get the gene value in the sequence
            sequence[gene] = {
                'value': newValue,
                'baseValue': basevalue,
                'deviation': geneData.get('deviation'),
                'description': geneData.get('description'),
                'genomicrange': geneData.get('genomicrange')
            }
            print(f"[PAI][GENOMES SEQUENCER]: Gene {gene} added to sequence")
            
        return sequence
    

Agent = Genome(None, 0.5, 4)
print(Agent)
print(str(Agent))
