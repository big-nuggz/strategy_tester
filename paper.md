# Time in the DCA Beats Timing the DCA?

- Published: 22nd of August, 2026
- Author: Mika Novakovic

## 1. Abstract

I've built a stock index investment strategy tester in Python to test a  timing strategy stemming from an idea[^1]; **what if you do DCA (dollar cost averaging), but reserve a portion of your contributions during market highs, so that you can invest more during the drawdowns?** The answer was disappointing (as these things usually are).

The results essentially confirms the famous line in the world of investment, **"time in the market beats timing the market"**. The uninvested cash suffers from cash drag, which can significantly reduce the final returns of any timing based strategies.

Lump sum investment is known to be statistically superior to most passive investment strategies in the long term, as it was also confirmed in this paper, while the DCA being the next best thing. The proposed strategy over all ended up being a slightly worse version of the simple DCA, though it interestingly doesn't fall too far behind the DCA's performance.

## 2. Method

### 2.1. Dataset

I've used set of two historical S&P DJI 500 U.S. stock index data to back test the investment strategies. First dataset is the price only version that excludes the dividends. This data was obtained from Yahoo Finance with the ticker symbol **^GSPC**. The prices for this dataset have been retroactively calculated to include period that predates the index itself, starting from 1927.

The other one is more recent index, S&P 500 Total Return. The key difference from the price only index is that it includes dividend reinvestment. Dividends play a huge role in real investment, so it is a more practical data for the purpose of back testing. The downside of this dataset is that it only goes back to 1988, so the dataset is much smaller than the price only version. The data was once again obtained from Yahoo Finance with the ticker symbol **^SP500TR**.

For both indices, I've used 10 year period rolling window with a stride of 1 year to extract the individual test samples. The first starting year was set to be 1 year after the first available year (1928 for the price only, 1989 for the total return) to avoid partial years. Last starting year to be 2015 for the same reason, to ensure the full 10 year period was available across every samples. The resulting datasets contained 88 samples for the price only, and 27 samples for the total return.

### 2.2. Strategies

Three different strategies were tested, with two of them being the benchmark. The three strategies are "Buy and Hold", "DCA" and "Timed DCA" (proposed strategy). All strategies receive the same initial budget, but the timing of investment differs.

Buy and Hold is simple lump sum investment. It invests the entire budget on day one, then simply holds until end of investment period. It is not a practical benchmark, since most investors lack the fund to invest all future contributions on day one.

DCA stands for dollar cost averaging. This strategy invests steady contributions until the target total contribution is achieved. This strategy mimics what most investors do in their real investments, and is more useful as a benchmark to compare against the proposed strategy, which itself is a modified version of the DCA.

The proposed strategy, Timed DCA, is similar to simple DCA in that there's a steady contribution every month. The difference, is that it doesn't invest all the fund available each month. Instead, it withholds portion of the fund as cash reserve while the market is near the recent high. When the index price falls below the recent high at a certain threshold, the entire cash reserve is invested along with the regular contribution. The aim of the proposed strategy is to increase the final return by "buying the dip", while also cushioning the uninvested cash drag by having the steady contribution happening in the background, regardless of the market conditions.

## 3. Experiment

With both of the datasets, all three strategies were tested for every sample, then the statistic metrics were calculated from all the results. Metrics are; mean final 10 year return, mean compound annual growth rate (CAGR) obtained from the mean 10 year return, minimum 10 year return, maximum 10 year return, and the standard deviation of all 10 year returns.

DCA and Timed DCA strategies both take same parameter, number of years to spread the investments across. It was set to first 5 years out of 10 year period, for both. Timed DCA strategy additionally takes three parameters; portion of regular contributions, threshold for cash reserve investment relative to the market high, and period to calculate the market high. 12 months (approximation of the widely used 52 weeks) was used as the market high reference period. For the rest of the parameters, a parameter sweep was performed with the regular contribution portion varying from 20%-80%, and the price dip threshold varying from 95% (5% drop from high) to 99% (1% drop from high).

## 4. Results

<figure>
  <img src="fig4.1.png" alt="heatmap of parameter sweep, price only">
  <figption><em><b>Figure 4.1.</b> Parameter sweep heatmap of Timed DCA strategy 10 year returns. S&P 500 price only data.</em></figcaption>
</figure>

<figure>
  <img src="fig4.2.png" alt="heatmap of parameter sweep, total return">
  <figption><em><b>Figure 4.2.</b> Parameter sweep heatmap of Timed DCA strategy 10 year returns. S&P 500 total return data.</em></figcaption>
</figure>

**Figure 4.1.** and **Figure 4.2.** shows parameter sweep heatmaps of Timed DCA strategy tested on the S&P 500 dataset. For both of the figures, the X axis represents the portion of monthly contribution that is invested regardless of the market condition, and the Y axis represents the threshold for the index price dip.

