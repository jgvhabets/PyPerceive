### create a Timing class """

from dataclasses import dataclass

@dataclass (init=True, repr=True)
class timingClass:
    """
    timing Class 
    
    parameters:
        (input from main dataclass PerceiveData)
        - sub:
        - rec_modality: "Streaming", "Survey", "Timeline"

    Returns:
        - 
    
    """