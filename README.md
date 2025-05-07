# KMeansClustering
Clustering Countries Using Socioeconomic Indicators with K-Means.

This project aims to compare the results of a K-Means clustering algorithm with the Human Development Index (HDI) classifications for countries in the year 2017.

In the "AllFeatures" version of the project, all features with at least 200 non-null values are selected from the "Country Statistics - UNData" dataset (https://www.kaggle.com/datasets/sudalairajkumar/undata-country-profiles) to cluster countries into four groups. This number mirrors the four standard HDI tiers (https://hdr.undp.org/data-center/human-development-index#/indicies/HDI). Using a K-Means++ model with Lloyd’s algorithm, an interactive world map is generated and displayed in the browser, enabling visual analysis of the resulting clusters. This map can be compared with the 2017 HDI map (https://ourworldindata.org/grapher/human-development-index?time=2017) based on data from the same year.

As an iteration on this concept, the "HDIFeatures" version focuses exclusively on indicators that directly contribute to the calculation of HDI. These indicators were selected from the same dataset, based on research into the components of HDI. Additionally, the number of clusters was increased to seven, matching the tier system used in the 2017 HDI visualization from Our World in Data (https://ourworldindata.org/grapher/human-development-index?time=2017) using seven tiers instead of four. Although HDI is conventionally presented in four tiers, this modification allows for a more precise visual comparison between the model-generated map and the official HDI map.

Descriptions for each indicator of HDI can be found here: https://www.investopedia.com/terms/h/human-development-index-hdi.asp#:~:text=It%20is%20composed%20of%20four,income%20(GNI)%20per%20capita.

**Health:** Measured by the life expectancy calculated at the time of birth, which the UNData dataset countains

**Education:** Measured by the mean years of schooling for residents, and the expected years of schooling. However, the UNData dataframe does not contain these statistics. In its place I used the % of the population that enroll in primary, secondary, and tertiary education.

**Economics** Measured by Gross National Income (GNI) per capita. Since GNI per capita is not available in the UNData dataset, the unemployment rate was used as the closest economic proxy.
