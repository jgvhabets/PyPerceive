""" Metadata Class """

from dataclasses import dataclass, field


@dataclass(init=True, repr=True) 
class MetadataClass:
    """
    Metadata class to store repetitive variables that are changing constantly throughout the hierarchy
    
    parameters:
        - sub: number of subject e.g. "021" (make sure to use exactly three digits)
        - incl_modalities: a list of recording modalities to include ["survey", "streaming", "timeline", "indefiniteStreaming"] 
        - incl_timing: a list of timing sessions to include ["postop", "fu3m", "fu12m", "fu18m", "fu24m"]
        - incl_cond: a list of conditions to include  ["m0s0", "m1s0", "m0s1", "m1s1"]
        - incl_task: a list of tasks to include ["rest", "tapping", "updrs"]
        - orig_meta_table: original metadata table read with pd.read_excel()

    post-initialized parameters:
        
    Returns:
        - 
    """
    

    sub: str            
    incl_modalities: list
    incl_session: list 
    incl_condition: list 
    incl_task: list
    orig_meta_table: any # pd.DataFrame read with pd.read_excel(), will stay original and won´t be changed
    




