PS\#3: Hodgepodge
================
Chih-Yu Chiang
UCID 12145146
May 14, 2017

Part 1: Regression diagnostics
------------------------------

### Estimate model

``` r
df <- read_csv("data/biden.csv") %>%
  na.omit() %>%
  rownames_to_column(var="row")
```

    ## Parsed with column specification:
    ## cols(
    ##   biden = col_integer(),
    ##   female = col_integer(),
    ##   age = col_integer(),
    ##   educ = col_integer(),
    ##   dem = col_integer(),
    ##   rep = col_integer()
    ## )

``` r
lm_1 <- lm(biden ~ age + female + educ, data=df)
pander(summary(lm_1))
```

<table style="width:86%;">
<colgroup>
<col width="25%" />
<col width="15%" />
<col width="18%" />
<col width="13%" />
<col width="13%" />
</colgroup>
<thead>
<tr class="header">
<th align="center"> </th>
<th align="center">Estimate</th>
<th align="center">Std. Error</th>
<th align="center">t value</th>
<th align="center">Pr(&gt;|t|)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="center"><strong>age</strong></td>
<td align="center">0.04188</td>
<td align="center">0.03249</td>
<td align="center">1.289</td>
<td align="center">0.1975</td>
</tr>
<tr class="even">
<td align="center"><strong>female</strong></td>
<td align="center">6.196</td>
<td align="center">1.097</td>
<td align="center">5.65</td>
<td align="center">1.864e-08</td>
</tr>
<tr class="odd">
<td align="center"><strong>educ</strong></td>
<td align="center">-0.8887</td>
<td align="center">0.2247</td>
<td align="center">-3.955</td>
<td align="center">7.941e-05</td>
</tr>
<tr class="even">
<td align="center"><strong>(Intercept)</strong></td>
<td align="center">68.62</td>
<td align="center">3.596</td>
<td align="center">19.08</td>
<td align="center">4.337e-74</td>
</tr>
</tbody>
</table>

<table style="width:85%;">
<caption>Fitting linear model: biden ~ age + female + educ</caption>
<colgroup>
<col width="20%" />
<col width="30%" />
<col width="11%" />
<col width="22%" />
</colgroup>
<thead>
<tr class="header">
<th align="center">Observations</th>
<th align="center">Residual Std. Error</th>
<th align="center"><span class="math inline"><em>R</em><sup>2</sup></span></th>
<th align="center">Adjusted <span class="math inline"><em>R</em><sup>2</sup></span></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="center">1807</td>
<td align="center">23.16</td>
<td align="center">0.02723</td>
<td align="center">0.02561</td>
</tr>
</tbody>
</table>

After applying listwise missing value deletion, the above model is estimated with 1,807 observations, `age`, `female` (gender), and `educ` (education) as predictor variables, and `biden` (Joe Biden feeling thermometer) as the outcome variable.

Estimated parameters, standard errors, and significance are reported in the first table.

### 1. Test the model to identify any unusual and/or influential observations. Identify how you would treat these observations moving forward with this research.

``` r
pander(summary(df))
```

<table style="width:99%;">
<caption>Table continues below</caption>
<colgroup>
<col width="23%" />
<col width="19%" />
<col width="19%" />
<col width="18%" />
<col width="18%" />
</colgroup>
<thead>
<tr class="header">
<th align="center">row</th>
<th align="center">biden</th>
<th align="center">female</th>
<th align="center">age</th>
<th align="center">educ</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="center">Length:1807</td>
<td align="center">Min. : 0.0</td>
<td align="center">Min. :0.000</td>
<td align="center">Min. :18.0</td>
<td align="center">Min. : 0.0</td>
</tr>
<tr class="even">
<td align="center">Class :character</td>
<td align="center">1st Qu.: 50.0</td>
<td align="center">1st Qu.:0.000</td>
<td align="center">1st Qu.:34.0</td>
<td align="center">1st Qu.:12.0</td>
</tr>
<tr class="odd">
<td align="center">Mode :character</td>
<td align="center">Median : 60.0</td>
<td align="center">Median :1.000</td>
<td align="center">Median :47.0</td>
<td align="center">Median :13.0</td>
</tr>
<tr class="even">
<td align="center">NA</td>
<td align="center">Mean : 62.2</td>
<td align="center">Mean :0.553</td>
<td align="center">Mean :47.5</td>
<td align="center">Mean :13.4</td>
</tr>
<tr class="odd">
<td align="center">NA</td>
<td align="center">3rd Qu.: 85.0</td>
<td align="center">3rd Qu.:1.000</td>
<td align="center">3rd Qu.:59.5</td>
<td align="center">3rd Qu.:16.0</td>
</tr>
<tr class="even">
<td align="center">NA</td>
<td align="center">Max. :100.0</td>
<td align="center">Max. :1.000</td>
<td align="center">Max. :93.0</td>
<td align="center">Max. :17.0</td>
</tr>
</tbody>
</table>

<table style="width:39%;">
<colgroup>
<col width="19%" />
<col width="19%" />
</colgroup>
<thead>
<tr class="header">
<th align="center">dem</th>
<th align="center">rep</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="center">Min. :0.000</td>
<td align="center">Min. :0.000</td>
</tr>
<tr class="even">
<td align="center">1st Qu.:0.000</td>
<td align="center">1st Qu.:0.000</td>
</tr>
<tr class="odd">
<td align="center">Median :0.000</td>
<td align="center">Median :0.000</td>
</tr>
<tr class="even">
<td align="center">Mean :0.432</td>
<td align="center">Mean :0.205</td>
</tr>
<tr class="odd">
<td align="center">3rd Qu.:1.000</td>
<td align="center">3rd Qu.:0.000</td>
</tr>
<tr class="even">
<td align="center">Max. :1.000</td>
<td align="center">Max. :1.000</td>
</tr>
</tbody>
</table>

``` r
ggplot(df) +
  geom_histogram(aes(x=biden), binwidth=1) +
  labs(title="Histogram of Joe Biden feeling thermometer",
       x="Joe Biden feeling thermometer",
       y="Observation count")
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P1-1%20Basic-1.png)

``` r
ggplot(df) +
  geom_histogram(aes(x=educ), binwidth=1) +
  labs(title="Histogram of education",
       x="Education",
       y="Observation count")
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P1-1%20Basic-2.png)

