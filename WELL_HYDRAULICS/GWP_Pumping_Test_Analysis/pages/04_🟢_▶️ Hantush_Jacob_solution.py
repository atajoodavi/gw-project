# Loading the required Python libraries
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import scipy.interpolate as interp
import math
import pandas as pd
import streamlit as st
import streamlit_book as stb
from streamlit_extras.stateful_button import button

# Authors, institutions, and year
year = 2025 
authors = {
    "Thomas Reimann": [1],  # Author 1 belongs to Institution 1
    "Eileen Poeter": [2],
}
institutions = {
    1: "TU Dresden, Institute for Groundwater Management",
    2: "Colorado School of Mines"
}
index_symbols = ["¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]
author_list = [f"{name}{''.join(index_symbols[i-1] for i in indices)}" for name, indices in authors.items()]
institution_list = [f"{index_symbols[i-1]} {inst}" for i, inst in institutions.items()]
institution_text = " | ".join(institution_list)

st.title('🟢 :green[Hantush-Jacob] parameter estimation')

st.header('for drawdown in :green[**leaky aquifers**]')
st.markdown("""
            This section uses the Hantush-Jacob solution for drawdown in response to pumping a :green[**leaky aquifer with no storage capacity**] to estimate Transmissivity, Storativity, and Aquitard Leakage.
            """) 
st.subheader(':green-background[Introduction]', divider="green")
st.markdown("""
            The Hantush-Jacob (1955) solution is intended to evaluate pumping tests in semiconfined settings with aquitards that store an insignificant volume of water.
            
            This application uses the Hantush-Jacob solution to estimate Transmissivity $T$ and  Storativity $S$ of an aquifer, as well as the leakage factor $r/B$ related to aquitard properties, from drawdown data collected during a pumping test.
            
            You can estimate $T$, $S$, and $r/B$ by adjusting a slider or by typing a number (depending on the toggle switch position) to modify the values of $T$, $S$, and $r/B$ until the measured data align with the Hantush-Jacob curve for the input parameters. 
            
            _B_ is a parameter that reflects the inverse of the potential for aquitard leakage _b'/K'_ relative to the ability of the aquifer to transmit groundwater laterally $T$. There is greater leakage potential for a smaller value of B which reflects a thinner aquitard of higher vertical hydraulic conductivity, that is, there is more potential leakage through an aquitard with a smaller ratio of _b'_ to _K'_. 
            
            """)      
                
st.latex(r'''B = \sqrt{\frac{Tb'}{K'}}''')

st.markdown("""
            The parameter used when matching data to the Hantush-Jacob Solution is $r/B$, where r is the distance of the observation well from the pumping well. Larger values of $r/B$ indicate more leakage because B is in the denominator.
            
            """)   
            
left_co, cent_co, last_co = st.columns((20,60,20))
with cent_co:
    st.image('WELL_HYDRAULICS/GWP_Pumping_Test_Analysis/assets/images/leaky_aquifer_2.png', caption="Cross section of a pumped leaky aquifer, with vertical arrows illustrating leakage is larger near the well where drawdown is larger and declines with distance from the well, Kruseman et al., 1994")
            
st.markdown("""
           Before investigating the Hantush-Jacob Solution it is useful to think about the questions provided in this initial assessment.
"""
)
# Initial assessment
   
with st.expander(":green[**Show/Hide the initial assessment**]"):
    columnsQ1 = st.columns((1,1))
    
    with columnsQ1[0]:
        stb.single_choice(":green[**What conditions are appropriate for use of the Hantush-Jacob Solution?**]",
                  ["Steady state flow, confined aquifer.", "Transient flow, confined aquifer", "Steady state flow, semiconfined aquifer",
                  "Transient flow, semiconfined aquifer", "Steady state flow, unconfined aquifer",
                  "Transient flow, unconfined aquifer"],
                  3,success='CORRECT! Hantush-Jacob is designed for transient flow in a semiconfined (i.e., leaky) aquifer', error='This is not correct ... You can learn more about the Hantush-Jacob Solution [by downloading the book: An Introduction to Hydraulic Testing in Hydrogeology - Basic Pumping, Slug, and Packer Methods​​ and reading Section 9 through 9.2](https://gw-project.org/books/an-introduction-to-hydraulic-testing-in-hydrogeology-basic-pumping-slug-and-packer-methods/). Feel free to answer again.')
                  
        stb.single_choice(":green[**What is the key difference between the Hantush-Jacob solution and the Theis solution?**]",
                  ["Theis solution applies to leaky aquifers, while Hantush-Jacob is for unconfined aquifers", "Hantush-Jacob solution accounts for leakage through an aquitard, while Theis assumes a fully confined aquifer", "Theis solution considers the presence of an impermeable boundary", "Hantush-Jacob solution applies only to steady-state conditions"],
                  1,success='CORRECT! Hantush-Jacob solution accounts for leakage through an aquitard, while Theis assumes a fully confined aquifer', error='This is not correct ... You can learn more about the Theis and Hantush-Jacob Solutions [by downloading the book: An Introduction to Hydraulic Testing in Hydrogeology - Basic Pumping, Slug, and Packer Methods​​ and reading Sections 8 and 9.2, respectively](https://gw-project.org/books/an-introduction-to-hydraulic-testing-in-hydrogeology-basic-pumping-slug-and-packer-methods/). Feel free to answer again.')
                  
        stb.single_choice(":green[**What parameter is introduced in the Hantush-Jacob solution to account for leakage?**]",
                  ["Storage coefficient", "Leakage factor (B)", "Specific yield", "Transmissivity"],
                  1,success='CORRECT! Leakage factor', error='This is not correct ... You can learn more about the Theis and Hantush-Jacob Solutions [by downloading the book: An Introduction to Hydraulic Testing in Hydrogeology - Basic Pumping, Slug, and Packer Methods​​ and reading Sections 8 and 9 through 9.2, respectively](https://gw-project.org/books/an-introduction-to-hydraulic-testing-in-hydrogeology-basic-pumping-slug-and-packer-methods/). Feel free to answer again.')                     
    with columnsQ1[1]:      
        stb.single_choice(":green[**Which of the following best defines the leakage factor B in the Hantush-Jacob solution?**]",
                  ["A measure of the storage capacity of the aquifer", "A parameter that describes the rate at which water moves through the aquifer", "A term that quantifies how much water leaks through an aquitard into the aquifer", "A constant value independent of aquifer properties"],
                  2,success='CORRECT! A term that quantifies how readily water leaks through an aquitard into an aquifer', error='This is not correct ... You can learn more about the Hantush-Jacob Solution [by downloading the book: An Introduction to Hydraulic Testing in Hydrogeology - Basic Pumping, Slug, and Packer Methods​​ and reading Section 9.2](https://gw-project.org/books/an-introduction-to-hydraulic-testing-in-hydrogeology-basic-pumping-slug-and-packer-methods/). Feel free to answer again.')
                  
        stb.single_choice(":green[**What happens to drawdown in a leaky confined aquifer compared to a fully confined aquifer?**]",
                  ["Drawdown decreases more rapidly in a leaky aquifer", "Drawdown is less in a leaky aquifer due to the additional water source", "Drawdown remains the same in both cases", "Drawdown is greater in a leaky aquifer due to the additional water source", "Drawdown occurs only in the aquitard, not in the aquifer"],
                  1,success='CORRECT! Drawdown is less in a leaky aquifer due to the additional water source', error='This is not correct ... You can learn more about the Theis and Hantush-Jacob Solutions [by downloading the book: An Introduction to Hydraulic Testing in Hydrogeology - Basic Pumping, Slug, and Packer Methods​​ and reading Sections 8 and 9 through 9.2, respectively](https://gw-project.org/books/an-introduction-to-hydraulic-testing-in-hydrogeology-basic-pumping-slug-and-packer-methods/). Feel free to answer again.')                     

        stb.single_choice(":green[**How does the Hantush-Jacob solution represent storage in the aquitard?**]",
                  ["Aquitard storage is ignored", "Aquitard storage controls the rate of leakage", "Aquitard storage controls the timing of leakage"],
                  0,success='CORRECT! The Hantush-Jacob solution assumes there is no water stored in the aquitard. Water flows through the aquitard from another aquifer.', error='This is not correct ... You can learn more about the Hantush-Jacob Solution by reviewing the Introduction to this section or [by downloading the book: An Introduction to Hydraulic Testing in Hydrogeology - Basic Pumping, Slug, and Packer Methods​​ and reading Section 9](https://gw-project.org/books/an-introduction-to-hydraulic-testing-in-hydrogeology-basic-pumping-slug-and-packer-methods/). Feel free to answer again.')                     
"---"

# Optional theory here
st.subheader(':green-background[Underlying theory] - The Hantush-Jacob Solution for Pumping Test Evaluation', divider="green")
st.markdown("""       
            The Hantush-Jacob solution extends the Theis solution to account for leaky confined aquifers, where vertical leakage from an overlying or underlying aquifer flows through an aquitard, contributing to flow that moves toward a well in the pumped aquifer. This approach is useful when an aquifer is semi-confined rather than perfectly confined.
            """)
# Optional theory here
with st.expander('**Click here for more information** about the underlying theory of the :green[**Hantush-Jacob Solution**]'):
    st.markdown("""        
            The drawdown _s_ at a distance $r$ from a well pumping at a constant rate _Q_ is given by:
            """)
            
    st.latex(r'''s(r,t) = \frac{Q}{4\pi T} W(u, r/B)''')

    st.markdown(
            """
            where:
            - $s$ is drawdown at time $t$ and distance $r$ from the well
            - $T$ is the transmissivity of the aquifer
            - $W(u, r/B)$ is the Hantush leaky well function
            - $u$ is a dimensionless time parameter, given by:
            """)
            
    st.latex(r'''u = \frac{r^2 S}{4 T t}''')
            
    st.markdown(
            """
            - $S$ is the storativity (specific storage times aquifer thickness)
            - $t$ is the time since pumping began
            - $B$ is the leakage factor, defined as:
            
            """)
            
    st.latex(r'''B = \sqrt{\frac{T b'}{K'}}''')

    st.markdown(
            """
            where:
            - $b′$ is the thickness of the aquitard
            - $K′$ is the vertical hydraulic conductivity of the aquitard
            
            The well function $W(u, r/B)$ is computed as:
            """)

    st.latex(r'''W \left (u, \left (\frac{r}{B}  \right ) \right )  = \int_u^{\infty} \frac{e^{ -x - \frac{1}{4x} (\frac{r}{B})^2} }{x} dx''')

    st.markdown(
            """
            This solution is commonly used in pumping test analysis when leakage from an aquitard significantly affects the drawdown behavior, making it more gradual compared to the purely confined case described by the Theis solution.
            """)

"---" 
          
# Computation
# (Here the necessary functions like the well function $W(u)$ are defined. Later, those functions are used in the computation)
# Define a function, class, and object for Theis Well analysis

def well_function(u):
    return scipy.special.exp1(u)
    
def theis_u(T,S,r,t):
    u = r ** 2 * S / 4. / T / t
    return u
    
def Hantush_s(Q, T, u, u_HAN, w_u_HAN,r_div_B):
    #Interpolate for discrete w_u_HAN
    if r_div_B in [0, 1]:
        method = 'nearest'
    else:
        method = 'linear'
    w_u_HAN_interpolated = interp.interp1d(u_HAN, w_u_HAN[:, r_div_B], kind=method, fill_value="extrapolate")
    s = Q / 4. / np.pi / T * w_u_HAN_interpolated(u)
    return s
    
def compute_s(T, S, t, Q, r, u_HAN, w_u_HAN, r_div_B):
    u = theis_u(T, S, r, t)
    s = Hantush_s(Q, T, u, u_HAN, w_u_HAN,r_div_B)
    return s

def compute_statistics(measured, computed):
    # Calculate the number of values
    n = len(measured)

    # Initialize a variable to store the sum of squared differences
    total_me = 0
    total_mae = 0
    total_rmse = 0

    # Loop through each value
    for i in range(n): # Add the squared difference to the total
        total_me   += (computed[i] - measured[i])
        total_mae  += (abs(computed[i] - measured[i]))
        total_rmse += (computed[i] - measured[i])**2

    # Calculate the me, mae, mean squared error
    me = total_me / n
    mae = total_mae / n
    meanSquaredError = total_rmse / n

    # Raise the mean squared error to the power of 0.5 
    rmse = (meanSquaredError) ** (1/2)
    return me, mae, rmse
    
# Callback function to update session state
def update_T(v):
    st.session_state[f"T_slider_value_{v}"] = st.session_state[f"T_input_{v}"]
def update_S(v):
    st.session_state[f"S_slider_value_{v}"] = st.session_state[f"S_input_{v}"]
    
# Initialize session state for value and toggle state
st.session_state.number_input = False  # Default to number_input

# (Here, the method computes the data for the well function. Those data can be used to generate a type curve.)
u_min = -5
u_max = 4

u = np.logspace(u_min,u_max)
u_inv = 1/u
w_u = well_function(u)

u_HAN = np.array([1.00E-05, 2.00E-05, 4.00E-05, 6.00E-05, 1.00E-04, 2.00E-04, 4.00E-04, 6.00E-04, 1.00E-03, 2.00E-03, 4.00E-03, 6.00E-03, 1.00E-02, 2.00E-02, 4.00E-02, 6.00E-02, 1.00E-01, 2.00E-01, 4.00E-01, 6.00E-01, 1 , 2])

t_HAN     = [0]*len(u_HAN)
s_HAN     = [0]*len(u_HAN)
u_inv_HAN = [0]*len(u_HAN)

for x in range(0,len(u_HAN)):
        u_inv_HAN[x] = 1/u_HAN[x]

# Hantush Jacob type curve data from tables

w_u_HAN = [[9.420E+00, 6.670E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.300E+00, 6.670E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.010E+00, 6.670E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [8.770E+00, 6.670E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [8.400E+00, 6.670E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [7.820E+00, 6.620E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [7.190E+00, 6.450E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [6.800E+00, 6.270E+00, 4.850E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [6.310E+00, 5.970E+00, 4.830E+00, 3.510E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 5.450E+00, 4.710E+00, 3.500E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 4.850E+00, 4.420E+00, 3.480E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 4.480E+00, 4.180E+00, 3.430E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 4.000E+00, 3.810E+00, 3.290E+00, 2.230E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 3.340E+00, 3.240E+00, 2.950E+00, 2.180E+00, 1.550E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 9.990E+02, 2.630E+00, 2.480E+00, 2.020E+00, 1.520E+00, 8.420E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 9.990E+02, 2.260E+00, 2.170E+00, 1.850E+00, 1.460E+00, 8.390E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 9.990E+02, 1.800E+00, 1.750E+00, 1.560E+00, 1.310E+00, 8.190E-01, 4.271E-01, 2.280E-01, 1.174E-01],
           [9.990E+02, 9.990E+02, 9.990E+02, 1.190E+00, 1.110E+00, 9.960E-01, 7.150E-01, 4.100E-01, 2.270E-01, 1.174E-01],
           [9.990E+02, 9.990E+02, 9.990E+02, 6.930E-01, 6.650E-01, 6.210E-01, 5.020E-01, 3.400E-01, 2.100E-01, 1.174E-01],
           [9.990E+02, 9.990E+02, 9.990E+02, 4.500E-01, 4.360E-01, 4.150E-01, 3.540E-01, 2.550E-01, 1.770E-01, 1.100E-01],
           [9.990E+02, 9.990E+02, 9.990E+02, 9.990E+02, 2.130E-01, 2.060E-01, 1.850E-01, 1.509E-01, 1.140E-01, 8.030E-02],
           [9.990E+02, 9.990E+02, 9.990E+02, 9.990E+02, 9.990E+02, 4.700E-02, 4.400E-02, 9.990E+02, 3.400E-02, 2.500E-02]]

w_u_HAN = np.array(w_u_HAN)

st.subheader(':green[Estimate $T$, $S$, and Leakage Factor $r/B$ by matching a Hantush-Jacob Curve to measured drawdown data]', divider="rainbow")

st.markdown("""
            In this section, you can **adjust the values of transmissivity, storativity, and $r/B$ until the curve of drawdown versus time that is calculated and plotted on the graph matches the measured data from the Varnum test site in Sweden**. A close match indicates that the selected values are a reasonable representation of the aquifer properties. The measured data were collected during a field course for the GVG460 course at the [University of Gothenburg](https://www.gu.se/en/earth-sciences).
            
            The aquifer is 9 meters thick and is overlain by an 11-meters thick aquitard that separates the lower Varnum Aquifer from an overlying aquifer. When the lower aquifer is pumped, water leaks downward from the overlying aquifer in response to the lowered head in the deeper aquifer.
        
            After estimating the parameter values that result in a good fit of the Hantush-Jacob curve to the data, and knowing the thickness of the aquitard, the vertical hydraulic conductivity of the aquitard is calculated.
            
            Additionally, you can **switch between a log-log and a semi-log plot** to analyze the effect of transmissivity, storativity, and $r/B$ on the drawdown behavior. The semi-log plot is useful for visualizing that late-time drawdown-versus-time data from a semiconfined aquifer form a straight line on a semi-log graph before leakage from adjacent layers becomes significant.
            
            More precise matching can be achieved by **zooming in** and/or by using **typed number input rather than slider input**. Both are selected with a toggle switch.
            
            The **scatter plot** can be turned on by using a toggle switch. It provides a visual comparison of the data and the fitted curve. A 45 degree line indicates a perfect match between the measured drawdowns and those calculated by the Hantush-Jacob solution for the input values of $T$, $S$, and $r/B$.
"""
)

@st.fragment
def inverse(v):
    # This is the function to plot the graph with the data 
    
    Pirna = False
    
    if f"T_slider_value_{v}" not in st.session_state:
        st.session_state[f"T_slider_value_{v}"] = -3.0  # Default value (log of T)
    if f"S_slider_value_{v}" not in st.session_state:
        st.session_state[f"S_slider_value_{v}"] = -4.0  # Default value (log of S)
        
    # Get input data
    # Define the minimum and maximum for the logarithmic scale
    log_min1 = -7.0 # T / Corresponds to 10^-7 = 0.0000001
    log_max1 = 0.0  # T / Corresponds to 10^0 = 1
    log_min2 = -7.0 # S / Corresponds to 10^-7 = 0.0000001
    log_max2 = 0.0  # S / Corresponds to 10^0 = 1
    
    # Toggle to switch between slider and number-input mode
    st.session_state.number_input = st.toggle("Toggle to use Slider or Number for input of $T$ and $S$", key = 10+v)
   
    columns2 = st.columns((1,1), gap = 'large')
    with columns2[0]:
        semilog = st.toggle("Toggle for **semi log graph**", key = 15+v)
        refine_plot = st.toggle("**Zoom in** on the **data in the graph**", key = 20+v)
        scatter = st.toggle('Show scatter plot', key = 30+v)
        if v==2:
            Pirna = True
    with columns2[1]:
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR TRANSMISSIVITY
        container = st.container()
        if st.session_state.number_input:
            T_slider_value_new = st.number_input("_(log of) Transmissivity in m²/s_", log_min1,log_max1, st.session_state[f"T_slider_value_{v}"], 0.01, format="%4.2f", key=f"T_input_{v}", on_change=update_T,args=(v,))
        else:
            T_slider_value_new = st.slider("_(log of) Transmissivity in m²/s_", log_min1,log_max1, st.session_state[f"T_slider_value_{v}"], 0.01, format="%4.2f", key=f"T_input_{v}", on_change=update_T,args=(v,))
        T = 10 ** T_slider_value_new
        container.write("**Transmissivity in m²/s**: %5.2e" %T)
        # READ LOG VALUE, CONVERT, AND WRITE VALUE FOR STORATIVITY
        container = st.container()
        if st.session_state.number_input:
            S_slider_value_new=st.number_input('_(log of) Storativity_', log_min2,log_max2,st.session_state[f"S_slider_value_{v}"],0.01,format="%4.2f", key=f"S_input_{v}", on_change=update_S,args=(v,))
        else:
            S_slider_value_new=st.slider('_(log of) Storativity_', log_min2,log_max2,st.session_state[f"S_slider_value_{v}"],0.01,format="%4.2f", key=f"S_input_{v}", on_change=update_S,args=(v,))
        S = 10 ** S_slider_value_new
        container.write("**Storativity (dimensionless)**: %5.2e" %S)
        # r/B
        r_div_B_choice = st.selectbox("$r/B$",('0.01', '0.04', '0.1', '0.2', '0.4', '0.6', '1', '1.5', '2', '2.5'), key = 60+v,)
        r_div_B_list = ['0.01', '0.04', '0.1', '0.2', '0.4', '0.6', '1', '1.5', '2', '2.5']
        r_div_B = r_div_B_list.index(r_div_B_choice)
    
    # Select data
     # Drawdown data from Varnum 2016 / R12 
    #R12\n",
    m_time =  [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325] # time in minutes\n",
    m_ddown = [2E-05,0.02022,0.04591,0.0716,0.09342,0.11433,0.12882,0.14332,0.15139,0.16313,0.17396,0.18203,0.18827,0.1936,0.19878,0.2012,0.20729,0.21247,0.21489,0.22007,0.22249,0.22583,0.22826,0.23068,0.23358,0.23648,0.23938,0.24228,0.24243,0.24533,0.24915,0.2493,0.2522,0.25235,0.2551,0.2551,0.25785,0.25785,0.2606,0.2606,0.26335,0.26335,0.2661,0.2661,0.26597,0.26585,0.26847,0.2656,0.26822,0.27177,0.26797,0.27152,0.27139,0.27402,0.27397,0.27392,0.27387,0.27382,0.27652,0.27647,0.27642,0.27637,0.27907,0.27627,0.27614,0.27877,0.27589,0.27577,0.27839,0.27735,0.27814,0.2771,0.28064,0.2796,0.27712,0.2774,0.28042,0.27795,0.27822,0.2785,0.28152,0.27905,0.28207,0.28235,0.28307,0.28012,0.28175,0.2843,0.2841,0.28482,0.28462,0.28442,0.28422,0.28402,0.28404,0.28407,0.28684,0.28412,0.28689,0.28692,0.28694,0.28422,0.28699,0.28702,0.28717,0.28732,0.28747,0.28762,0.28777,0.28792,0.28807,0.28822,0.28837,0.28852,0.29144,0.28887,0.29179,0.28922,0.28939,0.28957,0.28974,0.28992,0.29009,0.29027,0.28994,0.29237,0.28929,0.29172,0.29139,0.29107,0.29074,0.29042,0.29009,0.28977,0.28974,0.28972,0.28969,0.29333,0.28964,0.28687,0.28959,0.29323,0.28954,0.28952,0.29336,0.29353,0.29371,0.29022,0.29406,0.29423,0.29441,0.29458,0.29109,0.29493,0.29488,0.29483,0.29478,0.29473,0.29468,0.29463,0.29458,0.29453,0.29723,0.29718,0.29443,0.29443,0.29443,0.29443,0.29443,0.29718,0.29443,0.29443,0.29443,0.29718,0.29701,0.29683,0.29666,0.29648,0.29631,0.29613,0.29596,0.29578,0.29561,0.29543,0.29561,0.29853,0.29596,0.29613,0.29631,0.29648,0.29666,0.29683,0.29701,0.29993,0.29688,0.29658,0.29628,0.29598,0.29568,0.29538,0.29508,0.29478,0.29723,0.29693,0.29418,0.29418,0.29418,0.29418,0.29693,0.29693,0.29418,0.29418,0.29693,0.29418,0.29433,0.29723,0.29738,0.29478,0.29768,0.29783,0.29798,0.29813,0.29828,0.29843,0.29838,0.29833,0.29828,0.29823,0.29818,0.29813,0.29808,0.29803,0.29798,0.29793,0.29796,0.29798,0.29801,0.29803,0.30081,0.30083,0.29811,0.29813,0.29816,0.30093,0.29853,0.29888,0.29923,0.29958,0.29993,0.30303,0.30338,0.30098,0.30133,0.30168,0.30408,0.30098,0.30063,0.30303,0.29993,0.30233,0.29923,0.29888,0.29853,0.29818,0.30113,0.30133,0.29878,0.29898,0.30193,0.30213,0.30233,0.30253,0.30273,0.30018,0.30001,0.30258,0.30241,0.29948,0.29931,0.29913,0.30171,0.29878,0.29861,0.29843,0.30133,0.29873,0.29888,0.29903,0.29918,0.29933,0.29948,0.29963,0.30253,0.29993,0.30011,0.30028,0.30046,0.30063,0.30081,0.30373,0.30391,0.30133,0.30151,0.30443,0.30151,0.30133,0.30116,0.30098,0.30081,0.30338,0.30046,0.30028,0.30286,0.29993,0.30286,0.30303,0.30321,0.30338,0.30356,0.30373,0.30391,0.30408,0.30426,0.30443,0.30408] # drawdown in meters\n",
    r = 38.9     # m
    b = 9       # m
    b2 = 11      # m aquitard 
    Qs = 0.01317   # m^3/s
    Qd = Qs*60*60*24 # m^3/d

    if Pirna:
        # Drawdown data from Pirna24 exercise and parameters
        m_time = [1, 2, 2, 4, 5, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970, 971, 972, 973, 974, 975, 976, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992, 993, 994, 995, 996, 997, 998, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1127, 1128, 1129, 1130, 1131, 1132, 1133, 1134, 1135, 1136, 1137, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1145, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1171, 1172, 1173, 1174, 1175, 1176, 1177, 1178, 1179, 1180, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1189, 1190, 1191, 1192, 1193, 1194, 1195, 1196, 1197, 1198, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1209, 1210, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1218, 1219, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1239, 1240, 1241, 1242, 1243, 1244, 1245, 1246, 1247, 1248, 1249, 1250, 1251, 1252, 1253, 1254, 1255, 1256, 1257, 1258, 1259, 1260, 1261, 1262, 1263, 1264, 1265, 1266, 1267, 1268, 1269, 1270, 1271, 1272, 1273, 1274, 1275, 1276, 1277, 1278, 1279, 1280, 1281, 1282, 1283, 1284, 1285, 1286, 1287, 1288, 1289, 1290, 1291, 1292, 1293, 1294, 1295, 1296, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1304, 1305, 1306, 1307, 1308, 1309, 1310, 1311, 1312, 1313, 1314, 1315, 1316, 1317, 1318, 1319, 1320, 1321, 1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329, 1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352, 1353, 1354, 1355, 1356, 1357, 1358, 1359, 1360, 1361, 1362, 1363, 1364, 1365, 1366, 1367, 1368, 1369, 1370, 1371, 1372, 1373, 1374, 1375, 1376, 1377, 1378, 1379, 1380, 1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, 1390, 1391, 1392, 1393, 1394, 1395, 1396, 1397, 1398, 1399, 1400, 1401, 1402, 1403, 1404, 1405, 1406, 1407, 1408, 1409, 1410, 1411, 1412, 1413, 1414, 1415, 1416, 1417, 1418, 1419, 1420, 1421, 1422, 1423, 1424, 1425, 1426, 1427, 1428, 1429, 1430, 1431, 1432, 1433, 1434, 1435, 1436, 1437, 1438, 1439, 1440, 1441, 1442, 1443, 1444, 1445, 1446, 1447, 1448, 1449, 1450, 1451, 1452, 1453, 1454, 1455, 1456, 1457, 1458, 1459, 1460, 1461, 1462, 1463, 1464, 1465, 1466, 1467, 1468, 1469, 1470, 1471, 1472, 1473, 1474, 1475, 1476, 1477, 1478, 1479, 1480, 1481, 1482, 1483, 1484, 1485, 1486, 1487, 1488, 1489, 1490, 1491, 1492, 1493, 1494, 1495, 1496, 1497, 1498, 1499, 1500, 1501, 1502, 1503, 1504, 1505, 1506, 1507, 1508, 1509, 1510, 1511, 1512, 1513, 1514, 1515, 1516, 1517, 1518, 1519, 1520, 1521, 1522, 1523, 1524, 1525, 1526, 1527, 1528, 1529, 1530, 1531, 1532, 1533, 1534, 1535, 1536, 1537, 1538, 1539, 1540, 1541, 1542, 1543, 1544, 1545, 1546, 1547, 1548, 1549, 1550, 1551, 1552, 1553, 1554, 1555, 1556, 1557, 1558, 1559, 1560, 1561, 1562, 1563, 1564, 1565, 1566, 1567, 1568, 1569, 1570, 1571, 1572, 1573, 1574, 1575, 1576, 1577, 1578, 1579, 1580, 1581, 1582, 1583, 1584, 1585, 1586, 1587, 1588, 1589, 1590, 1591, 1592, 1593, 1594, 1595, 1596, 1597, 1598, 1599, 1600, 1601, 1602, 1603, 1604, 1605, 1606, 1607, 1608, 1609, 1610, 1611, 1612, 1613, 1614, 1615, 1616, 1617, 1618, 1619, 1620, 1621, 1622, 1623, 1624, 1625, 1626, 1627, 1628, 1629, 1630, 1631, 1632, 1633, 1634, 1635, 1636, 1637, 1638, 1639, 1640, 1641, 1642, 1643, 1644, 1645, 1646, 1647, 1648, 1649, 1650, 1651, 1652, 1653, 1654, 1655, 1656, 1657, 1658, 1659, 1660, 1661, 1662, 1663, 1664, 1665, 1666, 1667, 1668, 1669, 1670, 1671, 1672, 1673, 1674, 1675, 1676, 1677, 1678, 1679, 1680, 1681, 1682, 1683, 1684, 1685, 1686, 1687, 1688, 1689, 1690, 1691, 1692, 1693, 1694, 1695, 1696, 1697, 1698, 1699, 1700, 1701, 1702, 1703, 1704, 1705, 1706, 1707, 1708, 1709, 1710, 1711, 1712, 1713, 1714, 1715, 1716, 1717, 1718, 1719, 1720, 1721, 1722, 1723, 1724, 1725, 1726, 1727, 1728, 1729, 1730, 1731, 1732, 1733, 1734, 1735, 1736, 1737, 1738, 1739, 1740, 1741, 1742, 1743, 1744, 1745, 1746, 1747, 1748, 1749, 1750, 1751, 1752, 1753, 1754, 1755, 1756, 1757, 1758, 1759, 1760, 1761, 1762, 1763, 1764, 1765, 1766, 1767, 1768, 1769, 1770, 1771, 1772, 1773, 1774, 1775, 1776, 1777, 1778, 1779, 1780, 1781, 1782, 1783, 1784, 1785, 1786, 1787, 1788, 1789, 1790, 1791, 1792, 1793, 1794, 1795, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1803, 1804, 1805, 1806, 1807, 1808, 1809, 1810, 1811, 1812, 1813, 1814, 1815, 1816, 1817, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825, 1826, 1827, 1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1839, 1840, 1841, 1842, 1843, 1844, 1845, 1846, 1847, 1848, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040, 2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050, 2051, 2052, 2053, 2054, 2055, 2056, 2057, 2058, 2059, 2060, 2061, 2062, 2063, 2064, 2065, 2066, 2067, 2068, 2069, 2070, 2071, 2072, 2073, 2074, 2075, 2076, 2077, 2078, 2079, 2080, 2081, 2082, 2083, 2084, 2085, 2086, 2087, 2088, 2089, 2090, 2091, 2092, 2093, 2094, 2095, 2096, 2097, 2098, 2099, 2100, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2111, 2112, 2113, 2114, 2115, 2116, 2117, 2118, 2119, 2120, 2121, 2122, 2123, 2124, 2125, 2126, 2127, 2128, 2129, 2130, 2131, 2132, 2133, 2134, 2135, 2136, 2137, 2138, 2139, 2140, 2141, 2142, 2143, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2151, 2152, 2153, 2154, 2155, 2156, 2157, 2158, 2159, 2160, 2161, 2162, 2163, 2164, 2165, 2166, 2167, 2168, 2169, 2170, 2171, 2172, 2173, 2174, 2175, 2176, 2177, 2178, 2179, 2180, 2181, 2182, 2183, 2184, 2185, 2186, 2187, 2188, 2189, 2190, 2191, 2192, 2193, 2194, 2195, 2196, 2197, 2198, 2199, 2200, 2201, 2202, 2203, 2204, 2205, 2206, 2207, 2208, 2209, 2210, 2211, 2212, 2213, 2214, 2215, 2216, 2217, 2218, 2219, 2220, 2221, 2222, 2223, 2224, 2225, 2226, 2227, 2228, 2229, 2230, 2231, 2232, 2233, 2234, 2235, 2236, 2237, 2238, 2239, 2240, 2241, 2242, 2243, 2244, 2245, 2246, 2247, 2248, 2249, 2250, 2251, 2252, 2253, 2254, 2255, 2256, 2257, 2258, 2259, 2260, 2261, 2262, 2263, 2264, 2265, 2266, 2267, 2268, 2269, 2270, 2271, 2272, 2273, 2274, 2275, 2276, 2277, 2278, 2279, 2280, 2281, 2282, 2283, 2284, 2285, 2286, 2287, 2288, 2289, 2290, 2291, 2292, 2293, 2294, 2295, 2296, 2297, 2298, 2299, 2300, 2301, 2302, 2303, 2304, 2305, 2306, 2307, 2308, 2309, 2310, 2311, 2312, 2313, 2314, 2315, 2316, 2317, 2318, 2319, 2320, 2321, 2322, 2323, 2324, 2325, 2326, 2327, 2328, 2329, 2330, 2331, 2332, 2333, 2334, 2335, 2336, 2337, 2338, 2339, 2340, 2341, 2342, 2343, 2344, 2345, 2346, 2347, 2348, 2349, 2350, 2351, 2352, 2353, 2354, 2355, 2356, 2357, 2358, 2359, 2360, 2361, 2362, 2363, 2364, 2365, 2366, 2367, 2368, 2369, 2370, 2371, 2372, 2373, 2374, 2375, 2376, 2377, 2378, 2379, 2380, 2381, 2382, 2383, 2384, 2385, 2386, 2387, 2388, 2389, 2390, 2391, 2392, 2393, 2394, 2395, 2396, 2397, 2398, 2399, 2400, 2401, 2402, 2403, 2404, 2405, 2406, 2407, 2408, 2409, 2410, 2411, 2412, 2413, 2414, 2415, 2416, 2417, 2418, 2419, 2420, 2421, 2422, 2423, 2424, 2425, 2426, 2427, 2428, 2429, 2430, 2431, 2432, 2433, 2434, 2435, 2436, 2437, 2438, 2439, 2440, 2441, 2442, 2443, 2444, 2445, 2446, 2447, 2448, 2449, 2450, 2451, 2452, 2453, 2454, 2455, 2456, 2457, 2458, 2459, 2460, 2461, 2462, 2463, 2464, 2465, 2466, 2467, 2468, 2469, 2470, 2471, 2472, 2473, 2474, 2475, 2476, 2477, 2478, 2479, 2480, 2481, 2482, 2483, 2484, 2485, 2486, 2487, 2488, 2489, 2490, 2491, 2492, 2493, 2494, 2495, 2496, 2497, 2498, 2499, 2500, 2501, 2502, 2503, 2504, 2505, 2506, 2507, 2508, 2509, 2510, 2511, 2512, 2513, 2514, 2515, 2516, 2517, 2518, 2519, 2520, 2521, 2522, 2523, 2524, 2525, 2526, 2527, 2528, 2529, 2530, 2531, 2532, 2533, 2534, 2535, 2536, 2537, 2538, 2539, 2540, 2541, 2542, 2543, 2544, 2545, 2546, 2547, 2548, 2549, 2550, 2551, 2552, 2553, 2554, 2555, 2556, 2557, 2558, 2559, 2560, 2561, 2562, 2563, 2564, 2565, 2566, 2567, 2568, 2569, 2570, 2571, 2572, 2573, 2574, 2575, 2576, 2577, 2578, 2579, 2580, 2581, 2582, 2583, 2584, 2585, 2586, 2587, 2588, 2589, 2590, 2591, 2592, 2593, 2594, 2595, 2596, 2597, 2598, 2599, 2600, 2601, 2602, 2603, 2604, 2605, 2606, 2607, 2608, 2609, 2610, 2611, 2612, 2613, 2614, 2615, 2616, 2617, 2618, 2619, 2620, 2621, 2622, 2623, 2624, 2625, 2626, 2627, 2628, 2629, 2630, 2631, 2632, 2633, 2634, 2635, 2636, 2637, 2638, 2639, 2640, 2641, 2642, 2643, 2644, 2645, 2646, 2647, 2648, 2649, 2650, 2651, 2652, 2653, 2654, 2655, 2656, 2657, 2658, 2659, 2660, 2661, 2662, 2663, 2664, 2665, 2666, 2667, 2668, 2669, 2670, 2671, 2672, 2673, 2674, 2675, 2676, 2677, 2678, 2679, 2680, 2681, 2682, 2683, 2684, 2685, 2686, 2687, 2688, 2689, 2690, 2691, 2692, 2693, 2694, 2695, 2696, 2697, 2698, 2699, 2700, 2701, 2702, 2703, 2704, 2705, 2706, 2707, 2708, 2709, 2710, 2711, 2712, 2713, 2714, 2715, 2716, 2717, 2718, 2719, 2720, 2721, 2722, 2723, 2724, 2725, 2726, 2727, 2728, 2729, 2830, 2831, 2832, 2833, 2834, 2835, 2836, 2837, 2838, 2839, 2840, 2841, 2842, 2843, 2844, 2845, 2846, 2847, 2848, 2849, 2850, 2851, 2852, 2853, 2854, 2855, 2856, 2857, 2858, 2859, 2860, 2861, 2862, 2863, 2864, 2865, 2866, 2867, 2868, 2869, 2870, 2871, 2872, 2873, 2874, 2875, 2876, 2877, 2878, 2879, 2880, 2881, 2882, 2883, 2884, 2885, 2886, 2887, 2888, 2889, 2890, 2891, 2892, 2893, 2894, 2895, 2896, 2897, 2898, 2899, 2900, 2901, 2902, 2903, 2904, 2905, 2906, 2907, 2908, 2909, 2910, 2911, 2912, 2913, 2914, 2915, 2916, 2917, 2918, 2919, 2920, 2921, 2922, 2923, 2924, 2925, 2926, 2927, 2928, 2929, 2930, 2931]
        m_ddown = [0.038, 0.043, 0.045, 0.046, 0.047, 0.048, 0.048, 0.049, 0.049, 0.05, 0.05, 0.051, 0.051, 0.051, 0.051, 0.052, 0.052, 0.052, 0.053, 0.053, 0.053, 0.054, 0.054, 0.054, 0.054, 0.055, 0.055, 0.055, 0.055, 0.056, 0.056, 0.056, 0.056, 0.057, 0.057, 0.057, 0.057, 0.057, 0.058, 0.058, 0.058, 0.058, 0.058, 0.059, 0.059, 0.059, 0.06, 0.059, 0.06, 0.06, 0.06, 0.06, 0.061, 0.061, 0.061, 0.061, 0.062, 0.062, 0.062, 0.062, 0.063, 0.063, 0.063, 0.063, 0.063, 0.064, 0.064, 0.064, 0.064, 0.064, 0.064, 0.065, 0.065, 0.065, 0.065, 0.065, 0.065, 0.066, 0.066, 0.066, 0.066, 0.066, 0.067, 0.067, 0.067, 0.067, 0.068, 0.068, 0.068, 0.068, 0.068, 0.069, 0.069, 0.069, 0.069, 0.069, 0.069, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.07, 0.071, 0.071, 0.071, 0.071, 0.071, 0.071, 0.071, 0.072, 0.072, 0.072, 0.072, 0.072, 0.073, 0.073, 0.073, 0.073, 0.073, 0.073, 0.073, 0.074, 0.074, 0.074, 0.074, 0.074, 0.074, 0.075, 0.075, 0.075, 0.075, 0.075, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076, 0.076, 0.077, 0.077, 0.077, 0.077, 0.077, 0.077, 0.077, 0.077, 0.078, 0.078, 0.078, 0.078, 0.078, 0.078, 0.078, 0.078, 0.079, 0.079, 0.079, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.081, 0.081, 0.081, 0.081, 0.081, 0.081, 0.081, 0.081, 0.082, 0.082, 0.082, 0.082, 0.082, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.084, 0.084, 0.084, 0.084, 0.084, 0.084, 0.084, 0.085, 0.084, 0.085, 0.085, 0.085, 0.085, 0.085, 0.085, 0.085, 0.086, 0.086, 0.086, 0.086, 0.086, 0.086, 0.086, 0.086, 0.086, 0.087, 0.087, 0.087, 0.087, 0.087, 0.088, 0.088, 0.088, 0.088, 0.088, 0.088, 0.088, 0.088, 0.089, 0.089, 0.088, 0.089, 0.089, 0.089, 0.089, 0.089, 0.089, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.091, 0.091, 0.091, 0.091, 0.091, 0.091, 0.091, 0.091, 0.091, 0.092, 0.092, 0.092, 0.092, 0.092, 0.092, 0.092, 0.093, 0.093, 0.093, 0.093, 0.093, 0.093, 0.093, 0.094, 0.094, 0.094, 0.094, 0.094, 0.094, 0.094, 0.094, 0.094, 0.094, 0.094, 0.095, 0.095, 0.095, 0.095, 0.095, 0.095, 0.095, 0.096, 0.096, 0.096, 0.096, 0.096, 0.096, 0.096, 0.096, 0.096, 0.097, 0.097, 0.097, 0.097, 0.097, 0.097, 0.097, 0.097, 0.097, 0.097, 0.097, 0.098, 0.098, 0.098, 0.098, 0.098, 0.098, 0.098, 0.099, 0.099, 0.099, 0.099, 0.099, 0.099, 0.099, 0.099, 0.099, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.101, 0.101, 0.101, 0.101, 0.101, 0.101, 0.101, 0.101, 0.102, 0.102, 0.102, 0.102, 0.102, 0.102, 0.102, 0.102, 0.102, 0.102, 0.103, 0.103, 0.103, 0.103, 0.103, 0.103, 0.103, 0.103, 0.104, 0.104, 0.104, 0.104, 0.104, 0.104, 0.104, 0.104, 0.104, 0.104, 0.104, 0.105, 0.105, 0.105, 0.105, 0.105, 0.105, 0.105, 0.105, 0.105, 0.105, 0.106, 0.106, 0.106, 0.106, 0.106, 0.106, 0.106, 0.106, 0.107, 0.107, 0.107, 0.107, 0.107, 0.107, 0.107, 0.107, 0.107, 0.107, 0.108, 0.108, 0.108, 0.108, 0.108, 0.108, 0.108, 0.108, 0.108, 0.108, 0.109, 0.109, 0.109, 0.109, 0.109, 0.109, 0.109, 0.109, 0.109, 0.109, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.11, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.111, 0.112, 0.112, 0.112, 0.112, 0.112, 0.112, 0.112, 0.112, 0.112, 0.112, 0.112, 0.113, 0.113, 0.113, 0.113, 0.113, 0.113, 0.113, 0.113, 0.113, 0.113, 0.113, 0.113, 0.113, 0.114, 0.114, 0.114, 0.114, 0.114, 0.114, 0.114, 0.114, 0.115, 0.115, 0.115, 0.115, 0.115, 0.115, 0.115, 0.115, 0.115, 0.115, 0.115, 0.115, 0.115, 0.115, 0.115, 0.115, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.116, 0.117, 0.117, 0.117, 0.117, 0.117, 0.117, 0.117, 0.117, 0.118, 0.118, 0.118, 0.118, 0.118, 0.118, 0.118, 0.118, 0.118, 0.118, 0.118, 0.118, 0.118, 0.118, 0.118, 0.119, 0.119, 0.119, 0.119, 0.119, 0.119, 0.119, 0.119, 0.119, 0.119, 0.119, 0.119, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.121, 0.121, 0.121, 0.121, 0.121, 0.121, 0.121, 0.121, 0.121, 0.121, 0.122, 0.122, 0.122, 0.122, 0.122, 0.122, 0.122, 0.122, 0.122, 0.122, 0.122, 0.122, 0.122, 0.122, 0.123, 0.123, 0.122, 0.123, 0.123, 0.123, 0.123, 0.123, 0.123, 0.123, 0.123, 0.124, 0.124, 0.124, 0.124, 0.124, 0.124, 0.124, 0.124, 0.124, 0.124, 0.124, 0.124, 0.124, 0.124, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.126, 0.125, 0.125, 0.125, 0.126, 0.126, 0.126, 0.126, 0.126, 0.126, 0.126, 0.126, 0.126, 0.126, 0.126, 0.127, 0.127, 0.127, 0.127, 0.127, 0.127, 0.127, 0.127, 0.127, 0.127, 0.127, 0.127, 0.127, 0.127, 0.127, 0.127, 0.127, 0.128, 0.128, 0.128, 0.128, 0.128, 0.128, 0.128, 0.128, 0.128, 0.128, 0.128, 0.128, 0.128, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.129, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.13, 0.131, 0.131, 0.131, 0.131, 0.131, 0.131, 0.131, 0.131, 0.131, 0.131, 0.131, 0.131, 0.132, 0.132, 0.132, 0.132, 0.132, 0.132, 0.132, 0.132, 0.132, 0.132, 0.132, 0.132, 0.132, 0.132, 0.132, 0.132, 0.133, 0.133, 0.133, 0.133, 0.133, 0.133, 0.133, 0.133, 0.134, 0.133, 0.134, 0.134, 0.134, 0.134, 0.134, 0.134, 0.134, 0.134, 0.134, 0.134, 0.134, 0.134, 0.134, 0.134, 0.134, 0.134, 0.134, 0.134, 0.135, 0.135, 0.135, 0.135, 0.135, 0.135, 0.135, 0.135, 0.135, 0.135, 0.135, 0.135, 0.135, 0.135, 0.136, 0.136, 0.136, 0.136, 0.136, 0.136, 0.136, 0.136, 0.136, 0.136, 0.136, 0.136, 0.136, 0.136, 0.137, 0.137, 0.137, 0.137, 0.137, 0.137, 0.137, 0.137, 0.137, 0.137, 0.137, 0.137, 0.137, 0.137, 0.137, 0.137, 0.137, 0.137, 0.138, 0.138, 0.138, 0.138, 0.138, 0.138, 0.138, 0.138, 0.138, 0.138, 0.138, 0.138, 0.138, 0.139, 0.139, 0.139, 0.139, 0.139, 0.139, 0.139, 0.139, 0.139, 0.139, 0.139, 0.139, 0.139, 0.139, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.141, 0.141, 0.141, 0.141, 0.141, 0.141, 0.141, 0.141, 0.141, 0.141, 0.141, 0.142, 0.141, 0.141, 0.142, 0.142, 0.142, 0.142, 0.142, 0.142, 0.142, 0.142, 0.142, 0.142, 0.142, 0.142, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143, 0.144, 0.144, 0.144, 0.144, 0.144, 0.144, 0.144, 0.144, 0.144, 0.144, 0.144, 0.144, 0.144, 0.144, 0.144, 0.144, 0.144, 0.144, 0.144, 0.145, 0.145, 0.145, 0.145, 0.145, 0.145, 0.145, 0.145, 0.145, 0.145, 0.145, 0.145, 0.145, 0.145, 0.145, 0.146, 0.146, 0.146, 0.146, 0.146, 0.146, 0.146, 0.146, 0.146, 0.146, 0.146, 0.146, 0.146, 0.146, 0.146, 0.146, 0.147, 0.147, 0.147, 0.147, 0.147, 0.147, 0.147, 0.147, 0.147, 0.147, 0.147, 0.147, 0.147, 0.147, 0.147, 0.147, 0.148, 0.148, 0.148, 0.148, 0.148, 0.148, 0.148, 0.148, 0.148, 0.148, 0.148, 0.148, 0.148, 0.149, 0.149, 0.149, 0.149, 0.149, 0.149, 0.149, 0.149, 0.149, 0.149, 0.149, 0.149, 0.149, 0.149, 0.149, 0.15, 0.149, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.151, 0.151, 0.151, 0.151, 0.151, 0.151, 0.151, 0.151, 0.151, 0.151, 0.151, 0.151, 0.151, 0.151, 0.151, 0.152, 0.152, 0.152, 0.152, 0.152, 0.152, 0.152, 0.152, 0.152, 0.152, 0.152, 0.152, 0.152, 0.152, 0.152, 0.152, 0.152, 0.153, 0.153, 0.153, 0.153, 0.153, 0.153, 0.153, 0.153, 0.153, 0.153, 0.153, 0.153, 0.153, 0.153, 0.154, 0.154, 0.154, 0.154, 0.154, 0.154, 0.154, 0.154, 0.154, 0.154, 0.154, 0.154, 0.154, 0.154, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.155, 0.156, 0.156, 0.156, 0.156, 0.156, 0.156, 0.156, 0.156, 0.156, 0.156, 0.156, 0.156, 0.156, 0.156, 0.156, 0.156, 0.156, 0.157, 0.157, 0.157, 0.157, 0.157, 0.157, 0.157, 0.157, 0.158, 0.157, 0.157, 0.157, 0.157, 0.157, 0.157, 0.157, 0.157, 0.156, 0.156, 0.155, 0.155, 0.156, 0.161, 0.159, 0.158, 0.159, 0.158, 0.159, 0.159, 0.159, 0.159, 0.159, 0.159, 0.159, 0.159, 0.159, 0.159, 0.159, 0.159, 0.159, 0.16, 0.159, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.161, 0.161, 0.161, 0.161, 0.161, 0.161, 0.161, 0.161, 0.161, 0.161, 0.161, 0.161, 0.161, 0.161, 0.161, 0.161, 0.161, 0.161, 0.161, 0.162, 0.162, 0.162, 0.162, 0.162, 0.162, 0.162, 0.162, 0.162, 0.162, 0.162, 0.162, 0.162, 0.162, 0.162, 0.163, 0.163, 0.163, 0.163, 0.163, 0.163, 0.163, 0.163, 0.163, 0.163, 0.163, 0.163, 0.163, 0.164, 0.164, 0.164, 0.164, 0.163, 0.164, 0.164, 0.164, 0.164, 0.164, 0.164, 0.164, 0.164, 0.164, 0.164, 0.164, 0.165, 0.165, 0.165, 0.165, 0.165, 0.165, 0.165, 0.165, 0.165, 0.165, 0.165, 0.165, 0.165, 0.165, 0.166, 0.166, 0.166, 0.166, 0.166, 0.166, 0.166, 0.166, 0.166, 0.166, 0.166, 0.166, 0.166, 0.166, 0.166, 0.166, 0.166, 0.166, 0.167, 0.167, 0.166, 0.167, 0.167, 0.167, 0.167, 0.167, 0.167, 0.167, 0.167, 0.167, 0.167, 0.167, 0.167, 0.167, 0.167, 0.167, 0.167, 0.168, 0.167, 0.168, 0.168, 0.168, 0.168, 0.168, 0.168, 0.168, 0.168, 0.168, 0.168, 0.168, 0.168, 0.169, 0.169, 0.169, 0.169, 0.169, 0.169, 0.169, 0.169, 0.169, 0.169, 0.169, 0.169, 0.169, 0.169, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.17, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.171, 0.172, 0.172, 0.172, 0.172, 0.172, 0.172, 0.172, 0.172, 0.172, 0.172, 0.172, 0.172, 0.172, 0.172, 0.173, 0.173, 0.173, 0.173, 0.173, 0.173, 0.173, 0.173, 0.173, 0.173, 0.173, 0.173, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.174, 0.175, 0.174, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.175, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.176, 0.177, 0.177, 0.177, 0.177, 0.177, 0.177, 0.177, 0.177, 0.177, 0.177, 0.177, 0.177, 0.178, 0.178, 0.177, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.178, 0.179, 0.178, 0.179, 0.179, 0.179, 0.179, 0.179, 0.179, 0.179, 0.179, 0.179, 0.179, 0.179, 0.179, 0.179, 0.179, 0.179, 0.179, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.181, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.182, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.184, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.183, 0.184, 0.183, 0.184, 0.184, 0.184, 0.184, 0.184, 0.184, 0.184, 0.184, 0.184, 0.184, 0.184, 0.184, 0.184, 0.184, 0.184, 0.184, 0.184, 0.184, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.185, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.186, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.187, 0.188, 0.188, 0.188, 0.187, 0.188, 0.187, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.188, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.188, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.189, 0.19, 0.189, 0.189, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.19, 0.191, 0.19, 0.19, 0.191, 0.19, 0.19, 0.19, 0.19, 0.191, 0.191, 0.191, 0.191, 0.191, 0.191, 0.191, 0.191, 0.191, 0.191, 0.191, 0.191, 0.191, 0.191, 0.191, 0.191, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.192, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.193, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.194, 0.195, 0.194, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.195, 0.196, 0.195, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.195, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.197, 0.197, 0.196, 0.196, 0.196, 0.196, 0.196, 0.196, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.197, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.198, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.199, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.201, 0.202, 0.201, 0.202, 0.201, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.202, 0.203, 0.202, 0.203, 0.203, 0.203, 0.203, 0.203, 0.203, 0.203, 0.203, 0.203, 0.203, 0.203, 0.203, 0.203, 0.203, 0.203, 0.204, 0.204, 0.204, 0.203, 0.203, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.204, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.205, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.207, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.206, 0.207, 0.206, 0.206, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.207, 0.208, 0.208, 0.208, 0.208, 0.207, 0.207, 0.208, 0.207, 0.207, 0.208, 0.208, 0.208, 0.208, 0.208, 0.208, 0.208, 0.208, 0.208, 0.208, 0.208, 0.208, 0.208, 0.208, 0.208, 0.208, 0.208, 0.208, 0.209, 0.209, 0.208, 0.208, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.21, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.209, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.21, 0.211, 0.21, 0.211, 0.21, 0.211, 0.21, 0.211, 0.21, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.211, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.212, 0.213, 0.213, 0.212, 0.212, 0.212, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213, 0.213, 0.214, 0.214, 0.214, 0.214, 0.214, 0.214, 0.213, 0.214, 0.214, 0.214, 0.214, 0.214, 0.214, 0.214, 0.214, 0.214, 0.214, 0.214, 0.214, 0.214, 0.214, 0.214, 0.215, 0.215, 0.215, 0.215, 0.215, 0.215, 0.215, 0.215, 0.215, 0.215, 0.215, 0.215, 0.216, 0.215, 0.215, 0.215, 0.215, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.216, 0.217, 0.217, 0.217, 0.217, 0.217, 0.217, 0.217, 0.217, 0.217, 0.217, 0.217, 0.218, 0.218, 0.218, 0.217, 0.218, 0.218, 0.218, 0.218, 0.218, 0.218, 0.218, 0.218, 0.218, 0.218, 0.218, 0.218, 0.219, 0.219, 0.218, 0.219, 0.219, 0.219, 0.219, 0.219, 0.219, 0.219, 0.219, 0.219, 0.219, 0.219, 0.219, 0.219, 0.219, 0.219, 0.22, 0.22, 0.22, 0.22, 0.22, 0.22, 0.22, 0.22, 0.22, 0.22, 0.221, 0.22, 0.221, 0.221, 0.22, 0.221, 0.221, 0.221, 0.221, 0.221, 0.221, 0.221, 0.221, 0.221, 0.221, 0.221, 0.222, 0.222, 0.222, 0.222, 0.222, 0.222, 0.222, 0.222, 0.222, 0.222, 0.222, 0.222, 0.222, 0.222, 0.222, 0.223, 0.223, 0.223, 0.223, 0.223, 0.223, 0.223, 0.223, 0.223, 0.223, 0.223, 0.223, 0.223, 0.224, 0.224, 0.224, 0.224, 0.224, 0.224, 0.224, 0.224, 0.224, 0.224, 0.225, 0.224, 0.225, 0.225, 0.225, 0.225, 0.225, 0.225, 0.225, 0.225, 0.225, 0.225, 0.226, 0.226, 0.226, 0.226, 0.226, 0.226, 0.226, 0.226, 0.226, 0.226, 0.226, 0.226, 0.226, 0.226, 0.226, 0.227, 0.227, 0.227, 0.227, 0.227, 0.227, 0.227, 0.227, 0.227, 0.227, 0.228, 0.228, 0.228, 0.227, 0.228, 0.228, 0.228, 0.228, 0.228, 0.228, 0.228, 0.229, 0.229, 0.228, 0.229, 0.229, 0.229, 0.229, 0.229, 0.229, 0.229, 0.229, 0.229, 0.229, 0.23, 0.23, 0.23, 0.23, 0.23, 0.23, 0.23, 0.23, 0.231, 0.231, 0.231, 0.231, 0.231, 0.231, 0.231, 0.231, 0.231, 0.231, 0.231, 0.232, 0.232, 0.232, 0.232, 0.232, 0.232, 0.232, 0.232, 0.232, 0.232, 0.232, 0.232, 0.233, 0.233, 0.233, 0.233, 0.233, 0.233, 0.233, 0.233, 0.233, 0.233, 0.233, 0.234, 0.234, 0.234, 0.234, 0.234, 0.234, 0.234, 0.234, 0.234, 0.234, 0.234, 0.234, 0.234, 0.235, 0.235, 0.235, 0.235, 0.235, 0.235, 0.235, 0.235, 0.235, 0.235, 0.235, 0.235, 0.235, 0.236, 0.236, 0.236, 0.236, 0.236, 0.236, 0.236, 0.236, 0.236, 0.236, 0.237, 0.237, 0.237, 0.237, 0.237, 0.237, 0.237, 0.237, 0.237, 0.237, 0.237, 0.237, 0.237, 0.237, 0.238, 0.238, 0.238, 0.238, 0.238, 0.238, 0.238, 0.238, 0.239, 0.239, 0.239, 0.248, 0.248, 0.248, 0.249, 0.248, 0.248, 0.249, 0.248, 0.249, 0.249, 0.249, 0.249, 0.249, 0.249, 0.249, 0.249, 0.249, 0.249, 0.249, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.251, 0.25, 0.251, 0.251, 0.251, 0.251, 0.251, 0.251, 0.251, 0.251, 0.251, 0.251, 0.251, 0.251, 0.251, 0.252, 0.251, 0.252, 0.252, 0.252, 0.252, 0.252, 0.252, 0.252, 0.252, 0.252, 0.252, 0.253, 0.253, 0.253, 0.253, 0.253, 0.253, 0.253, 0.253, 0.253, 0.253, 0.253, 0.254, 0.254, 0.254, 0.254, 0.254, 0.254, 0.254, 0.254, 0.254, 0.254, 0.254, 0.254, 0.254, 0.255, 0.255, 0.255, 0.255, 0.255, 0.255, 0.255, 0.255, 0.255, 0.255, 0.255, 0.255, 0.256, 0.255, 0.256, 0.255, 0.256, 0.256, 0.256, 0.256, 0.256, 0.256]
        r = 91       # m
        b = 6       # m
        Qs = 1.18/60   # m^3/s
        Qd = Qs*60*60*24 # m^3/d

    m_time_s = [i*60 for i in m_time] # time in seconds
    num_times = len(m_time)
        
    # Compute K and SS to provide parameters for plausibility check
    # (i.e. are the parameter in a reasonable range)
    K = T/b     # m/s
    
    # Theis curve
    t_term = r**2 * S / 4 / T
    s_term = Qs/(4 * np.pi * T)

    t = u_inv * t_term
    s = w_u * s_term

    # Hantush Jacob curve
    for x in range(0,len(u_HAN)):
        t_HAN[x] = u_inv_HAN[x] * t_term
        if (w_u_HAN[x][r_div_B] == 999):
            s_HAN[x] = well_function(1/u_inv_HAN[x]) * s_term
        else:
            s_HAN[x] = w_u_HAN[x][r_div_B] * s_term
        
    # Compute point data for scatter plot
    m_ddown_Hantush = [compute_s(T, S, i, Qs, r, u_HAN, w_u_HAN, r_div_B) for i in m_time_s]
    
    # Find the max for the scatter plot
    max_s = math.ceil(max(m_ddown)*10)/10
        
        
    fig = plt.figure(figsize=(10,14))
    ax = fig.add_subplot(2, 1, 1)
    # Info-Box
    props   = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    out_txt = '\n'.join((       
                         r'$T$ (m²/s) = %10.2E' % (T, ),
                         r'$S$ (-) = %10.2E' % (S, )))
    ax.plot(t, s, label=r'Computed drawdown - Theis')
    ax.plot(t_HAN, s_HAN, 'b--', label=r'Computed drawdown - Hantush-Jacob') 
    if Pirna:
        ax.plot(m_time_s, m_ddown,'o', color='mediumorchid', label=r'measured drawdown - Pirna 24')
    else:
        ax.plot(m_time_s, m_ddown,'go', label=r'measured drawdown - Varnum 16')
    if semilog:
        plt.xscale("log")
    else:    
        plt.yscale("log")
        plt.xscale("log")
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    if refine_plot:
        if semilog:
            plt.axis([1E1,1E5,0,1])
        else:
            plt.axis([1E1,1E5,1E-3,1E+1])
    else:
        if semilog:
            plt.axis([1E-1,1E8,0,10])
            ax.text((0.2),0.8,'Coarse plot - Refine for final fitting')            
        else:
            plt.axis([1E-1,1E8,1E-4,1E+1])
            ax.text((0.2),1.8E-4,'Coarse plot - Refine for final fitting')
    plt.xlabel(r'time t in (s)', fontsize=14)
    plt.ylabel(r'drawdown s in (m)', fontsize=14)
    plt.title(f"Hantush-Jacob drawdown with $r/B$ = {r_div_B_choice}", fontsize=16)
    ax.grid(which="both")
    plt.legend(fontsize=14)
    plt.text(0.3, 0.95,out_txt, horizontalalignment='right', transform=ax.transAxes, fontsize=14, verticalalignment='top', bbox=props)
    
    if scatter:
        x45 = [0,200]
        y45 = [0,200]
        ax = fig.add_subplot(2, 1, 2)
        ax.plot(x45,y45, '--')
        if Pirna:
            ax.plot(m_ddown, m_ddown_Hantush,  'o', color='mediumorchid', label=r'measured')
        else:
            ax.plot(m_ddown, m_ddown_Hantush,  'go', label=r'measured')
        me, mae, rmse = compute_statistics(m_ddown, m_ddown_Hantush)
        plt.title('Scatter plot', fontsize=16)
        plt.xlabel(r'Measured s in m', fontsize=14)
        plt.ylabel(r'Computed s in m', fontsize=14)
        plt.ylim(0, max_s)
        plt.xlim(0, max_s)
        out_txt = '\n'.join((
                             r'$ME = %.3f$ m' % (me, ),
                             r'$MAE = %.3f$ m' % (mae, ),
                             r'$RMSE = %.3f$ m' % (rmse, ))) 
        plt.text(0.97*max_s, 0.05*max_s, out_txt, horizontalalignment='right', bbox=dict(boxstyle="square", facecolor='wheat'), fontsize=14)
    st.pyplot(fig)
    
    columns3 = st.columns((1,10,1), gap = 'medium')
    with columns3[1]:
        if st.button(':green[**Submit**] your parameters and **show results**', key = 70+v):
            st.write("**Parameters and Results**")
            st.write("- Distance of measurement from the well **$r$ = %3i" %r," m**")
            st.write("- Pumping rate during test **$Q$ = %5.3f" %Qs," m³/s**")
            st.write("- Transmissivity **$T$ = % 10.2E"% T, " m²/s**")
            st.write("- Storativity    **$S$ = % 10.2E"% S, "[dimensionless]**")
            st.write("- Thickness of aquitard **$b'$ = % 5.2f"% b2, " m**")
            st.write("- Aquitard Vertical Hydraulic Conductivity **$K'$ = % 10.2E"% (T*b2*float(r_div_B_list[r_div_B])*float(r_div_B_list[r_div_B])/r/r), " m²/s**")
 
inverse(1)

with st.expander('**:red[Click here]** to see one **example of the Hantush-Jacob curve fitting to the :green[Varnum] data**'):
    st.markdown(""" 
            The following example shows one curve match. If five experts made the curve match they would all have a slightly different set of parameter values, but the parameter sets would likely all be close enough to one another to draw comparable conclusions, and make similar predictions. 
            While adjusting parameter values, one finds that the data can be matched well to the Hantush-Jacob curve with an $r/B$ value of 0.4. 
            """)
    left_co2, cent_co2, last_co2 = st.columns((20,60,20))
    with cent_co2:
        st.image('WELL_HYDRAULICS/GWP_Pumping_Test_Analysis/assets/images/Hantush_Varnum_example.png', caption="One example for a curve match of the Hantush-Jacob solution to the Varnum data") 
        
st.subheader(':green-background[Next step - evaluating Theis and Hantush-Jacob curves] with field data from an alluvial aquifer', divider="green")

st.markdown("""
            Above, we investigated field data from the lower Varnum aquifer which is overlain by a semi-permeable aquitard. Parameter values could be adjusted such that the Hantush-Jacob curve closely fit the measured drawdown data.
            
            Next, we investigate how the Hantush-Jacob Solution aligns with field data from an unconfined alluvial aquifer during a pumping test where the drawdown is small relative to the saturated thickness of the unconfined aquifer. Assuming a small change in thickness makes it reasonable to consider use of a confined aquifer solution for an unconfined aquifer because uniform thickness is an underlying assumption of the Theis Solution and its extensions.
            
            We do not have an aquitard thickness for the unconfined system, thus for the purposes of calculation we continue to use the thickness for the Varnum site.
"""
)
# However, some aquifers are unconfined alluvial material with high hydraulic conductivity so the thickness does not change much when they are pumped and so hydrogeologist will often approximate their behavior with equations developed for a confined aquifer. In this case the value of storativity will reflect the specific yield of the aquifer. 

with st.expander("Matching the **Hantush-Jacob Solutions** to drawdown data from a leaky **unconfined aquifer** - :red[Click here]"):
    inverse(2)

with st.expander('**:red[Click here]** to see one **example of the Hantush-Jacob curve fitting to the :violet[Pirna] data**'):
    st.markdown(""" 
            While adjusting parameter values, one finds that the data cannot be matched well to the Hantush-Jacob curve. The reason for this behavior is that the investigated aquifer doesn't conform to the conditions for applying the Hantush-Jacob solution because it is unconfined. In an uncofined aquifer, delayed yield should be considered, that is the character of the drawdown curve will first be controlled by the elastic storage of the aquifer, then there will be a period of constant drawdown while pore drainage
            """)
    left_co2, cent_co2, last_co2 = st.columns((20,60,20))
    with cent_co2:
        st.image('WELL_HYDRAULICS/GWP_Pumping_Test_Analysis/assets/images/Hantush_Pirna_example.png', caption="One example for a curve match of the Hantush-Jacob solution to the Pirna drawdown data") 
    
st.subheader(':green-background[To continue...]', divider="green")
st.markdown("""
            Are you curious whether there is a better way how to proceed with the estimating aquifer properties from drawdown data collected while pumping an unconfined aquifer? On the next page we will investigate the Neuman Solution for calculating drawdown in response to pumping an unconfined aquifer.      
    """
    )

with st.expander('**Click here for some references**'):
    st.markdown("""
    Hantush, M.S. and C.E. Jacob, 1955. Non-steady radial flow in an infinite leaky aquifer, American Geophysical Union Transactions, volume 36, number 1, pages 95-100.
    
    [Kruseman, G.P., de Ridder, N.A., & Verweij, J.M.,  1991.](https://gw-project.org/books/analysis-and-evaluation-of-pumping-test-data/) Analysis and Evaluation of Pumping Test Data, International Institute for Land Reclamation and Improvement, Wageningen, The Netherlands, 377 pages.
"""
)

"---"
# Navigation at the bottom of the side - useful for mobile phone users     
        
columnsN1 = st.columns((1,1,1), gap = 'large')
with columnsN1[0]:
    if st.button("Previous page"):
        st.switch_page("pages/03_🟠_▶️ Theis_solution.py")
with columnsN1[1]:
    st.subheader(':orange[**Navigation**]')
with columnsN1[2]:
    if st.button("Next page"):
        st.switch_page("pages/05_🟣_▶️ Neuman_solution.py")
        
'---'
# Render footer with authors, institutions, and license logo in a single line
columns_lic = st.columns((5,1))
with columns_lic[0]:
    st.markdown(f'Developed by {", ".join(author_list)} ({year}). <br> {institution_text}', unsafe_allow_html=True)
with columns_lic[1]:
    st.image('FIGS/CC_BY-SA_icon.png')