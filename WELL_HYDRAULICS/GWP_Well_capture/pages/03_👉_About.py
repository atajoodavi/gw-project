import streamlit as st

st.header('👉 About the WellCapture app')
st.markdown(
    """
    ### Description
    The WellCapture interactive tool calculates the capture area for a pumping well in a confined, homogeneous, isotropic aquifer.
    
    ### Development
    Innovative and digital learning and teaching materials are currently enhanced and transferred to various partners across Europe by the EU cooperation project [iNUX](https://www.gw-inux.org/). The iNUX project is funded by the ERASMUS+ program of the European Union.
    
    WellCapture was developed by Thomas Reimann as a Jupyter notebook and adapted to the Groundwater Project interactive education format. It was released in October of 2024.
    """
)

left_co2, cent_co2 = st.columns((20,60))
with left_co2:
    st.image('90_Streamlit_apps/GWP_Well_capture/assets/images/iNUX_wLogo.png')
with cent_co2:
    st.image('90_Streamlit_apps/GWP_Well_capture/assets/images/1200px-Erasmus+_Logo.svg.png')

st.markdown(
    """
    ### About the Developer
"""
)
left_co, cent_co = st.columns((20,60))
with left_co:
    st.image('90_Streamlit_apps/GWP_Well_capture/assets/images/thomasreimann.png')
with cent_co:
    st.markdown(
        """
        Thomas Reimann is a researcher and lecturer at the Institute for Groundwater Management at TU Dresden, Germany. With nearly 20 years of experience, Thomas’ work focus on groundwater engineering, often in combination with distributed numerical models in different environments, e.g., karst systems or open-pit mining for soft coal. He received a diploma in water management with a focus on groundwater engineering from TU Dresden in 2003. In 2012 he was promoted to Dr.-Ing. (Ph.D.) in groundwater management for research in karst systems by TU Dresden.
        
        Thomas is a specialist in applying and adapting distributed numerical models for use in research and industry. He enhanced the distributed numerical discrete-continuum model MODFLOW Conduit Flow Process (CFP) with various boundary conditions, as well as flow and transport processes. It is called CFPv2. Current research projects comprise Karst system characterization with inverse groundwater modeling, groundwater management in open-pit mining environments, and Managed Aquifer Recharge.
        
        Besides research, he has been actively teaching groundwater management and groundwater modeling since 2003 at Dresden University of Technology and as a guest lecturer for Hydrogeology since 2017 at the University of Gothenburg (Sweden). His ongoing teaching activities use various innovative digital methods to improve the learning process, which was honored by the Dresden University of Technology teaching award in 2017.
        
        """
    )