``` r
ggplot(df) +
  geom_histogram(aes(x=age), binwidth=1) +
  labs(title="Histogram of age",
       x="Age",
       y="Observation count")
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P1-1%20Basic-3.png)

To observe the unusual observations, first, I examine descriptive statistics and histograms of variables. From the descriptive summary, we make sure that all the binary variables, `female`, `dem`, and `rep`, contain only appropriate responses (0 or 1). I then turn to the histograms to examine the continuous (or order) variables. From the graphs, we can see some observations with `biden` at 0, some with `educ` at lower level, such as less than 7, and some with `age`, such as higher than 80--they stray from the major part of the observations and could potentially have disproportionate influences on our model. To check if their influence a problem of our model, next, I do a bubble plot with influential indicators.

``` r
#Add key statistics
df_augment <- df %>%
  mutate(hat=hatvalues(lm_1),
         student=rstudent(lm_1),
         cooksd=cooks.distance(lm_1))

# draw bubble plot
ggplot(df_augment, aes(hat, student)) +
  geom_hline(yintercept=0, linetype=2) +
  geom_point(aes(size=cooksd), shape=1) +
  geom_text(data=df_augment %>%
              arrange(-cooksd) %>%
              slice(1:10),
            aes(label=row, color="orange")) +
  scale_size_continuous(range=c(1, 20)) +
  labs(title="Bubble plot of influential indicators",
       subtitle="Leverage, Sutentized residual, and Cook’s D (bubble size)",
       x="Leverage",
       y="Studentized residual") +
  theme(legend.position ="none")
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P1-1%20Bubble-1.png)

The bubble size denotes the observation's Cook's D value. In the graph, I identify the ten observations with the highest Cook's D value, with their IDs marked in the bubbles, including observation 408, 609, 1086, 1682, etc.

``` r
hat <- df_augment %>%
  filter(hat > 2 * mean(hat))

student <- df_augment %>%
  filter(abs(student) > 2)

cooksd <- df_augment %>%
  filter(cooksd > 4 / (nrow(.) - (length(coef(lm_1)) - 1) - 1))

bind_rows(hat, student, cooksd)
```

    ## # A tibble: 246 × 10
    ##      row biden female   age  educ   dem   rep      hat  student    cooksd
    ##    <chr> <int>  <int> <int> <int> <int> <int>    <dbl>    <dbl>     <dbl>
    ## 1     48    70      0    80    17     0     0 0.005036  0.56855 4.092e-04
    ## 2    100    70      1    44     7     1     0 0.004959 -0.01899 4.494e-07
    ## 3    151   100      1    64     1     1     0 0.015371  1.01787 4.043e-03
    ## 4    250   100      1    76     3     1     0 0.011841  1.07146 3.439e-03
    ## 5    253    60      1    84    16     0     0 0.004457 -0.17805 3.550e-05
    ## 6    274    60      1    63     4     0     0 0.009328 -0.60292 8.560e-04
    ## 7    282    85      0    18     8     1     0 0.005995  0.98460 1.462e-03
    ## 8    289    70      0    79     9     1     0 0.004614  0.26259 7.995e-05
    ## 9    296    50      1    22     9     0     0 0.004497 -0.76763 6.656e-04
    ## 10   318    50      1    23     8     0     0 0.005379 -0.80827 8.834e-04
    ## # ... with 236 more rows

I then do some quick rules of thumb stat examination, including standards for Hat-values, Studentized residuals, and Cook's D indicator:

-   Anything with Hat-values exceeding twice the average Hat-values.
-   Anything with Studentized residuals outside of the range \[−2,2\].
-   Anything with Cook's D &gt; 4/(n-k-1), where n is the number of observations and k is the number of coefficients in the regression model.

I filter to acquire the 246 observations who fall into any of the above three groups. In general, the identified observations have either `biden` = 0, lower `educ` level, or/and higher `age` level. This result conforms to what we concluded in observing the data summary and histograms.

While those observations are identified visually and statistically, they are all still reasonable for me. Their values still fall in reasonable range. For example, people are possible to have a low level of biden affection to have `biden` = 0; it is also not uncommon to have respondants in their 80s or 90s, or with fewer years of education. In other words, these identified observations are probably not caused by survey or recording mistakes. The reason why they are identified here is probably just because, naturally in the population, fewer people have those traits. For example, it is natural that there are less people in their 90s than in 40s or 50s. Accordingly, potential treatments in dealing with these observations are proposed as follows:

1.  As these observations seem not unreasonable and could represent distribution of the real population, it is less proper to just delete them listwise--that could make the model less representative to the real situation.
2.  Instead, I would suggest keep these observations in estimating the model. Perhaps, we should also consider collecting more data with those identified traits to estimate the traits at these identified levels better.
3.  Another action can be taken is that redoing this survey with extended scale for the survey item evaluating biden thermometer. While many respondants answered `biden` at level 0 and 100, this could indicate the scale is not complete enough to account for the diverse level of biden affection. For example, if the upper limit is extended to 200, the observations can be scattered into a larger range, which leads to a larger standard error and could make these "unusual" observations normal (they are normal by nature, in some sense).

### 2. Test for non-normally distributed errors. If they are not normally distributed, propose how to correct for them.

``` r
car::qqPlot(lm_1)
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P1-2%20QQ%20and%20dis-1.png)

``` r
augment(lm_1, df) %>%
  mutate(.student=rstudent(lm_1)) %>%
  ggplot(aes(.student)) +
  geom_density(adjust=.5) +
  labs(title = "Density plot of the studentized residuals",
       x="Studentized residuals",
       y="Estimated density")
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P1-2%20QQ%20and%20dis-2.png)

I apply the qqplot and the density plot of the studentized residuals to observe if there are the non-normally distributed errors. In the qqplot, many of the observation points stray outside the 95% confidence intervals marked by the dashed red lines at higher levels (&gt; 1.5) and lower levels (at around -2) of t quantiles. This is confirmed in the residual plot, where the distribution is apparently left skewed, with too many observations having higher level residuals. These evidences indicate the extant of non-normally distributed problem.

``` r
df_power <- df %>%
  mutate(biden_power = biden**1.4)

lm_1_2 <- lm(biden_power ~ age + female + educ, data=df_power)
pander(summary(lm_1_2))
```

