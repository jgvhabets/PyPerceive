""" PLOTLY line plots """


import plotly.express as px
import plotly.graph_objs as go


def peakFrequencyOverTime(DataFrameInput):
    """
    this function uses plotly to plot a line plot
    Input: has to be a Dataframe with specifically named columns: "Session", "Peak_frequency_highBeta"
   
    """

    fig = go.Figure(data=go.Scatter(x=DataFrameInput['Session'].astype(dtype=str), 
                        y=DataFrameInput['Peak_frequency_highBeta'],
                        marker_color='indianred', text="counts"))
                        
    fig.update_layout({"title": 'Peak frequency over time',
                   "xaxis": {"title":"Follow-Up dates"},
                   "yaxis": {"title":"Peak frequency in the high beta band"},
                   "showlegend": False})

    #fig.write_image("PeakFrequencyOverTime.png",format="png", width=1000, height=600, scale=3)

    fig.show()