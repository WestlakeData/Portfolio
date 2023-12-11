# MSBA Capstone Project - Maverik

### Business Problem

As Maverik continues to expand operations and open new locations, it is important both for planning as well as for evaluation of ongoing business operations to be able to accurately identify expected revenues at new stores. Of primary importance is to have an accurate forecast of the sales within the four key sales segments (Diesel, Unleaded, Inside Sales, and Food Service) for the first year of an individual store’s operation.  Secondarily, is to have an accurate daily performance forecast for each of the 4 key sales segments.

#### Analytic Problems
In order for this project to be successful, a few tasks need to be accomplished by the final model(s):
1.	Correct Prediction of the First-Year Annual Sales
Models will be developed to accurately forecast the annual sales in each of the 4 key sales segments, taking into account store characteristics.
2.	Correct Prediction of Daily Sales
Models will be developed to accurately forecast the daily sales in each of the 4 key sales segments, taking into account seasonality (both annual and weekly), and store characteristics.
3.	Adjustment of Forecast of Daily Sales to Account for Past Performance
The current model is naive and does not take into account past performance at a location to help forecast future daily sales.  A key improvement of the planned solution will be to derive a solution whereby the predictions of daily performance adjust as actual sales data becomes available.

#### Benefits
Implementing this forecasting solution will empower Maverik with the ability to make informed and strategic decisions regarding new store openings. Accurate sales predictions will enhance financial planning, enabling the company to allocate resources efficiently, create precise ROI documents, optimize inventory management, and improve overall operational efficiency. This, in turn, will bolster investor confidence, streamline store operations, and ensure Maverik’s sustained growth for customers, all while maximizing profitability and minimizing risks associated with expansion.

#### Performance Metrics
The success of this project will be determined by several critical performance metrics. The accuracy of the forecast of the sales will be a primary indicator. Success will be measured through the financial impact, comparing forecasted sales to actuals and their alignment with financial plans and ROI projections. Furthermore, improvements in operational efficiency, illustrated by optimized inventory management and staffing levels, will play a significant role. The ability to create more reliable ROI documents and garner investor confidence is another key metric.

#### Deliverables
The project will deliver a fully functional forecasting model capable of generating accurate daily and annual sales forecasts for inside sales, food service sales, and fuel sales. It will integrate with Maverik's data sources and provide a reporting and visualization tool for decision-makers. However, out of scope are physical store operations and marketing strategy adjustments.

#### Execution
The project will be executed by a dedicated team of three experts, working collaboratively to develop and implement the forecasting solution. The project's deadline is set for 29th November, emphasizing the commitment to deliver precise daily sales forecasts and meet predefined success criteria within the given timeframe. This timeline allows ample time for comprehensive data analysis, model development, and thorough testing to ensure the solution's effectiveness in providing valuable insights for Maverik's strategic decision-making process.
"# Maverik_Forecasting" 

## Exploratory Data Analysis
Based upon our intial analysis, there are several variables which are likely to inform a machine learning model, therefore we propose to continue with this dataset to the modelling phase. Several variables were also identified that have no variation in the data set and so may be excluded. Both 'day of week' and 'annual fiscal week' data showed recognizable seasonality trends which will be important to incorporate into any machine learning model. It is likely that several engineered features will need to be created, however, the current data has already shown that it can capture a significant amount of the variation in the dataset. We propose due to the differences in the 4 key segments it will be necessary to create multiple models in order to accurately forecast sales volumes for each segment. 

## Modelling 
Time series modelling was effective at capturing the seasonality observed in the training data. However predicted values displayed large RMSE values, our model evaluation metric. We therefore decided to pursue other model paradigms. Our modelling showed that Random Forest tree models performed the best in terms of RMSE, which we used as our model evaluation metric. Results for Inside Sales (333.76), Food Service (101.04), Diesel (369.71), and Unleaded Gasoline (352.84) outperformed all other models on the validation data set. XGBoost showed some promise by outperforming Random Forest on Inside Sales (309.17), even though it didn't match the results in other sales components. Further examination of model performance on the test data set, comprised of 5 stores, showed that XGBoost models gave comparable results even though the current model has undergone minimal hyperparameter tuning. Further work in this area will likely lead to improved accuracy of XGBoost models.

In addition, Feature Importance and the elimination of features with low importance had a dramatic effect on the accuracy of both types of tree models (data not shown). We believe that a possible path forward is to use an optimized XGBoost model to produce predicted sales which can then inform a time series model which can improve the models performance in regards to seasonality. This predicted data could then be slowly replaced by actual sales data, which would allow our model to satisfy one of the key aspects of the original business problem.

## Group Work
Group deliverables available <a href link=https://github.com/WestlakeData/Maverik_Forecasting>here</a>