<table style="width:86%;">
<colgroup>
<col width="25%" />
<col width="15%" />
<col width="18%" />
<col width="13%" />
<col width="13%" />
</colgroup>
<thead>
<tr class="header">
<th align="center"> </th>
<th align="center">Estimate</th>
<th align="center">Std. Error</th>
<th align="center">t value</th>
<th align="center">Pr(&gt;|t|)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="center"><strong>age</strong></td>
<td align="center">0.437</td>
<td align="center">0.2238</td>
<td align="center">1.952</td>
<td align="center">0.05107</td>
</tr>
<tr class="even">
<td align="center"><strong>female</strong></td>
<td align="center">41.81</td>
<td align="center">7.557</td>
<td align="center">5.533</td>
<td align="center">3.612e-08</td>
</tr>
<tr class="odd">
<td align="center"><strong>educ</strong></td>
<td align="center">-5.969</td>
<td align="center">1.548</td>
<td align="center">-3.855</td>
<td align="center">0.0001198</td>
</tr>
<tr class="even">
<td align="center"><strong>(Intercept)</strong></td>
<td align="center">374.5</td>
<td align="center">24.78</td>
<td align="center">15.11</td>
<td align="center">1.122e-48</td>
</tr>
</tbody>
</table>

<table style="width:85%;">
<caption>Fitting linear model: biden_power ~ age + female + educ</caption>
<colgroup>
<col width="20%" />
<col width="30%" />
<col width="11%" />
<col width="22%" />
</colgroup>
<thead>
<tr class="header">
<th align="center">Observations</th>
<th align="center">Residual Std. Error</th>
<th align="center"><span class="math inline"><em>R</em><sup>2</sup></span></th>
<th align="center">Adjusted <span class="math inline"><em>R</em><sup>2</sup></span></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="center">1807</td>
<td align="center">159.6</td>
<td align="center">0.0277</td>
<td align="center">0.02608</td>
</tr>
</tbody>
</table>

``` r
car::qqPlot(lm_1_2)
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P1-2%20Solution-1.png)

``` r
augment(lm_1_2, df_power) %>%
  mutate(.student = rstudent(lm_1_2)) %>%
  ggplot(aes(.student)) +
  geom_density(adjust = .5) +
  labs(title = "Density plot of the studentized residuals",
       x = "Studentized residuals",
       y = "Estimated density")
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P1-2%20Solution-2.png)

To correct the non-normally distributed error, I propose a power transformation for the `biden` variable. I try transforming `biden` to the power of 1.4; the result is displayed as above. In qqplot, at the identifed levels, substantially less observations fall outside the confidence interval. The residual distribution is also less skewed compared to the original one.

### 3. Test for heteroscedasticity in the model. If present, explain what impact this could have on inference.

``` r
df_hetero <- df %>%
  add_predictions(lm_1) %>%
  add_residuals(lm_1)

ggplot(df_hetero, aes(pred, resid)) +
  geom_point(alpha = .2) +
  geom_hline(yintercept = 0, linetype = 2) +
  geom_quantile(method = "rqss", lambda = 5, quantiles = c(.05, .95)) +
  labs(title = "Homoscedastic variance of error terms",
       x = "Predicted values",
       y = "Residuals")
```

    ## Loading required package: SparseM

    ## 
    ## Attaching package: 'SparseM'

    ## The following object is masked from 'package:base':
    ## 
    ##     backsolve

    ## Smoothing formula not specified. Using: y ~ qss(x, lambda = 5)

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P1-3%20Scatter-1.png)

For detecting heteroscedasticity problem, I apply the residual plot. From the plot, we can observe that the residuals for observations with higher predicted values (&gt; 65) and lower predicted values (&lt; 57) have smaller variances, compared to the observations with middle levels of predicted values.

``` r
bptest(lm_1)
```

    ## 
    ##  studentized Breusch-Pagan test
    ## 
    ## data:  lm_1
    ## BP = 23, df = 3, p-value = 5e-05

In the Breusch-Pagan test, we also have to reject the null hypothesis, which indicates the present of heteroscedasticity.

``` r
weights <- 1 / residuals(lm_1) ^ 2

lm_wls <- lm(biden ~ age + female + educ, data=df, weights=weights)
pander(lm_wls)
```

<table style="width:86%;">
<caption>Fitting linear model: biden ~ age + female + educ</caption>
<colgroup>
<col width="25%" />
<col width="15%" />
<col width="18%" />
<col width="13%" />
<col width="13%" />
</colgroup>
<thead>
<tr class="header">
<th align="center"> </th>
<th align="center">Estimate</th>
<th align="center">Std. Error</th>
<th align="center">t value</th>
<th align="center">Pr(&gt;|t|)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="center"><strong>age</strong></td>
<td align="center">0.03883</td>
<td align="center">0.00227</td>
<td align="center">17.11</td>
<td align="center">6.353e-61</td>
</tr>
<tr class="even">
<td align="center"><strong>female</strong></td>
<td align="center">5.97</td>
<td align="center">0.1288</td>
<td align="center">46.37</td>
<td align="center">1.196e-309</td>
</tr>
<tr class="odd">
<td align="center"><strong>educ</strong></td>
<td align="center">-0.9098</td>
<td align="center">0.02879</td>
<td align="center">-31.6</td>
<td align="center">9.449e-175</td>
</tr>
<tr class="even">
<td align="center"><strong>(Intercept)</strong></td>
<td align="center">69.02</td>
<td align="center">0.3368</td>
<td align="center">204.9</td>
<td align="center">0</td>
</tr>
</tbody>
</table>

To counter the problem of heteroscedasticity, I propose applying the weighted least squares regression as estimated above. In this model, we assume that the errors are independent and normally distributed with mean zero and different variances. The weights are estimated from the error variances of the original model. Comparing the new model to the original one, the parameter estimates change not much. However, the standard errors become a lot smaller, which can potentially be biased. The weights, therefore, are suggested to be estimated from relevant explanatory variables (if having any theory), instead of basing only on original residuals.

### 4. Test for multicollinearity. If present, propose if/how to solve the problem.

