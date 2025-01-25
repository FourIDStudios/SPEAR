import random

class Genes:
    Genes = {
        'SocialAffinityGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases social affinity, making the agent more extroverted.",
            'genomicrange': [0, 0.5]
        },
        'SocialAffinityDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases social affinity, making the agent more introverted.",
            'genomicrange': [0, 0.5]
        },
        'RiskAversionGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases risk aversion, making the agent more cautious.",
            'genomicrange': [0, 0.5]
        },
        'RiskAversionDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases risk aversion, making the agent more of a risk-taker.",
            'genomicrange': [0, 0.5]
        },
        'AdaptabilityGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases adaptability, making the agent more flexible.",
            'genomicrange': [0, 0.5]
        },
        'AdaptabilityDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases adaptability, making the agent more rigid.",
            'genomicrange': [0, 0.5]
        },
        'CuriosityGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases curiosity, making the agent more likely to explore.",
            'genomicrange': [0, 0.5]
        },
        'CuriosityDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases curiosity, making the agent stick to routines.",
            'genomicrange': [0, 0.5]
        },
        'SelfDisciplineGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases self-discipline, making the agent more disciplined.",
            'genomicrange': [0, 0.5]
        },
        'SelfDisciplineDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases self-discipline, making the agent more impulsive.",
            'genomicrange': [0, 0.5]
        },
        'EmpathyGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases empathy, making the agent more emotionally supportive.",
            'genomicrange': [0, 0.5]
        },
        'EmpathyDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases empathy, making the agent more detached.",
            'genomicrange': [0, 0.5]
        },
        'StressToleranceGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases stress tolerance, making the agent more calm and composed.",
            'genomicrange': [0, 0.5]
        },
        'StressToleranceDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases stress tolerance, making the agent more easily overwhelmed.",
            'genomicrange': [0, 0.5]
        },
        'OptimismGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases optimism, making the agent more positive.",
            'genomicrange': [0, 0.5]
        },
        'OptimismDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases optimism, making the agent more pessimistic.",
            'genomicrange': [0, 0.5]
        },
        'AmbitionGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases ambition, making the agent more driven.",
            'genomicrange': [0, 0.5]
        },
        'AmbitionDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases ambition, making the agent more content with the status quo.",
            'genomicrange': [0, 0.5]
        },
        'EnergyLevelGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases energy level, making the agent more energetic.",
            'genomicrange': [0, 0.5]
        },
        'EnergyLevelDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases energy level, making the agent more lethargic.",
            'genomicrange': [0, 0.5]
        },
        'HungerSensitivityGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases hunger sensitivity, making the agent more responsive to hunger.",
            'genomicrange': [0, 0.5]
        },
        'HungerSensitivityDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases hunger sensitivity, making the agent less responsive to hunger.",
            'genomicrange': [0, 0.5]
        },
        'SleepRequirementGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases sleep requirement, making the agent need more sleep.",
            'genomicrange': [0, 0.5]
        },
        'SleepRequirementDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases sleep requirement, making the agent need less sleep.",
            'genomicrange': [0, 0.5]
        },
        'SpendingHabitsGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases spending habits, making the agent more extravagant.",
            'genomicrange': [0, 0.5]
        },
        'SpendingHabitsDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases spending habits, making the agent more frugal.",
            'genomicrange': [0, 0.5]
        },
        'AltruismGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases altruism, making the agent more generous and giving.",
            'genomicrange': [0, 0.5]
        },
        'AltruismDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases altruism, making the agent more self-centered.",
            'genomicrange': [0, 0.5]
        },
        'ConformityGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases conformity, making the agent more of a rule follower.",
            'genomicrange': [0, 0.5]
        },
        'ConformityDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases conformity, making the agent more of a rebel/independent thinker.",
            'genomicrange': [0, 0.5]
        },
        'PreferenceForRoutineGain': {
            'baseValue': 0.1,
            'deviation': 0.05,
            'description': "Increases preference for routine, making the agent rely more on consistent routines.",
            'genomicrange': [0, 0.5]
        },
        'PreferenceForRoutineDrain': {
            'baseValue': 0.05,
            'deviation': 0.03,
            'description': "Decreases preference for routine, making the agent thrive on change.",
            'genomicrange': [0, 0.5]
        }
        }
    
    @staticmethod
    def mutate_gene(gene, mutationRate):
        mutationFactor = random.random() * 0.1 - mutationRate  # +/- 5% mutation
        gene['value'] += mutationFactor

        # Ensure the gene value stays within the genomic range
        gene['value'] = max(gene['genomicrange'][0], min(gene['value'], gene['genomicrange'][1]))
        return gene