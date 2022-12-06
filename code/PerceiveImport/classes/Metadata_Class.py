""" Metadata Class """

from dataclasses import dataclass, field


@dataclass(init=True, repr=True) 
class MetadataClass:
    """
    Metadata class to store repetitive variables that are changing constantly throughout the hierarchy
    
    parameters:
        - sub: subject name called sub-xxx, e.g. "021" (make sure to use exactly the same str as your subject folder is called)
        - incl_modalities: list
        - incl_session: list  
        - incl_med: list 
        - incl_condition: list
        - metadata: any

    post-initialized parameters:
        
    Returns:
        - 
    """
    

    sub: str            
    incl_modalities: list
    incl_session: list 
    incl_condition: list 
    incl_task: list
    metadata: any # pd.DataFrame from MainClass, will be modified in each class 
    
    



    def __post_init__(self,): 

        print("MetadataClass has been loaded")