``` r
cormat_heatmap <- function(data){
  # generate correlation matrix
  cormat <- round(cor(data), 2)
  
  # melt into a tidy table
  get_upper_tri <- function(cormat){
    cormat[lower.tri(cormat)]<- NA
    return(cormat)
  }
  
  upper_tri <- get_upper_tri(cormat)
  
  # reorder matrix based on coefficient value
  reorder_cormat <- function(cormat){
    # Use correlation between variables as distance
    dd <- as.dist((1-cormat)/2)
    hc <- hclust(dd)
    cormat <-cormat[hc$order, hc$order]
  }
  
  cormat <- reorder_cormat(cormat)
  upper_tri <- get_upper_tri(cormat)
  
  # Melt the correlation matrix
  melted_cormat <- reshape2::melt(upper_tri, na.rm = TRUE)
  
  # Create a ggheatmap
  ggheatmap <- ggplot(melted_cormat, aes(Var2, Var1, fill = value))+
    geom_tile(color = "white")+
    scale_fill_gradient2(low = "blue", high = "red", mid = "white", 
                         midpoint = 0, limit = c(-1,1), space = "Lab", 
                         name="Pearson\nCorrelation") +
    theme_minimal()+ # minimal theme
    theme(axis.text.x = element_text(angle = 45, vjust = 1, 
                                     size = 12, hjust = 1))+
    coord_fixed()
  
  # add correlation values to graph
  ggheatmap + 
    geom_text(aes(Var2, Var1, label = value), color = "black", size = 4) +
    theme(
      axis.title.x = element_blank(),
      axis.title.y = element_blank(),
      panel.grid.major = element_blank(),
      panel.border = element_blank(),
      panel.background = element_blank(),
      axis.ticks = element_blank(),
      legend.position = "bottom") +
    labs(title="Correlation matrix")
}

cormat_heatmap(select(df, age, female, educ))
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P1-4%20Correlation-1.png)

``` r
ggpairs(select(df, age, female, educ))
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P1-4%20Correlation-2.png)

To detect collinearity, I observe the correlation matrix of explanatory variables. From the graphs, all correlations are low. There seems no high-level correlations could potentially cause collinearity problem. In the pair-wise scatter plots, no specific correlated patterns can be observed.

``` r
vif(lm_1)
```

    ##    age female   educ 
    ##  1.013  1.002  1.012

VIF values are also computed. All are at values around 1, way smaller than 10. This indicates that we probably do not have to worry too much about the collinearity in our model.

However, if the collinearity do exist, three approaches are suggested to address the problem:
1. Add more observations to increase the probability that different levels of one variables can be observed conditional on a certain level of other variables.
2. Transform the variables. For example, combine the variables with the collinearity problem into a new variable, which captures the information provided in all original variables while avoiding the collinearity problem.
3. Applying Shrinkage methods, such as lasso regression, to involve all variables while shrinking all estimated coefficients toward zero. This method acquires smaller variance of the estimates with a cost of increasing the potential bias.

Part 2: Interaction terms
-------------------------

### Estimate model

``` r
lm_2 <- lm(biden ~ age + educ + age * educ, data=df)
pander(summary(lm_2))
```

<table style="width:86%;">
<colgroup>
<col width="25%" />
<col width="15%" />
<col width="18%" />
<col width="13%" />
<col width="13%" />
</colgroup>
<thead>
<tr class="header">
<th align="center"> </th>
<th align="center">Estimate</th>
<th align="center">Std. Error</th>
<th align="center">t value</th>
<th align="center">Pr(&gt;|t|)</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="center"><strong>age</strong></td>
<td align="center">0.6719</td>
<td align="center">0.1705</td>
<td align="center">3.941</td>
<td align="center">8.431e-05</td>
</tr>
<tr class="even">
<td align="center"><strong>educ</strong></td>
<td align="center">1.657</td>
<td align="center">0.714</td>
<td align="center">2.321</td>
<td align="center">0.02038</td>
</tr>
<tr class="odd">
<td align="center"><strong>age:educ</strong></td>
<td align="center">-0.04803</td>
<td align="center">0.0129</td>
<td align="center">-3.723</td>
<td align="center">0.0002029</td>
</tr>
<tr class="even">
<td align="center"><strong>(Intercept)</strong></td>
<td align="center">38.37</td>
<td align="center">9.564</td>
<td align="center">4.012</td>
<td align="center">6.254e-05</td>
</tr>
</tbody>
</table>

<table style="width:85%;">
<caption>Fitting linear model: biden ~ age + educ + age * educ</caption>
<colgroup>
<col width="20%" />
<col width="30%" />
<col width="11%" />
<col width="22%" />
</colgroup>
<thead>
<tr class="header">
<th align="center">Observations</th>
<th align="center">Residual Std. Error</th>
<th align="center"><span class="math inline"><em>R</em><sup>2</sup></span></th>
<th align="center">Adjusted <span class="math inline"><em>R</em><sup>2</sup></span></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td align="center">1807</td>
<td align="center">23.27</td>
<td align="center">0.01756</td>
<td align="center">0.01592</td>
</tr>
</tbody>
</table>

``` r
# function to get point estimates and standard errors
# model - lm object
# mod_var - name of moderating variable in the interaction
instant_effect <- function(model, mod_var){
  # get interaction term name
  int.name <- names(model$coefficients)[[which(str_detect(names(model$coefficients), ":"))]]
  
  marg_var <- str_split(int.name, ":")[[1]][[which(str_split(int.name, ":")[[1]] != mod_var)]]
  
  # store coefficients and covariance matrix
  beta.hat <- coef(model)
  cov <- vcov(model)
  
  # possible set of values for mod_var
  if(class(model)[[1]] == "lm"){
    z <- seq(min(model$model[[mod_var]]), max(model$model[[mod_var]]))
  } else {
    z <- seq(min(model$data[[mod_var]]), max(model$data[[mod_var]]))
  }
  
  # calculate instantaneous effect
  dy.dx <- beta.hat[[marg_var]] + beta.hat[[int.name]] * z
  
  # calculate standard errors for instantaeous effect
  se.dy.dx <- sqrt(cov[marg_var, marg_var] +
                     z^2 * cov[int.name, int.name] +
                     2 * z * cov[marg_var, int.name])
  
  # combine into data frame
  data_frame(z = z,
             dy.dx = dy.dx,
             se = se.dy.dx)
}
```

After applying listwise missing value deletion, the above model is estimated with 1,807 observations, `age`, `female` (gender), and interaction term of `age` and `female` as predictor variables, and `biden` (Joe Biden feeling thermometer) as the outcome variable.

Estimated parameters, standard errors, and significance are reported in the above table. Generally, all coefficients, including the interaction term of `age` and `female`, in this model are significant (all p-value &lt; 0.05).

