# AYX 
Sauls coverage starts around: #34874

## My understanding
Alteryx lets you hook up a wide variety of datasources (your own databases, google analytics, salesforce, etc), clean up the data, mash it all together, cut and filter and slice and dice, and then perform a variety of analyses on them. Excel stuff sure, but also think regression models, AB tests, etc. The more advanced stuff that Excel would struggle with, and Excel doesn't do connection and cleanup well.

Alteryx sits in this junction, enabling collection of data, and analysis in one place. It's not strong in visualisation, but it seems unlikely that visualisation is a big part of the use case. Its more like a visual R or Python alternative with data combining and cleansing baked in.

> "The Alteryx platform provides the analytic flexibility that the 30 million business analysts and citizen data scientists, trained statisticians and IT professionals need, to create an operationalized analytic models through a collaborative, scalable and governed platform."

I wrote an initial pre-deep dive here:
(http://boards.fool.com/alteryx-write-up-all-in-one-place-32936733.aspx?sort=whole#32941965)

which looked at Tableau and Datawatch briefly. I've done some googling re: DataWatch, and their spiel seems to be "We're cheaper than Alteryx!" which means you should probably write them off.

From Googling, people seem to really like Alteryx.

As software goes, I don't think its particularly special in terms of functionality. I also don't think it is creating a new market, and similarly I don't think it has a TAM of "30 million users". However, what it does, _it seems to do very well_, which is a huge tick in my book.

My sense also is that its a product at the right place and time. I could easily imagine an Excel user being asked "what if we include this other variable in our analysis?"

### Pricing and TAM musings
Alteryx is a software-as-a-service offering, so they make money by subscriptions. The prices are pretty high ($5195USD/user) for Alteryx designer, which makes me doubt the "21 million business analysts, citizen data scientists, trained statisticians and IT professionals" they talk about, ie, ≅$100b market.

Also, thats just the base package. Spatial data cost a lot ($12k), demographic data costs even more ($34k), and even desktop scheduling which would be a trivial addition to the code base costs $6.5k per user per year?!? It seems to work for them and other products (eg: Talend) appear to have similar pricing.

It does restrict the TAM to companies with a reasonable budget for these kinds of tools, which is a little unclear.

Last quarter (Q1 2018) they reported revenue booked at 42.82m, and deferred revenue at $112m, so total 'bookable' revenue at **$155m**. CEO Dean Stoecker says "about half Designer and half Server in terms of revenue". So say 17,000 actual end-users. They say "close to 3700 active customers", so maybe average of 4-5 users per customer on average. Not sure any of that is relevant, but some colour.

## Customers

https://www.featuredcustomers.com/vendor/alteryx/customers

is a good resource. Looks like a who's who of some pretty big companies.


## Alteryx products

They have four products, Designer, Server, and the new Promote and Connect.


### Alteryx Designer

Their main product. That is, everything you do with Alteryx you do via the designer. Hook up designer to some datasources, drag-and-drop to clean, filter, and analyse, as well as produce basic reports.

The list of tool categories is:  

1. Input/Output - Getting data into and out of Alteryx. For example, connecting to databases. They also have a bunch of connectors to common datasources, including: AWS S3, Google Analytics, Marketo, MongoDB, SalesForce, SharePoint.
2. Preparation - Cleaning up your data. Filtering, calculated fields, sampling (useful for massive datasets), selects, sorting, de-duplications...
3. Join - Joining different tables and datasources. For example, you might want to grab your customer table, and join it to your addresses table, and then join to google analytics data. Also grouping, so common SQL tasks.
4. Predictive - **The meat (I think) of Alteryx**. Taking your prepared data and performing analysis (data mining) on it. Covers the "_what does my data look mean_" questions, and this is what Excel and databases can't do (some can, I believe Oracle and SQL-server have some support for this type of analysis). AB tests (comparing to previous time period), market basket analysis (eg: If I buy X, what am I also likely to buy?), regression models, decision trees, naive bayes, and also time series analysis.
5. Spatial - Polygons and maps. 
6. Investigation - Covers the "_what does my data look like_" questions. What data is missing? What correlations are there?
7. Parse and Transform

> What about pivot tables? Interestingly, Alteryx can't do this, at least not to Excel standard. You either have to export to a CSV and use Excel, or pipe it to a Tableau workbook. You can create a 'pivot table' using the table tool,but AFAIK you can't let users interact with it, so the filtering etc would need to be done beforehand.  

**NOTE: WINDOWS ONLY.** Even the server solution is expected to run on Windows. This suggests that Alteryx is an 'old' code-base (C++). However, they provide a Windows Server 2012 AWS AMI so you can run on AWS.


### Alteryx Server

Scale, share, automate, govern Alteryx workflows with people who don't have an Alteryx license. So create a workflow, add some interactive functionality (convert to Analytic App), and then publish to gallery (Alteryx server) which provides the browser front-end to all the published analytic apps.

Anyone can then run the workflow in the browser and see the report.

Also provides version control and scheduling for workflows. It seems a bit limited in terms of access control, but assume thats a pretty simple fix.


### Alteryx Connect

Connect is a clearing house for data and Alteryx workflows. It lets people in the organisation record datasources and workflows, comment on them, ask questions of users about them, and utilise them in their own Alteryx Designer sessions.

It's a wiki for data. Seems like a useful addition for larger organisations with large numbers of analysts and datasources, so theres a central knowledge base of datasources and Alteryx workflows.

Alteryx acquired Semanta in 2017, and I believe this IP is the basis of the Connect product.


### Alteryx Promote

Promote is cool. It lets people deploy Alteryx models into production so that other services can use the model. Essentially it sets up a remote web server that responds to web requests to use the model, as well as managing the process for getting that model into production, testing, versioning etc. All the things that tech would have to normally do (write the code, unit test, github, provision servers, deploy, rollback errors etc).

For example, you might have a mortgage estimator you want to put on your banks website so users can see how much they might borrow. The data people can publish that model with no (little) tech help, while tech build the user interface and model interface. 

Alteryx acquired ŷhat in 2017, and this IP is the basis of the Promote product.


### Comments

Promote in particular is interesting, because the use case is: getting your model into production. So not just internally, coming up with an analysis that you re-run every month to put in the CEO's report, but actually productionising your model so that other services (and users in the real world) can utilise it. 

At the moment, productionising models is a tech problem. Data people would come up with the model, and then chuck it over the wall to the tech people, who would (probably) have to recreate that model in their own deployment toolset (language, testing, deployment). Promote will give a lot more power to the data people to own and update their models.

So will be watching Promote uptake carefully. If Promote does well, that will be an excellent indication for Alteryx.

>Promote simplifies last-mile of analytics by allowing models to be deployed and scaled in minutes, not months. For example, in Q1, a current customer strategic funding expanded their footprint with Alteryx by adding Promote to their server implementation. They have been an Alteryx customer for almost three years, primarily running predictive models in R and Python through Alteryx Server to qualify hundreds of incoming applications on a daily basis and produce real-time scoring for pricing.


It's a good sign that the couple of acquisitions that Alteryx have made (ŷhat and Semanta) have been released as products soon after. Also, I think these acquisitions are very clear indication of where Alteryx expects their focus to be: Larger companies, managing their formatted data and analyses, and getting models into production. 


### Alteryx Designer 2
Very speculative on my part, but by perusing the careers page, theres a suggestion that they're rewriting Designer in web-based technologies.


## Tableau
Tableau is often the elephant in the room, but I'm not convinced its actually deserved. Tableau is (more or less) excellent visualisation software that takes a bunch of data (sometimes the output of Alteryx) and allows people to make pretty interactive analyses (graphs and tables), which can be shared for collaboration, reporting etc.

Tableau is reputedly not awesome at combining datasources, something which is Alteryx's bread and butter. The big question around Tableau is... how much of Alteryx's revenue is from the Alteryx+Tableau combination?

I also believe analyses will get more and more complicated, with larger numbers of variables. Humans deal well with two-dimensional data, deal ok with 3-dimensional data, 4D gets difficult, and anything above is pretty much impossible.

Visuals are designed for human decision making, but the explosion of variables that are being captured by businesses (IMO) don't lend themselves to visual decision making. More complicated analyses like multivariate-regression, decision trees and neural network classifiers deal much better with these sorts of complexities.


### Tableau: The bull case.

Tableau won't impact Alteryx much, because visuals are not a large part of their use-case.  CEO has stated that only about 15% of their output heads to Tableau (which sounds like a reasonable amount to me!)

Tableau Prep is only about data-prep, rather than Analysis, and much simpler than Alteryx.

As mentioned previously, visualisation is a limited market, and Alteryx are going after the data management and analysis market. The acquisitions of Semanta and ŷhat are examples of that.


### Tableau: The bear case

This move marks the first steps for Tableau eating Alteryx's lunch. Tableau Prep is only going to get better, and nothing that Alteryx does is particularly rocket science.

> This seems to be a common refrain from 'Alteryx versus Tableau prep' thread on the Tableau forums: "For me, Alteryx is the first choice though - it's just so **** simple and easy to use, but at the same time so powerful."
 

My personal take is that Alteryx's big growth will come from more complicated analyses. Then you start to get into the Datarobot space, so worth watching how that develops.

Also...plot.ly.

## Related companies

### plot.ly
Check out Alteryx's collaboration with plot.ly:
[plot.ly collaboration PR](https://www.alteryx.com/press-releases/alteryx-joins-forces-with-plotly-to-enable-data-visualization-throughout-the)

Plot.ly is a web-based visualisation library company, playing in the same space as Tableau. This collaboration (depending on how long it takes to implement) starts pushing Alteryx firmly into Tableaus space.

I think this is an excellent (if obvious) move for Alteryx. They're not reinventing the wheel, but if the visualisations can be integrated cleanly into an Alteryx workflow, thats pretty much Tableau's functionality sorted. Why would you need both? If Alteryx Designer 2 is actually a thing, and actually web-based, powered by Alteryx Server, that could be a potent combination for all ETL, Analysis and Visualisation requirements.


### Talend
Phew. This section was the last (and most painful) section completed, mainly because I didnt really get what Talend actually do, despite repeated looks at their (stock photo heaven) website and watching their (interminable) videos.

1. Data agilty.
2. Data integration. 
3. Unified platform.
4. Open-source approach.
5. Work natively with cloud and big data technologies.

Honestly, their website is full of bull$#!+ buzzwords (BBs). And you can't speed up their videos, which are also full of BBs. Makes me want wash my eyes.

So, in desperation, I downloaded the manuals. OMG. Everything I've seen about Alteryx is: I could do that. Hook up some stuff here, draw some lines there. Talend manuals put me off completely.

So... youtube. At least you can speed things up. Things don't improve. Check out the Datarobot/Alteryx video I posted below for a pain-free comparison.

I think Talend do similar stuff to what Alteryx does, but they have a bazillion products. My opinion is: it looks hard to use. Alteryx seems much easier to just have a play with and get some real outputs. But, Talend is free for the basic versions, so thats their in. 

Ok, who cares what they do? Their financials:
Talend is an ADR. Which means no SEC filings. Morningstar gives:

Revenue:

Company|Q116|Q216|Q316|Q416|Q117|Q217|Q317|Q417|Q118
-------|----|----|----|----|----|----|----|----|----
Talend |23|25|27|30|33|36|38|42|47
Def. Rev||||71|70|73|79|110|108
Alteryx|18|20|22|25|29|30|34|39|43
Def. Rev||||74|74|77|82|114|112 

So almost identical in terms of revenue. My gut feel...? They're competition, but after different audiences. I'm pretty sure if you give Talend to a data scientist they'll punch you. If you give Talend to a developer who needs to get some kind of ETL job done and has no other tools... sure.

They're also very into corporate speak, which suggests they're really targeting C-level sales. Alteryx are more "Got an analysis problem? Play with our tool, solve it, then we'll talk about bigger things". I definitely prefer the Alteryx approach.

From here on, I'm going to ignore Talend because the corporate speak makes me ill.

### Datarobot
Datarobot is an interesting company. I saw mention of it on one of the boards. As far as I can tell, it automates that model building part of analysis. It will ingest your data, and then spin it through a large variety of models, with automatic feature discovery. 

The theory is that Datarobot will come up with better models more quickly than manual model creation (such that Alteryx provides). It automates the process of model building, and also testing using best practices (cross-validation, holdout) so its relatively simple to produce good models.

Datarobot looks like an adjunct to Alteryx. There is some overlap in functionality, but Datarobots bread and butter is replacing data scientists (the CEO states that Datarobot is better than 99.9% of the worlds data-scientists which is an interesting stance to take).

They have a plugin to Alteryx.

I sat through a cringe-worthy keynote from the CEO to discover all this. But the tech seems cool. I don't see it as an immediate competitor to Alteryx however. Definitely a nice plugin.

This video is worth looking at for a quick overview of use of Alteryx and Datarobot:
https://www.youtube.com/watch?v=0iauoScQC9c


## Glassdoor
Glassdoor reviews for both Alteryx (3.7) and Tableau (3.8) are a bit depressing. If you were judging the company by the negative reviews of the employees. In particular, Alteryx negative reviews seem honest and well-written, with the common refrain being "Great software, talented co-workers, really bad management".

https://www.glassdoor.com/research/studies/does-company-culture-pay-off-analyzing-stock-performance-of-best-places-to-work-companies/

Talend win with a ranking of 4.1 fwiw.


## Numbers
Revenue growth TTM: Q1-2017 versus Q1-2018 = _52%_

Q      | Q1 16| Q2 16| Q3 16|Q4 16|Q1 17|Q2 17|Q3 17|Q4 17|Q1 18
-------|----- |-----|------|------|-----|-----|-----|-----|------
Revenue|$18   |$20  |$22   |$25   |$29  |$30  |$34  |$39  |$43
       |      |9%   |12%   |11%   |14%  |6%   |13%  |13%  |11%
Def. Rev||||$74  |$74  |$77   |$82.  |$114 |$112  
||||||0%|4%|7%|38%|-2%


### Dollar based net revenue retention

These values were something mentioned on Sauls original post. Whats it mean?

Choose a quarter (Q^1). Choose same quarter following year (Q^5). Grab all the customers who started in Q^(1) and get their Q^(1) revenue (R^(1)). Get the revenue for Q^(5) (R^(5)) and work out the percent difference. Do that for another 3 (Q^2 to Q^4) quarters and average them. This gives you the DBNRR for Q^5.

Anything over 100% means that that cohort is spending more in the 2nd year than they were when they started. 

Note, Alteryx state that they include customers who have churned in the period, so DBNRR of >100% is something to be proud of.


### DCF

Using a compounded revenue growth rate of 32% over the next 5 years and an EBIT margin of 30% (a bit over industry average) and a WACC of 9% gives an estimated share value of **$31**.

Over the ten year period, revenue will grow to around $1.1b.

Any decrease in revenue growth or margins (all things equal) will decrease this share price. The WACC is the biggest unknown, although 1% up or down would change the output by less than 10%. Also, the low cost of debt will tend to keep the WACC lower. Note, Alteryx have just raised $178m in convertible debt at 0.5%.

#### DCF examples

--        |5yr Revenue CAGR               | 20%    | 25%    | 30%   | 40%
---------|--------------------------------|--------|--------|-------|-----
Operating margin|Implied 10 year rev      |$564m   |$755m   |$1b    |$1.7b
20% |                                     |  $7.80  |$11.10 |$15.30 |**$27.26**
25% |                                     |  $11.50 |$16.00 |$21.60 |**$37.70**
30% |                                     |  $15.20 |$20.80 |**$27.90** |$48.10

Ballpark in bold. Alteryx is pretty richly valued. _Is it fairly valued? Over-valued, or under-valued?_



#### Comparisons

Company      | Rev (TTM)| Rev Growth% | OpMargin% | NP %
-------------|----------|-------------|-----------|-----
Alteryx      | $146     |     52%     |    -12.6% | -9.9%
Talend       | $162     |     40%     |    -19.6% | -20.9% 
Tableau      | $923     |     8%      |    -20.3% | -9.7%
Datawatch    | $38      |     16%     |    -15.9% | 2.1%



#### Other numbers. 


Metric                 | Value
-----------------------|----------
Revenue Growth(TTM)    | 52%  |
P/E (TTM)              | -   |
PEG                    | -   |
Gross Margin (TTM)     | 84.9% |
EV/FCF                 | 85 (1.789b/21m) |
[Zacks Rank](https://www.zacks.com/stock/research/AYX/stock-style-scores)            | 3 |
Morningstar fair value[^morningstar] | $25.88 [28May18] |


[^morningstar]: This is a quantitative value they don't cover this stock.



### +'s and -'s [Big trends]
1. \+ More data needing analysis.
2. \+ More complex data requiring complex modelling.
4. \- Competition.

Anything else?

### (IMHO) beliefs required to own the stock

1. That the data analysis market is growing more rapidly than the market is crediting _OR_ there is significant pent up demand that Alteryx can target (eg: Manager says "lets add a variable to our Excel analysis!"
2. That Alteryx can defend and expand its market (perhaps due to pent up demand?). The incumbents (particularly Tableau) could leverage their customer base as those customers move away from visuals and more into analysis.
3. That analysis will remain a manual solution for a reasonable period of time. That is, the Datarobots of the world won't eat into Alteryx's customer base (unlikely because Datarobot is not in the ETL market).
4. The market is big enough for all of the competitive players.

And one additional:
1. If you believe that the WACC is less than 9% (debt at 0.5 (1-t) for example) then 
the DCF numbers will push up.

It seems Alteryx is not... underpriced. 5-year growth expectations of around 32% with 30% margins would make them pretty happy I think. The question is, can and will they exceed those numbers? 

## Updates
19 May 2018 - They closed the $200m convertible note offering, at 0.5% convertible at ~$44.33. So debt has increased by $200m, and cash has increased by $178 (after capped call and expenses). Seems pretty cheap to me, and a decent conversion premium, also covered by the capped call transactions to offset dilution.

My take is this doesn't really alter the value of Alteryx much, but gives them some further capital for safety.


## QUESTIONS
* If Alteryx is so great, why hasn't SAP or Oracle or ... purchased them already? They raised $6m from SAP Ventures early on in their journey (Apr 2011) so obviously have a relationship with them.

