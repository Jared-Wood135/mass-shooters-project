<!-- Title -->
<div style='background-color: green'>
<head>
    <h1 align='center'><b><u><i>
        Mass Shooters - README
    </i></u></b></h1>
</head></div>
<b><i>IMPORTANT:</i></b>

- This repository uses data from the <a href='https://www.theviolenceproject.org/'>Non-Profit organization: 'The Violence Project'</a>
- Because of the 'Terms of Use' outlined by the <a href='https://www.theviolenceproject.org/'>Non-Profit organization: 'The Violence Project'</a>, I will not be giving out the raw dataset nor the prepared version of their dataset
- If you wish to recreate anything from this repository, you must ask for the version 6.1 dataset from <a href='https://www.theviolenceproject.org/'>The Violence Project</a>
<br><br><br>





<!-- Table of Contents -->
<div style='background-color: orange'>
<head>
    <h3 align='center'><b><i>
        <a id='tableofcontents'></a>
        Table of Contents:
    </i></b></h3>
</head></div>
<h5>
<li><a href='#thanks'>Thanks/Citations</a href></li>
<li><a href='#executivesummary'>Executive Summary</a href></li>
<li><a href='#description'>Project Description</a href></li>
<li><a href='#goals'>Project Goals</a href></li>
<li><a href='#hypo'>Hypothesis/Questions</a href></li>
<li><a href='#datadict'>Data Dictionary</a href></li>
<li><a href='#planning'>Planning</a href></li>
<li><a href='#instructions'>Instruction To Replicate</a href></li>
<li><a href='#takeaways'>Takeaways</a href></li>
</h5>
<br><br><br>





<!-- Executive Summary -->
<div style='background-color: orange'>
<head>
    <h3 align='center'><b><i>
        <a id='thanks'></a>
        Thanks/Citations
    </i></b></h3>
</head></div>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<h5>

- <b><i>THANKS TO</i></b> Jillian Peterson and James Densley from the <a href='https://www.theviolenceproject.org/'>Non-Profit organization: 'The Violence Project'</a> for allowing me to use their dataset!
- Please visit their amazing website, <a href='https://www.theviolenceproject.org/'>The Violence Project</a>, if anything within this repository peaks your interest!
</h5>
<br><br><br>





<!-- Executive Summary -->
<div style='background-color: orange'>
<head>
    <h3 align='center'><b><i>
        <a id='executivesummary'></a>
        Executive Summary:
    </i></b></h3>
</head></div>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<h5>

- <b><i>Project Goals</i></b>
    - Attempt to predict whether a mass shooter is of high volatility (>10 casualties) or is of low volatility (<= 10 casualties).
- <b><i>Key Findings</i></b>
    - Orientation
        - From 1966 - 2022, mass shooting events have increased as well as the average casualties per shooting
    - Key Visuals
        - Leads to increase in casualties:
            - More unique felon crimes committed
            - More unique traumatic events experienced
            - More abnormalities the shooter exhibits
- <b><i>Summary</i></b>
    - It does appear that as an individual deviates further from normal life experiences, psyche, and has less inhibition to harm another, then the individual is more likely to become a highly volatile mass shooter. 
- <b><i>Recommendations</i></b>
    - Implementing this model (+42.9% recall) can give key decision makers in a mass shooting event a stronger drive to allocate more resources and/or quicker actions to a mass shooting event should the shooter be identified as highly volatile.
</h5>
<br><br><br>





<!-- Project Description -->
<div style='background-color: orange'>
<head>
    <h3 align='center'><b><i>
        <a id='description'></a>Project Description:
    </i></b></h3>
</head></div>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<br><br>
<h5>
Using a dataset of U.S. mass shooters from 1966 - JAN2023 given by the <a href='https://www.theviolenceproject.org/'>Non-Profit organization: 'The Violence Project'</a>, attempt to predict whether or not a mass shooter will be of high volatility (> 10 casualties) or of low volatility (<= 10 casualties).
</h5>
<br><br><br>





<!-- Project Goals -->
<div style='background-color: orange'>
<head>
    <h3 align='center'><b><i>
        <a id='goals'></a>Project Goals:
    </i></b></h3>
</head></div>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<br><br>
<h5>
<li>Obtain and read the mass shooters dataset</li>
<li>Ensure the data is formatted and prepared properly</li>
<li>Identify patterns of mass shooters that lead to increase in volatility</li>
<li>Use patterns for modeling</li>
<li>Identify best model and compare to baseline</li>
<li>Repeat process as necessary before moving to next step</li>
</h5>
<br><br><br>





<!-- Hypothesis/Questions -->
<div style='background-color: orange'>
<head>
    <h3 align='center'><b><i>
        <a id='hypo'></a>Hypothesis/Questions:
    </i></b></h3>
</head></div>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<br><br>
<h4><b>
Hypothesis:
</b></h4>
<h5>
I think that as a person is exposed to and/or participates in more violence, hatred, and essentially anything that is outside of the normal scope of a person's life, then that person will become more accostomed to as well as more willing to harm another person.
</h5>
<br>
<h4><b>
Questions:
</b></h4>
<h5>
<li>Does a person's criminal history show an increase in volatility?</li>
<li>Does a person's cumulation of traumatic events show an increase in volatility?</li>
<li>Does a person's exposure and/or participation in violence show an increase in volatility?</li>
<li>Can I discern the shooter's motivation from the data given and see if a particular motivation shows an icrease in volatility?</li>
<li>Does a person's overall accumulation of events that are significant and abnormal to a normal person's life show an increase in volatility?</li>
</h5>
<br><br><br>