Observerd by coefficient of the interaction term (-0.048), the marginal effect of age on Joe Biden thermometer rating goes down and goes negative when the education goes up, and the marginal effect of education on Joe Biden thermometer rating goes down and negative when the age goes up. Statistically, these two effects of different directions are equivelent. However, theoretically, I would stand for the first effect, the marginal effect of age on Joe Biden thermometer rating goes down when the education goes up. As people getting more education, their judgment can be more stable, and less influenced by emotions, body physical conditions, and other factors varied across people.

### 1. Evaluate the marginal effect of age on Joe Biden thermometer rating, conditional on education. Consider the magnitude and direction of the marginal effect, as well as its statistical significance.

``` r
#Discrete plot
instant_effect(lm_2, "educ") %>%
  ggplot(aes(z, dy.dx,
             ymin = dy.dx - 1.96 * se,
             ymax = dy.dx + 1.96 * se)) +
  geom_pointrange() +
  geom_hline(yintercept = 0, linetype = 2) +
  labs(title = "Marginal effect of age",
       subtitle = "By education",
       x = "Education",
       y = "Estimated marginal effect")
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P2-1%20Graph-1.png)

``` r
#Line plot
instant_effect(lm_2, "educ") %>%
  ggplot(aes(z, dy.dx)) +
  geom_line() +
  geom_line(aes(y = dy.dx - 1.96 * se), linetype = 2) +
  geom_line(aes(y = dy.dx + 1.96 * se), linetype = 2) +
  geom_hline(yintercept = 0) +
  labs(title = "Marginal effect of age",
       subtitle = "By education",
       x = "Education",
       y = "Estimated marginal effect")
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P2-1%20Graph-2.png)

Conditional on education, the marginal effect of age on Joe Biden thermometer rating are plotted as above. Conforming to what we observed from the estimated coefficient, the marginal effect of age goes down and eventually negative when education goes up (going from 0.65 to -0.15). From the plots, we can observe that this marginal effect is non-significant (can not tell if not different from zero) when the education is at levels between 13 and 16, while significant at other levels of education.

``` r
linearHypothesis(lm_2, "age + 12 * age:educ")
```

    ## Linear hypothesis test
    ## 
    ## Hypothesis:
    ## age  + 12 age:educ = 0
    ## 
    ## Model 1: restricted model
    ## Model 2: biden ~ age + educ + age * educ
    ## 
    ##   Res.Df    RSS Df Sum of Sq    F Pr(>F)   
    ## 1   1804 980731                            
    ## 2   1803 976688  1      4043 7.46 0.0064 **
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

``` r
linearHypothesis(lm_2, "age + 13 * age:educ")
```

    ## Linear hypothesis test
    ## 
    ## Hypothesis:
    ## age  + 13 age:educ = 0
    ## 
    ## Model 1: restricted model
    ## Model 2: biden ~ age + educ + age * educ
    ## 
    ##   Res.Df    RSS Df Sum of Sq    F Pr(>F)
    ## 1   1804 977833                         
    ## 2   1803 976688  1      1145 2.11   0.15

``` r
linearHypothesis(lm_2, "age + 14 * age:educ")
```

    ## Linear hypothesis test
    ## 
    ## Hypothesis:
    ## age  + 14 age:educ = 0
    ## 
    ## Model 1: restricted model
    ## Model 2: biden ~ age + educ + age * educ
    ## 
    ##   Res.Df    RSS Df Sum of Sq  F Pr(>F)
    ## 1   1804 976688                       
    ## 2   1803 976688  1     0.158  0   0.99

``` r
linearHypothesis(lm_2, "age + 15 * age:educ")
```

    ## Linear hypothesis test
    ## 
    ## Hypothesis:
    ## age  + 15 age:educ = 0
    ## 
    ## Model 1: restricted model
    ## Model 2: biden ~ age + educ + age * educ
    ## 
    ##   Res.Df    RSS Df Sum of Sq    F Pr(>F)
    ## 1   1804 977420                         
    ## 2   1803 976688  1       732 1.35   0.25

``` r
linearHypothesis(lm_2, "age + 16 * age:educ")
```

    ## Linear hypothesis test
    ## 
    ## Hypothesis:
    ## age  + 16 age:educ = 0
    ## 
    ## Model 1: restricted model
    ## Model 2: biden ~ age + educ + age * educ
    ## 
    ##   Res.Df    RSS Df Sum of Sq    F Pr(>F)  
    ## 1   1804 978641                           
    ## 2   1803 976688  1      1953 3.61  0.058 .
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

``` r
linearHypothesis(lm_2, "age + 17 * age:educ")
```

    ## Linear hypothesis test
    ## 
    ## Hypothesis:
    ## age  + 17 age:educ = 0
    ## 
    ## Model 1: restricted model
    ## Model 2: biden ~ age + educ + age * educ
    ## 
    ##   Res.Df    RSS Df Sum of Sq    F Pr(>F)  
    ## 1   1804 979699                           
    ## 2   1803 976688  1      3011 5.56  0.019 *
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

``` r
linearHypothesis(lm_2, "age + 18 * age:educ")
```

    ## Linear hypothesis test
    ## 
    ## Hypothesis:
    ## age  + 18 age:educ = 0
    ## 
    ## Model 1: restricted model
    ## Model 2: biden ~ age + educ + age * educ
    ## 
    ##   Res.Df    RSS Df Sum of Sq    F Pr(>F)   
    ## 1   1804 980503                            
    ## 2   1803 976688  1      3815 7.04  0.008 **
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

``` r
dim(filter(df, educ >= 13 & educ <= 16))[1] / dim(df)[1]
```

    ## [1] 0.446

Linear hypothesis tests at different levels of education are performed for quick examining the marginal effect of age. The results confirm our observation in the previous plots that the marginal effect is not significant when education is around 13 to 16 (p-value &gt; 0.05), and the marginal effect is significant at other levels of education (p-value &lt; 0.05). Around 44.6% of all observations fall in the insignificant range. In other words, it is noteworthy that the marginal effect of age is not significant for quite a large proportion of the observations as the direct effect and interaction effect counteract each other.

### 2. Evaluate the marginal effect of education on Joe Biden thermometer rating, conditional on age. Consider the magnitude and direction of the marginal effect, as well as its statistical significance.

