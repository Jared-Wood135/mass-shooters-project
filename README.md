<!-- Title -->
<head>
    <h1 align='center'><b><u><i>
        Wine Project - README
    </i></u></b></h1>
</head>





<!-- Table of Contents -->
<head>
    <h3 align='center'><b><i>
        <a id='tableofcontents'></a>Table of Contents:
    </i></b></h3>
</head>
<h5>
<li><a href='#description'>Project Description</a></li>
<li><a href='#goals'>Project Goals</a></li>
<li><a href='#hypo'>Hypothesis/Questions</a></li>
<li><a href='#datadict'>Data Dictionary</a></li>
<li><a href='#planning'>Planning</a></li>
<li><a href='#instructions'>Instruction To Replicate</a></li>
<li><a href='#takeaways'>Takeaways</a></li>
</h5>
<br><br><br>




<!-- Project Description -->
<head>
    <h3 align='center'><b><i>
        <a id='description'></a>Project Description:
    </i></b></h3>
</head>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<br><br>
<h5>
Using a 'red' and 'white' wine dataset from <a href='https://data.world/food/wine-quality'>Data.World Wine Quality Dataset</a>, determine the drivers of wine quality and create a model to best predict a wine's quality.
</h5>
<br><br><br>





<!-- Project Goals -->
<head>
    <h3 align='center'><b><i>
        <a id='goals'></a>Project Goals:
    </i></b></h3>
</head>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<br><br>
<h5>
<li>Implement Data Science Pipeline</li>
<li>Acquire 'red' and 'white' wine Datasets</li>
<li>Prepare both Datasets and join them into one</li>
<li>Explore and evaluate 'wine' Dataset for key driving features and create clusters where necessary</li>
<li>Model creation based off of key features from exploration</li>
<li>Deliver key takeaways and findings to audience</li>
</h5>
<br><br><br>





<!-- Hypothesis/Questions -->
<head>
    <h3 align='center'><b><i>
        <a id='hypo'></a>Hypothesis/Questions:
    </i></b></h3>
</head>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<br><br>
<h4><b>
Hypothesis:
</b></h4>
<h5>
Given the 'red' and 'white' wine datasets, the location, the pH levels, the overall balance of the wine, and processing of the wines will affect the wine's quality.
</h5>
<br>
<h4><b>
Questions:
</b></h4>
<h5>
<li>What features from this specific dataset can reasonably correlate to wine quality?</li>
<li>Does the alcohol content affect wine quality?</li>
<li>Does the acidity content affect wine quality?</li>
<li>Does the pH affect wine quality</li>
<li>Does the acidity level affect wine quality</li>
<li>Does red wines or white wines tend to have a better or lower quality score?</li>
<li>Is there any obvious signs of clustering when exploring the data?</li>
</h5>
<br><br><br>






<!-- Data Dictionary -->
<head>
    <h3 align='center'><b><i>
        <a id='datadict'></a>Data Dictionary:
    </i></b></h3>
</head>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<br><br>

| Feature Name | Data Type | Description | Example |
| ----- | ----- | ----- | ----- |
| fixed acidity | float | Total amount of tataric acid (Tartness and structure of wine) | 8.4 |
| volatile acidity | float | Total amount of acetic acid (Aroma and taste of wine) | 0.36 |
| citric acid | float | Total amount of weak organic acid (Natural preservative) | 0.36 |
| residual sugar | float | Total amount of sugar left in the wine after fermentation (Sweetness) | 11.1 |
| chlorides | float | Total amount of salt in wine (Flavor and mouthfeel) | 0.032 |
| free sulfur dioxide | float | Amount of added preservative to prevent oxidation and microbial spoilage (Aroma and taste) | 21.0 |
| total sulfur dioxide | float | Total amount of sulfur dioxide in wine (Aroma and taste) | 132.0 |
| density | float | Weight of wine relative to the volume of water (Indication of wine's body and alcohol content) | 0.99313 |
| pH | float | Acidity level on a scale of 0 to 14 (Lower is more acidic) | 2.95 |
| sulphates | float | Amount of sulfur-containing compounds (Aroma and preservation) | 0.39 |
| alcohol | float | alcohol content of the wine | 13.0 |
| quality | int | Scale from 0 to 10 of wine quality | 5 |


<br><br><br>






<!-- Planning -->
<head>
    <h3 align='center'><b><i>
        <a id='planning'></a>Planning:
    </i></b></h3>
</head>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<br><br>
<h4><b>Objective</b></h4>
<li>Create a classification model to best predict the wine’s quality score</li>
<br>
<h4><b>Methodology</b></h4>
<li>Data science pipeline</li>
<li>Explore for key features and relationships</li>
<li>Create clusters if and when necessary</li>
<li>Create models to best predict quality</li>
<li>Deliver takeaways</li>
<br>
<h4><b>Deliverables</b></h4>
<li>final_report.ipynb</li>
<li>Slide show (5 minute presentation)</li>
<br><br><br>






<!-- Instructions To Replicate -->
<head>
    <h3 align='center'><b><i>
        <a id='instructions'></a>Instructions To Replicate:
    </i></b></h3>
</head>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<br><br>

1. Clone this repo
2. Run desired files/operations
<br><br><br>





<!-- Takeaways -->
<head>
    <h3 align='center'><b><i>
        <a id='takeaways'></a>Takeaways:
    </i></b></h3>
</head>
<a href='#tableofcontents'>Back to 'Table of Contents'</a>
<br><br>
<h4><b>Summary:</b></h4>

- Through exploration and clustering, no one feature directly impacts the wine quality.  Rather, it's the wine's balance of all the features combined that better dictates the quality.
<br><br>
<h4><b>Recommendations:</b></h4>

- Better understand how to literally define the 'balance' of a wine's content in order to better predict a wine's quality.
<br><br>
<h4><b>Next Steps:</b></h4>

- Conduct further exploration, feature engineering, and clustering methods in order to better define 'balance' for the machine to understand so that the machine will have a more accurate predictor of higher quality wines.
<br><br>