<!-- Data Dictionary -->
<div style='background-color: orange'>
<head>
    <h3 align='center'><b><i>
        <a id='datadict'></a>Data Dictionary:
    </i></b></h3>
</head></div>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<br><br>
<b><i>IMPORTANT:</i></b>

- Because of the 'Terms of Use' outlined by the <a href='https://www.theviolenceproject.org/'>Non-Profit organization: 'The Violence Project'</a>, I will not be going in to extrenuous detail of the dataframe especially as to avoid revealing the raw contents of the dataset...

| Feature Name | Data Type | Description | Example |
| ----- | ----- | ----- | ----- |
| 197 Binary Columns(Prepared) | int | If something is true or not for a shooter | 1, 0 |
| 13 Aggregate Column(Prepared) | float | Average score of 0 - 1 from the sum of select columns for each shooter | 0.45 |
| 3 Datetime Columns(Prepared) | datetime | Datetimes of various specific columns |
| 41 Object Columns(Prepared) | Object | Columns that contain descriptions, locations, elaboration of specific circumstances, etc. | AZ |
<br><br><br>






<!-- Planning -->
<div style='background-color: orange'>
<head>
    <h3 align='center'><b><i>
        <a id='planning'></a>Planning:
    </i></b></h3>
</head></div>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<br><br>
<h4><b>Objective</b></h4>
<li>Create a predictive model of a mass shooter's volatility</li>
<br>
<h4><b>Methodology</b></h4>
<li>Data science pipeline (Wrangle, Explore, Model)</li>
<li>Wrangle the data by properly acquiring the data then ensuring the data can be interpreted by both human and machine via preparation</li>
<li>Explore for key features, relationships, and patterns</li>
<li>Create clusters if and when necessary</li>
<li>Create models to best predict quality</li>
<li>Deliver takeaways</li>
<br>
<h4><b>Deliverables</b></h4>
<li>final_report.ipynb</li>
<li>This github repository</li>
<br><br><br>






<!-- Instructions To Replicate -->
<div style='background-color: orange'>
<head>
    <h3 align='center'><b><i>
        <a id='instructions'></a>Instructions To Replicate:
    </i></b></h3>
</head></div>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<br><br>

<b><i>IMPORTANT:</i></b>

- Because of the 'Terms of Use' outlined by the <a href='https://www.theviolenceproject.org/'>Non-Profit organization: 'The Violence Project'</a>, I will not be giving out either the raw or prepared version of this data...
- HOWEVER, if you request the dataset from the <a href='https://www.theviolenceproject.org/'>Non-Profit organization: 'The Violence Project'</a>, and ensure you have version 6.1 of the mass shooter data, then you will be able to run anything and everything in this repository...
<br><br><br>





<!-- Takeaways -->
<div style='background-color: orange'>
<head>
    <h3 align='center'><b><i>
        <a id='takeaways'></a>Takeaways:
    </i></b></h3>
</head></div>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<br><br>
<h4><b>Summary:</b></h4>

- Since 1966, mass shooting events as well as the average casualties have been increasing.

- It does appear that as an individual deviates further from normal life experiences, psyche, and has less inhibition to harm another, then the individual is more likely to become a highly volatile mass shooter. 
<br><br>
<h4><b>Recommendations:</b></h4>

- Though the best model created performs the same as the baseline in terms of accuracy, the model does predict if a mass shooter is highly volatile 42.9% better than the baseline model.

- Implementing this model can give key decision makers in a mass shooting event a stronger drive to allocate more resources and/or quicker actions to a mass shooting event should the shooter be identified as highly volatile.
<br><br>
<h4><b>Next Steps:</b></h4>

1. (CURRENT) Predict volatility of mass shooters
    - Fully exhaust all exploration routes from this dataset (Only 1 excel sheet out of 8 sheets)
        - Attempt to identify stronger features
        - Attempt to improve model accuracy/recall
        - Create regression models to better predict casualties rather than binning them
   - Repeat this process for the 'true' full-dataset (All 8 excel sheets)
        - Attempt to improve findings from #1
   - Ensure the best possible model is created from this 'true' full-dataset
        - All possible exploration/modeling exhausted
2. (FUTURE) Predict shooter to mass shooter
    - Identify patterns of shooters
    - Create model for shooters
    - Attempt to use both shooter and mass shooter model to predict if someone will be a mass shooter as well as their volatility from a population of shooters
3. (FUTURE) Predict criminal to shooter
    - Identify patterns of criminals
    - Create model for criminals
    - Attempt to use criminal, shooter, and mass shooter models to predict if someone will be a mass shooter as well as their volatility from a population of criminals
4. (FUTURE) Predict civilian to criminal
    - Identify patterns of civilians
    - Create model for civilians
    - Attempt to use civilian, criminal, shooter, and mass shooter models to predict if someone will be a mmass shooter as well as their volatility from a population of civilians
5. (FUTURE) See similarities between countries???
<br><br>