``` r
#Discrete plot
instant_effect(lm_2, "age") %>%
  ggplot(aes(z, dy.dx,
             ymin = dy.dx - 1.96 * se,
             ymax = dy.dx + 1.96 * se)) +
  geom_pointrange() +
  geom_hline(yintercept = 0, linetype = 2) +
  labs(title = "Marginal effect of education",
       subtitle = "By age",
       x = "Age",
       y = "Estimated marginal effect")
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P2-2%20Graph-1.png)

``` r
#Line plot
instant_effect(lm_2, "age") %>%
  ggplot(aes(z, dy.dx)) +
  geom_line() +
  geom_line(aes(y = dy.dx - 1.96 * se), linetype = 2) +
  geom_line(aes(y = dy.dx + 1.96 * se), linetype = 2) +
  geom_hline(yintercept = 0) +
  labs(title = "Marginal effect of education",
       subtitle = "By age",
       x = "Age",
       y = "Estimated marginal effect")
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P2-2%20Graph-2.png)

Conditional on age, the marginal effect of education on Joe Biden thermometer rating are plotted as above. Conforming to what we observed from the estimated coefficient, the marginal effect of education goes down and eventually negative when education goes up (going from 1.8 to -2.8). From the plots, we cab observe that this marginal effect is non-significant (can not tell if not different from zero) when the age is at levels lower than 45 while significant at other levels of age.

``` r
linearHypothesis(lm_2, "educ + 20 * age:educ")
```

    ## Linear hypothesis test
    ## 
    ## Hypothesis:
    ## educ  + 20 age:educ = 0
    ## 
    ## Model 1: restricted model
    ## Model 2: biden ~ age + educ + age * educ
    ## 
    ##   Res.Df    RSS Df Sum of Sq    F Pr(>F)
    ## 1   1804 977847                         
    ## 2   1803 976688  1      1159 2.14   0.14

``` r
linearHypothesis(lm_2, "educ + 25 * age:educ")
```

    ## Linear hypothesis test
    ## 
    ## Hypothesis:
    ## educ  + 25 age:educ = 0
    ## 
    ## Model 1: restricted model
    ## Model 2: biden ~ age + educ + age * educ
    ## 
    ##   Res.Df    RSS Df Sum of Sq    F Pr(>F)
    ## 1   1804 977326                         
    ## 2   1803 976688  1       638 1.18   0.28

``` r
linearHypothesis(lm_2, "educ + 30 * age:educ")
```

    ## Linear hypothesis test
    ## 
    ## Hypothesis:
    ## educ  + 30 age:educ = 0
    ## 
    ## Model 1: restricted model
    ## Model 2: biden ~ age + educ + age * educ
    ## 
    ##   Res.Df    RSS Df Sum of Sq    F Pr(>F)
    ## 1   1804 976876                         
    ## 2   1803 976688  1       188 0.35   0.56

``` r
linearHypothesis(lm_2, "educ + 35 * age:educ")
```

    ## Linear hypothesis test
    ## 
    ## Hypothesis:
    ## educ  + 35 age:educ = 0
    ## 
    ## Model 1: restricted model
    ## Model 2: biden ~ age + educ + age * educ
    ## 
    ##   Res.Df    RSS Df Sum of Sq    F Pr(>F)
    ## 1   1804 976691                         
    ## 2   1803 976688  1         3 0.01   0.94

``` r
linearHypothesis(lm_2, "educ + 40 * age:educ")
```

    ## Linear hypothesis test
    ## 
    ## Hypothesis:
    ## educ  + 40 age:educ = 0
    ## 
    ## Model 1: restricted model
    ## Model 2: biden ~ age + educ + age * educ
    ## 
    ##   Res.Df    RSS Df Sum of Sq   F Pr(>F)
    ## 1   1804 977178                        
    ## 2   1803 976688  1       490 0.9   0.34

``` r
linearHypothesis(lm_2, "educ + 45 * age:educ")
```

    ## Linear hypothesis test
    ## 
    ## Hypothesis:
    ## educ  + 45 age:educ = 0
    ## 
    ## Model 1: restricted model
    ## Model 2: biden ~ age + educ + age * educ
    ## 
    ##   Res.Df    RSS Df Sum of Sq    F Pr(>F)  
    ## 1   1804 978970                           
    ## 2   1803 976688  1      2282 4.21   0.04 *
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

``` r
linearHypothesis(lm_2, "educ + 50 * age:educ")
```

    ## Linear hypothesis test
    ## 
    ## Hypothesis:
    ## educ  + 50 age:educ = 0
    ## 
    ## Model 1: restricted model
    ## Model 2: biden ~ age + educ + age * educ
    ## 
    ##   Res.Df    RSS Df Sum of Sq    F Pr(>F)   
    ## 1   1804 982457                            
    ## 2   1803 976688  1      5770 10.6 0.0011 **
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

``` r
dim(filter(df, age <= 45))[1] / dim(df)[1]
```

    ## [1] 0.4671

Linear hypothesis tests at different levels of education are performed for quick examining the marginal effect of education. The results confirm our observation in the previous plots that the marginal effect is significant when age is higher than 45 (p-value &lt; 0.05) and not significant when age is below 45 (p-value &gt; 0.05). Again, around 46.7% of all observations fall in this insignificant range. In other words, it is noteworthy that the marginal effect of education is not significant for quite a large proportion of the observations as the direct effect and interaction effect counteract each other.

Part 3: Missing data
--------------------

``` r
df_mi <- read_csv("data/biden.csv") %>%
  rownames_to_column(var="row")
```

    ## Parsed with column specification:
    ## cols(
    ##   biden = col_integer(),
    ##   female = col_integer(),
    ##   age = col_integer(),
    ##   educ = col_integer(),
    ##   dem = col_integer(),
    ##   rep = col_integer()
    ## )

### Use multiple imputation to account for the missingness in the data. Consider the multivariate normality assumption and transform any variables as you see fit for the imputation stage.

``` r
mi_all <- amelia(as.data.frame(df_mi), m=5, idvars=c("row"))
```

    ## -- Imputation 1 --
    ## 
    ##   1  2  3  4  5  6
    ## 
    ## -- Imputation 2 --
    ## 
    ##   1  2  3  4  5  6
    ## 
    ## -- Imputation 3 --
    ## 
    ##   1  2  3  4  5
    ## 
    ## -- Imputation 4 --
    ## 
    ##   1  2  3  4  5
    ## 
    ## -- Imputation 5 --
    ## 
    ##   1  2  3  4  5  6

