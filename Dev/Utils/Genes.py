import random

class Genes:
    Genes = {
        'HungerGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases hunger faster, making the agent feel hungry more often.",
            'genomicrange': [0, 0.5]
        },
        'HungerDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Reduces the rate of hunger increase, keeping the agent satisfied for longer periods.",
            'genomicrange': [0, 0.5]
        },
        'SleepGain': {
            'baseValue': 0.1,
            'deviation': 0.04,
            'description': "Increases the agent's need for sleep, causing them to feel tired more quickly.",
            'genomicrange': [0, 0.5]
        },
        'SleepDrain': {
            'baseValue': 0.05,
            'deviation': 0.02,
            'description': "Reduces the agent's need for sleep, allowing them to function well with less rest.",
            'genomicrange': [0, 0.5]
        },
        'WorkEthic': {
            'baseValue': 0.2,
            'deviation': 0.05,
            'description': "Improves the agent's motivation and efficiency at work, leading to more productivity.",
            'genomicrange': [0, 0.5]
        },
        'WorkFatigue': {
            'baseValue': 0.1,
            'deviation': 0.04,
            'description': "Causes the agent to tire more quickly during work, reducing work efficiency.",
            'genomicrange': [0, 0.5]
        },
        'Focus': {
            'baseValue': 0.15,
            'deviation': 0.05,
            'description': "Enhances the agent's ability to concentrate on tasks, increasing work and learning efficiency.",
            'genomicrange': [0, 0.5]
        },
        'Distraction': {
            'baseValue': 0.1,
            'deviation': 0.04,
            'description': "Makes it easier for the agent to get distracted, lowering concentration and efficiency.",
            'genomicrange': [0, 0.5]
        },
        'MetabolismBoost': {
            'baseValue': 0.1,
            'deviation': 0.03,
            'description': "Increases the rate at which the agent processes food, reducing hunger and food requirements.",
            'genomicrange': [0, 0.5]
        },
        'FoodSensitivity': {
            'baseValue': 0.1,
            'deviation': 0.04,
            'description': "Increases sensitivity to food, causing negative effects from certain meals.",
            'genomicrange': [0, 0.5]
        },
        'SocialNeed': {
            'baseValue': 0.2,
            'deviation': 0.05,
            'description': "Increases the agent's need for social interaction, making them crave companionship.",
            'genomicrange': [0, 0.5]
        },
        'SocialFatigue': {
            'baseValue': 0.1,
            'deviation': 0.03,
            'description': "Causes the agent to become tired from socializing, limiting the duration of social interactions.",
            'genomicrange': [0, 0.5]
        },
        'Charisma': {
            'baseValue': 0.15,
            'deviation': 0.05,
            'description': "Improves the agent's ability to charm and influence others, facilitating social bonds.",
            'genomicrange': [0, 0.5]
        },
        'Repulsion': {
            'baseValue': 0.1,
            'deviation': 0.04,
            'description': "Makes the agent more likely to repel others, reducing their ability to form relationships.",
            'genomicrange': [0, 0.5]
        },
        'LearningSpeed': {
            'baseValue': 0.2,
            'deviation': 0.05,
            'description': "Increases the rate at which the agent learns new information and skills.",
            'genomicrange': [0, 0.5]
        },
        'LearningResistance': {
            'baseValue': 0.1,
            'deviation': 0.04,
            'description': "Makes the agent less receptive to learning new skills and concepts.",
            'genomicrange': [0, 0.5]
        },
        'Curiosity': {
            'baseValue': 0.15,
            'deviation': 0.05,
            'description': "Increases the agent's desire to explore and acquire new knowledge.",
            'genomicrange': [0, 0.5]
        },
        'Apathy': {
            'baseValue': 0.1,
            'deviation': 0.04,
            'description': "Decreases the agent's desire to learn, making them indifferent to self-improvement.",
            'genomicrange': [0, 0.5]
        },
        'RiskTaking': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases the agent's willingness to engage in risky activities or take chances.",
            'genomicrange': [0, 0.5]
        },
        'Cautiousness': {
            'baseValue': 0.15,
            'deviation': 0.05,
            'description': "Makes the agent more careful and hesitant, avoiding risky actions and preferring to think things through.",
            'genomicrange': [0, 0.5]
        },
        'Impulsiveness': {
            'baseValue': 1,
            'deviation': 0.5,
            'description': "Affects the agent's willingness to stay in states.",
            'genomicrange': [-1, 1]
        },
        'RiskTolerance': {
            'baseValue': 0.15,
            'deviation': 0.05,
            'description': "Makes the agent more careful and hesitant, avoiding risky actions and preferring to think things through.",
            'genomicrange': [0, 0.5]
        }}
    
    @staticmethod
    def mutate_gene(gene):
        mutationFactor = random.random() * 0.1 - 0.05  # +/- 5% mutation
        gene['value'] += mutationFactor

        # Ensure the gene value stays within the genomic range
        gene['value'] = max(gene['genomicrange'][0], min(gene['value'], gene['genomicrange'][1]))