**Table 4.1.** and **Table 4.2.** shows summary of the statistical metrics for the price only S&P 500 index, and the total return S&P 500 index, respectively. For the Timed DCA strategy, only the results from the best parameter combination are shown in the tables. The best parameters were 80% regular contributions with dip buying threshold of 99% from the 12 months high, for both the price only dataset and the total return dataset.

<p align="center">
  <b>Table 4.1:</b> Summary of results, S&P 500 price only from year 1928 to 2025 in 10 year rolling window. The best value for each statistic metrics are shown in bold.
</p>

| Strategy | Mean 10 Year Return | Minimum 10 Year Return | Maximum 10 Year Return | Std. Deviation | Mean CAGR |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Buy and Hold | **109.77%** | -47.04% | **342.61%** | 92.36% | **7.69%** |
| DCA | 78.00% | -25.17% | 265.75% | **61.86%** | 5.94% |
| **Timed DCA** (best run) | 77.80% | **-25.08%** | 266.04% | 61.87% | 5.92% |

<p align="center">
  <b>Table 4.2:</b> Summary of results, S&P 500 total return from year 1989 to 2025 in 10 year rolling window. The best value for each statistic metrics are shown in bold.
</p>

| Strategy | Mean 10 Year Return | Minimum 10 Year Return | Maximum 10 Year Return | Std. Deviation | Mean CAGR |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Buy and Hold | **129.51%** | -26.52% | **342.61%** | 98.91% | **8.66%** |
| DCA | 89.69% | **-21.36%** | 265.75% | **70.64%** | 6.61% |
| **Timed DCA** (best run) | 89.44% | -21.45% | 266.04% | 70.72% | 6.60% |

The best mean 10 year return for both of the datasets were achieved by the Buy and Hold strategy, as expected. The simple DCA performed slightly better than the Timed DCA in both datasets. Both the DCA and Timed DCA achieved similarly low standard deviation compared to the Buy and Hold strategy across datasets, but especially in the price only dataset.

Over the long period of price only S&P 500 data, Buy and Hold strategy had significantly worse minimum 10 year return compared to other strategies. This is likely because the price only dataset includes a period during the Great Depression, where the U.S. stock market underperformed significantly.

Timed DCA strategy underperformed all strategies in almost all metrics, except for the minimum 10 year return in the price only dataset. The difference between the DCA and the Timed DCA's mean 10 year returns were less than 0.5% in both datasets, and over all, DCA and Timed DCA performed similarly across datasets.

## 5. Analysis

The heatmaps in both **Figure 4.1.** and **Figure 4.2.** clearly shows that there are positive correlations between both parameters and the strategy performance. Higher values for both of these parameters make the Timed DCA behave more like the standard DCA, and that is also evident from the fact that there are minimal differences between the performance of the DCA and the Timed DCA, at its highest performing set of parameters.

The results shows that the more the Timed DCA focuses its monthly contributions towards timing the market, the less it performs against the simple DCA. It also shows that the more it waits for the larger dip, the worse it performs. This can be explained by the fact that the S&P 500 index has a strong upwards bias in the long term. The market could keep breaking its 12 months high for many months consecutively without significant dips, in which period the Timed DCA strategy will suffer from uninvested cash drag. The DCA also suffers from the same cash drag, which is why it also underperforms the Buy and Hold strategy. This effect seems to negate any edge gained by the Timed DCA strategy buying the dips, though not by a significant margin compared to the DCA.

## 6. Conclusion

There doesn't seem to be any advantages from using the Timed DCA strategy instead of the simple DCA strategy. The effect of uninvested cash drag is a significant challenge in any timed investment strategies, and the more the strategy tries to time the dip, the more it suffers from it.

In the context of real investment, lump sum investment is almost never possible. This is because it assumes you have all the funds you'll ever invest ready on hand in the first day of investment. The most similar practical strategy is investing everything you can, the moment you have the money for it. In other words, a distributed lump sum investment. Which is more or less what the simple DCA strategy is.

The big question was, **is it possible to beat this standard strategy by introducing a rule based timing?** And the answer seems to be a disappointing **no**, at least, not in this way.

One major caveat of this paper is that the strategies were only tested for the S&P 500 index, which only includes the stocks from U.S. market. Not all stock markets perform the same across the world; Japanese TOPIX and Nikkei 225 index had decades long period of sideways price movement for example. Although, in the century-level long term, almost all of the broad market stock indices tends to have the similar upwards bias to S&P 500, as they roughly track the economic growth of the nations they represent. The proposed strategy could possibly perform well in the long stretch of volatile and sideways moving market conditions, but even in such case, the simple DCA might simply be superior. 

## References

[^1]: It was revealed to me in a dream.