``` r
missmap(mi_all)
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P3%20Observe-1.png)

``` r
models_imp <- data_frame(data=mi_all$imputations) %>%
  mutate(model=map(data, ~ lm(biden ~ age + female + educ,
                                data = .x)),
         coef = map(model, tidy)) %>%
  unnest(coef, .id = "id")
models_imp
```

    ## # A tibble: 20 × 6
    ##       id        term estimate std.error statistic    p.value
    ##    <chr>       <chr>    <dbl>     <dbl>     <dbl>      <dbl>
    ## 1   imp1 (Intercept) 67.35363   3.01354   22.3503 2.280e-100
    ## 2   imp1         age  0.02591   0.02795    0.9273  3.539e-01
    ## 3   imp1      female  5.11034   0.97283    5.2531  1.632e-07
    ## 4   imp1        educ -0.70737   0.18728   -3.7771  1.627e-04
    ## 5   imp2 (Intercept) 66.08639   2.99744   22.0476  5.880e-98
    ## 6   imp2         age  0.05595   0.02783    2.0103  4.451e-02
    ## 7   imp2      female  6.21042   0.96711    6.4217  1.630e-10
    ## 8   imp2        educ -0.74584   0.18613   -4.0071  6.340e-05
    ## 9   imp3 (Intercept) 66.40752   3.03535   21.8781  1.291e-96
    ## 10  imp3         age  0.06432   0.02812    2.2878  2.224e-02
    ## 11  imp3      female  5.51866   0.97737    5.6465  1.838e-08
    ## 12  imp3        educ -0.79952   0.18844   -4.2428  2.294e-05
    ## 13  imp4 (Intercept) 65.55167   3.00958   21.7810  7.515e-96
    ## 14  imp4         age  0.05432   0.02791    1.9461  5.177e-02
    ## 15  imp4      female  5.98561   0.97134    6.1622  8.434e-10
    ## 16  imp4        educ -0.71724   0.18707   -3.8340  1.294e-04
    ## 17  imp5 (Intercept) 66.94334   3.01251   22.2217  2.425e-99
    ## 18  imp5         age  0.05774   0.02791    2.0689  3.867e-02
    ## 19  imp5      female  6.36946   0.97008    6.5659  6.360e-11
    ## 20  imp5        educ -0.83089   0.18684   -4.4469  9.121e-06

First, the multiple imputation is performed based on all variables available in the dataset. The missingness map is drawn, from which we observe that most of the missing values occur in the variable `baiden`.

``` r
ggpairs(select_if(df_mi, is.numeric))
```

    ## Warning: Removed 460 rows containing non-finite values (stat_density).

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 460 rows containing missing values

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 493 rows containing missing values

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 469 rows containing missing values

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 481 rows containing missing values

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 481 rows containing missing values

    ## Warning: Removed 460 rows containing missing values (geom_point).

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 46 rows containing missing values

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 11 rows containing missing values

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 33 rows containing missing values

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 33 rows containing missing values

    ## Warning: Removed 493 rows containing missing values (geom_point).

    ## Warning: Removed 46 rows containing missing values (geom_point).

    ## Warning: Removed 46 rows containing non-finite values (stat_density).

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 51 rows containing missing values

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 76 rows containing missing values

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 76 rows containing missing values

    ## Warning: Removed 469 rows containing missing values (geom_point).

    ## Warning: Removed 11 rows containing missing values (geom_point).

    ## Warning: Removed 51 rows containing missing values (geom_point).

    ## Warning: Removed 11 rows containing non-finite values (stat_density).

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 43 rows containing missing values

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 43 rows containing missing values

    ## Warning: Removed 481 rows containing missing values (geom_point).

    ## Warning: Removed 33 rows containing missing values (geom_point).

    ## Warning: Removed 76 rows containing missing values (geom_point).

    ## Warning: Removed 43 rows containing missing values (geom_point).

    ## Warning: Removed 33 rows containing non-finite values (stat_density).

    ## Warning in (function (data, mapping, alignPercent = 0.6, method =
    ## "pearson", : Removed 33 rows containing missing values

    ## Warning: Removed 481 rows containing missing values (geom_point).

    ## Warning: Removed 33 rows containing missing values (geom_point).

    ## Warning: Removed 76 rows containing missing values (geom_point).

    ## Warning: Removed 43 rows containing missing values (geom_point).

    ## Warning: Removed 33 rows containing missing values (geom_point).

    ## Warning: Removed 33 rows containing non-finite values (stat_density).

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P3%20Variable%20Identification-1.png)

To select proper variables in estimating imputation values, a correlation matrix and pair-wise scatter plots are applied. I suggest to include `dem` and `rep` in estimating values for multiple imputation, even though they are not included in our regression model. Because the two variables are moderately correlated with `biden` (corr = 0.461 and -0.421, respectively), the variable with most missing values. In addition, all other variables in the original regression model will be included as well, including `female`, `age`, and `educ`.

In the distribution plot shown above, except three binary variables, we also observe some variables not conforming to normal distribution, such as `biden`, skewed to the left, and `age`, skewed to the right.

``` r
mi_transformed <- amelia(as.data.frame(df_mi), m=5, idvars=c("row"),
                      logs=c("age"),
                      sqrts=c("biden"),
                      noms=c("dem", "rep", "female"))
```

    ## -- Imputation 1 --
    ## 
    ##   1  2  3  4  5
    ## 
    ## -- Imputation 2 --
    ## 
    ##   1  2  3  4  5  6
    ## 
    ## -- Imputation 3 --
    ## 
    ##   1  2  3  4  5  6
    ## 
    ## -- Imputation 4 --
    ## 
    ##   1  2  3  4  5  6
    ## 
    ## -- Imputation 5 --
    ## 
    ##   1  2  3  4  5

To tackle the non-normal problem, I do a log transformation to `age`, and a squared-root transformation to `biden`. In addition, I mark `female`, `dem`, and `rep` as nominal variables when implementing Amelia's Multiple Imputation.

### Calculate appropriate estimates of the parameters and the standard errors. Explain how the results differ from the original, non-imputed model.

``` r
models_trans_imp <- data_frame(data=mi_transformed$imputations) %>%
  mutate(model=map(data, ~ lm(biden ~ age + female + educ,
                                data = .x)),
         coef = map(model, tidy)) %>%
  unnest(coef, .id = "id")
