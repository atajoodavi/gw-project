import streamlit as st

st.title('📃 Theory underlying WellCapture')

st.markdown(
    """
    ## The Conceptual Model for WellCapture
    A well capture zone (or capture zone) is an area within an aquifer that delineates groundwater that will ultimately reach the well. It is also referred to as the zone of contribution. In a contaminated aquifer, contamination within a well capture zone will eventually reach the well as presented conceptually in the figure below.
    
    The WellCapture interactive tool calculates the capture area for a pumping well in a confined, homogeneous, isotropic aquifer. The regional groundwater flow is directed along the x-axis with a hydraulic gradient i. Accordingly, the capture area of an ideal pumping well, situated at the coordinates (0,0) can be characterized by the culmination point and the maximum width of the zone within the flow divide.
"""
)
left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('90_Streamlit_apps/GWP_Well_capture/assets/images/wellcapturediagram-sm42.png', caption="Conceptual Diagram of a well capture zone; modified from Grubb(1993)")

st.markdown(
    """
    ## The Mathematical Model for WellCapture
    The full theoretical foundation for the computation can be found in a publication from Grubb (1993).
    
    The capture area of an ideal pumping well, situated at the coordinates (0,0) can be characterized by:
    - the culmination point _x0_, and
    - the maximum width of the zone within the flow divide, _B_
"""
)
st.latex(r'''x_0=\frac{Q}{2\pi Kib}''')
st.latex(r'''B=2y_{max}=\frac{Q}{Kib}''')
st.markdown(
    """
    The symbols are: _Q_ = pumping rate, _K_ = hydraulic conductivity, _i_ = hydrauic gradient, and _b_ = aquifer thickness.
    
    - each point on the flow divide can be calculated as:
"""
)

st.latex(r'''x=\frac{-y}{\tan (\frac{2 \pi Kiby}{Q})}''')

st.markdown(
    """
Grubb, S. (1993). Analytical Model for Estimation of Steady-State Capture Zones of Pumping Wells in Confined and Unconfined Aquifers. Groundwater, 31(1), 27-32. https://doi.org/10.1111/j.1745-6584.1993.tb00824.x

"""
)