models_trans_imp
```

    ## # A tibble: 20 × 6
    ##       id        term estimate std.error statistic   p.value
    ##    <chr>       <chr>    <dbl>     <dbl>     <dbl>     <dbl>
    ## 1   imp1 (Intercept) 66.95164   3.14208    21.308 3.724e-92
    ## 2   imp1         age  0.05752   0.02908     1.978 4.810e-02
    ## 3   imp1      female  6.03791   1.01181     5.967 2.780e-09
    ## 4   imp1        educ -0.82807   0.19487    -4.249 2.228e-05
    ## 5   imp2 (Intercept) 68.95423   3.24410    21.255 9.555e-92
    ## 6   imp2         age  0.04009   0.03008     1.333 1.827e-01
    ## 7   imp2      female  6.59360   1.04608     6.303 3.480e-10
    ## 8   imp2        educ -0.89433   0.20161    -4.436 9.595e-06
    ## 9   imp3 (Intercept) 66.60548   3.13466    21.248 1.087e-91
    ## 10  imp3         age  0.06460   0.02876     2.246 2.481e-02
    ## 11  imp3      female  5.60594   1.01311     5.533 3.495e-08
    ## 12  imp3        educ -0.81284   0.19540    -4.160 3.302e-05
    ## 13  imp4 (Intercept) 65.36487   3.20148    20.417 2.415e-85
    ## 14  imp4         age  0.03556   0.02941     1.209 2.269e-01
    ## 15  imp4      female  5.06139   1.03265     4.901 1.018e-06
    ## 16  imp4        educ -0.59752   0.19897    -3.003 2.701e-03
    ## 17  imp5 (Intercept) 65.71434   3.14065    20.924 3.414e-89
    ## 18  imp5         age  0.04848   0.02912     1.665 9.611e-02
    ## 19  imp5      female  5.40296   1.01389     5.329 1.083e-07
    ## 20  imp5        educ -0.69170   0.19493    -3.548 3.953e-04

``` r
mi.meld.plus <- function(df_tidy){
  # transform data into appropriate matrix shape
  coef.out <- df_tidy %>%
    select(id:estimate) %>%
    spread(term, estimate) %>%
    select(-id)
  
  se.out <- df_tidy %>%
    select(id, term, std.error) %>%
    spread(term, std.error) %>%
    select(-id)
  
  combined.results <- mi.meld(q = coef.out, se = se.out)
  
  data_frame(term = colnames(combined.results$q.mi),
             estimate.mi = combined.results$q.mi[1, ],
             std.error.mi = combined.results$se.mi[1, ])
}


# compare results
tidy(lm_1) %>%
  left_join(mi.meld.plus(models_trans_imp)) %>%
  select(-statistic, -p.value)
```

    ## Joining, by = "term"

    ##          term estimate std.error estimate.mi std.error.mi
    ## 1 (Intercept) 68.62101   3.59600    66.71811      3.52691
    ## 2         age  0.04188   0.03249     0.04925      0.03211
    ## 3      female  6.19607   1.09670     5.74036      1.21268
    ## 4        educ -0.88871   0.22469    -0.76489      0.23623

``` r
# cheating on my confidence intervals for this plot
bind_rows(orig = tidy(lm_1),
          full_imp = mi.meld.plus(models_imp) %>%
            rename(estimate = estimate.mi,
                   std.error = std.error.mi),
          trans_imp = mi.meld.plus(models_trans_imp) %>%
            rename(estimate = estimate.mi,
                   std.error = std.error.mi),
          .id = "method") %>%
  mutate(method = factor(method, levels = c("orig", "full_imp", "trans_imp"),
                         labels = c("Listwise deletion", "Full imputation",
                                    "Transformed imputation")),
         term = factor(term, levels = c("(Intercept)", "age", "female", "educ"),
                       labels = c("(Intercept)", "Age", "Female", "Education"))) %>%
  ggplot(aes(fct_rev(term), estimate, color = fct_rev(method),
             ymin = estimate - 1.96 * std.error,
             ymax = estimate + 1.96 * std.error)) +
  geom_hline(yintercept = 0, linetype = 2) +
  geom_pointrange(position = position_dodge(.75)) +
  coord_flip() +
  scale_color_discrete(guide = guide_legend(reverse = TRUE)) +
  labs(title = "Comparing regression results",
       x = NULL,
       y = "Estimated parameter",
       color = NULL) +
  theme(legend.position = "bottom")
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P3%20Model-1.png)

``` r
#Remove intercept
bind_rows(orig = tidy(lm_1),
          full_imp = mi.meld.plus(models_imp) %>%
            rename(estimate = estimate.mi,
                   std.error = std.error.mi),
          trans_imp = mi.meld.plus(models_trans_imp) %>%
            rename(estimate = estimate.mi,
                   std.error = std.error.mi),
          .id = "method") %>%
  mutate(method = factor(method, levels = c("orig", "full_imp", "trans_imp"),
                         labels = c("Listwise deletion", "Full imputation",
                                    "Transformed imputation")),
         term = factor(term, levels = c("(Intercept)", "age", "female", "educ"),
                       labels = c("(Intercept)", "Age", "Female", "Education"))) %>%
  filter(term != "(Intercept)") %>%
  ggplot(aes(fct_rev(term), estimate, color = fct_rev(method),
             ymin = estimate - 1.96 * std.error,
             ymax = estimate + 1.96 * std.error)) +
  geom_hline(yintercept = 0, linetype = 2) +
  geom_pointrange(position = position_dodge(.75)) +
  coord_flip() +
  scale_color_discrete(guide = guide_legend(reverse = TRUE)) +
  labs(title = "Comparing regression results",
       x = NULL,
       y = "Estimated parameter",
       color = NULL) +
  theme(legend.position = "bottom")
```

![](PS3_-_Chih-Yu_Chiang_files/figure-markdown_github/P3%20Model-2.png)

The coefficient estimates (estimate.mi) and standard errors (std.error.mi) from the imputed data are presented as above.

The estimated coefficients are visualized and compared in the above graphs. As observed, when compared to the original, non-imputed model, absolute value of the intercept goes down a little bit; with a higher standard error, the intercept is a little bit less significant to be different from 0. Absolute value of the parameter for `age` is slightly larger; with an slightly lower standard error, the parameter is a bit more significant to be different from 0. Absolute value of the parameter for `female` goes down around 10%; with a slightly higher standard error, the parameter is slightly less significant to be different from 0. Finally, absolute value of the parameter for `educ` goes down 20%; as the standard error increases, the parameter is less significant to be different from 0.
