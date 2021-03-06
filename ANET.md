# ANET 

## My understanding
Arista produce Gigabit ethernet switches and routers They're designed for 'cloud-scale' networking, which more or less means 'better than traditional (Cisco?) small datacenter switches and routers'. They also package their EOS cloud-networking operating system (the thing that lets people program the switches/routers instead of changing cables in ports).

### What is a switch? 
A switch creates networks.

So you plug in all your devices to the switch, and when one of them (A) wants to communicate with another (B), A sends the data to the switch (through A's port), which forwards to B (via B's port).

A little bit more detail. Each device (some thing that has a network interface) has a MAC address, which is like your social security number, uniquely identifying the device. On an (ether)network, devices communicate via MAC addresses (which look something like: 00:0a:95:9d:68:16).

Device A (IPAddress: 1.1.1.1, MAC: AAA) wants to send to Device B (IPAddress: 1.1.1.2, MAC: BBB) _on the same network_. A doesn't know B's mac address, so it has to ask the network "who has IP address 1.1.1.2?"

The switch tries to help out, by looking up its IP to MAC map (the devices also have these maps). If the IP address is found, it sends the MAC address of B (BBB) back to Device A. Then Device A sends the whole request with the destination MAC address (BBB).

If its not found, the switch sends a request to every other device on the network saying "Who's got IP address 1.1.1.2?", and 1.1.1.2 replies with its MAC address. The switch updates its map, sends the info back to A, who updates its map as well. Then A sends the properly formed message to the switch, and the switch sends it to B and back again.

### What is a router?
A router connects LAN networks, so if you want to go outside your LAN into another LAN (ie, a WAN, for example to the internet), routers are the things that make your request/data get to that far distant LAN. Then the switches get you to the actual computer/device you want to talk to.

Local area network traffic works on a MAC address level and use switches. Internet (or connected networks) work on a IP address level and use routers. Switches resolve MAC addresses to devices (computers, printers etc.) and routers resolve IP addresses to networks (and then pass responsibility to the switches).

### What's a hub?
A hub is a super-dumb switch, that doesn't care who's connected to what, it just sends the incoming traffic to each device connected to the hub. That means theres a whole bunch of duplication, so all in all, hubs suck. Forget about them.

### Ok, so what does Arista do?
Arista produces cool switches and routers. The basic premise is, in the olden days, switches and routers were relatively simple, even in quite big datacenters. Clients would ask individual servers for a response, and the server produces the response, possibly asking some other device for some information as well.

But most of the traffic was "north-south" (server-client). The routers got the incoming requests from the internet, sent it to the switch, which sent it to the server, who then responded.

In the "cloud age" however, those datacenters are very different. Theres a lot more "east-west" traffic between servers inside the datacenter, because those datacenters are supporting much (much) bigger workloads. A cloud datacenter can be considered a mashup of a whole bunch of individual enterprise datacenters, but with the servers being shared between those enterprises and everyone else who wants to use the cloud datacenter.

All of the Arista switches and routers run EOS, their network operating system, which is how people interact (and program) their devices.

As far as I can tell, Arista went "Cisco sucks. Their switches are expensive, and their software is old and monolithic. Lets make the best switch and the best software, and go after them in the datacenter switch market".


#### What is EOS?

EOS is the network device operating system, in my view their main IP. Each device runs this operating system, and its responsible for the programmability of the device. If you want to change the device, you log in to it using EOS. It's the equivalent of Ciscos IOS.

Unlike IOS, EOS is all the things modern process-specific software should be, modular, extensible etc. You can install 3rd party processes on the switch that can talk to EOS, at the same level as an EOS process.

Cisco is now playing catchup with their IOS XE, IOS XR, and NX OS operating systems.

The very fact that they have these multiple OS's is big plus for Arista. Supporting multiple operating systems would be an expensive pain in the ass for them.




#### What is CloudVision?

CloudVision is software developed by Arista that communicates with the individual EOS instances (on each router for example) that allows the user to view the entire network. This abstraction creates a one-stop-shop for network-wide functionality, for example analytics, security, provisioning etc.



#### 'Make'?
Arista don't make the routers and switches. They contract the actual products to other companies, but design the devices (not sure if there's much IP here?), and develop EOS which is installed on each device.

#### Money
Business model.. best left to Arista to explain:

"We generate revenue primarily from sales of our switching products which incorporate our EOS software. We generate the majority of our services revenue from post contract support, or PCS, which end customers typically purchase in conjunction with our products. Our end customers span a range of industries and include large Internet companies, service providers, financial services organizations, government agencies, media and entertainment companies and others. As we have grown the functionality of our EOS software, expanded the range of our product portfolio and increased the size of our sales force, our revenue has continued to grow rapidly. We have also been profitable and operating cash flow positive for each year since 2010."

"Our end customers span a range of industries and include large Internet companies, service providers, financial services organizations, government agencies, media and entertainment companies and others. Our customers include six of the largest cloud services providers based on annual revenue."

---

##### Deferred revenue
> Greg: So no recurring revenue except for 'services'? Why the large increase in deferred revenue? 

From their Sept-17 10Q, current deferred revenue is 424m, up from 273m in Dec-16. Long-term deferred revenue is up to 141m from 100m They say, "...related to contract acceptance terms and ongoing growth in PCS contracts".

10K Conference call - "The 2017 year end product deferred revenue balance was essentially flat to 2016 levels."

---

### Moat
Arista's moat seems to be mostly in software. "Software driven cloud-networking" does seem to emphasise the 'software'! EOS is the single interface to all of Arista's hardware, so if you have an investment in how to use EOS, it probably makes a lot of sense to continue to invest in Arista's hardware.

The strength of this moat is a bit unclear, and a lot (almost all) of the investment thesis relies on the strength of EOS. 

Here's a comment from Tinker on Sauls Investing Board which is relevant here:

>Here is Arista's take on EOS. EOS enables Arista to produce router functionality in the switch for a per port cost, from a slide put out last year by Arista at 33x less per port than Cisco charges for its router for the same (or even less functionality). Arista actually has a larger routing table than what Cisco or Juniper offer. That is 1/33 ($3,000 vs. $100,000).

>What this all means in practicality, so far, is Arista has moved up to 15% marketshare, more or less from zero just 5 or so years ago against a monopoly and Cisco marketshare has gone down by nearly the same. Arista's marketshare in 100GB is more than 25%. Thus the puzzlement of 25% growth rate for the rest of the year...

> we can only judge the narrative from the results. And forward prognostication seems to be less aggressive than the narrative would indicate (I believe the market thinks Arista was unduly conservative in regard - and could produce another huge drop if this is not the case, like we had last quarter - although some of that has been recovered), but backward results have systematically shown the advantage.


The historic trend certainly indicates some significant advantage for Arista versus Cisco.

### Litigation
Have ignored it here Arista seem pretty confident it will go away, most of Ciscos claims seem to have been rejected. Not sure about the [OptumSoft](https://www.networkworld.com/article/3016667/lan-wan/court-finds-for-arista-in-eos-suit-with-co-founder.html) one which still seems to be ongoing Helps to be a billionaire I guess.

For Cisco litigation, see [https://s21.q4cdn.com/861911615/files/doc_downloads/legal_proceedings/Arista-Legal-Update-2018.04.09.pdf]


### Stock advisor
https://www.fool.com/premium/stock-advisor/coverage/18/coverage/updates/2018/04/06/best-buy-now-arista-networks.aspx

### Major Competition
[nasdaq.com](https://www.nasdaq.com/symbol/anet/competitors)

1. Cisco 	- FY2017 'Infrastructure platforms' revenue: 27,779m
2. Juniper - FY2017 Revenue: 5027m


## Numbers
### Basic data (TMF1000)

* Revenue was 472.49m up (1.0%) from 467.87m from the previous quarter (335.48m same quarter last year)
* TTM Revenue was 1.783b up (45.9%) from 1.222b 
* TTM Revenue per share (diluted) was 22.34 up (36.4%) from 16.38
* EPS diluted (prev quarter): was 1.79 up (38.8%) from 1.29
* Earnings (same quarter prev year): was 1.79 up (67.3%) from 1.07
* TTM eps was 6.06 up (96.8%) from 3.08
* Diluted share count was 80.72m up (4.1%) from 77.52m
* Cash and short-term investments  was 1.738b up (13.2%) from 1.536b (prev quarter)
* Debt (prev quarter) was 37.14m down (1.4%) from 37.67m (prev quarter)
* Cash flow for quarter was 189.21m down (48.8%) from 369.75m
* Cash flow for TTM was 647.34m up (166.8%) from 242.60m
* Cash flow per share for TTM was $8.02
* Gross margins was 0.64 down (2.4%) from 0.66
* CapExp was 6.34m up (103.1%) from 3.12m

### Last reported quarter ranges min, max [last]

* Trading range between Oct 01, 2017 - Dec 31, 2017 was 181.17 to 307.96 [255.3]
* Market cap between Oct 01, 2017 - Dec 31, 2017 was 13.244b to 22.751b [18.860b]
* PE range (Oct 01, 2017 - Dec 31, 2017) was 27.33 to 46.45 [38.51]
* PS ratio range (Oct 01, 2017 - Dec 31, 2017) was 8.20 to 13.94 [11.56]
* Free cash flow (TTM) yield range (Oct 01, 2017 - Dec 31, 2017) was 2.85 to 4.89 [3.43]
* EV/Sales between Oct 01, 2017 - Dec 31, 2017 was 6.97 to 12.28 [10.10]

### Most recent quarter ranges min, max [last]
(uses more recent price data with last reported results)

* Trading range between Apr 01, 2018 - Jun 30, 2018 was 239.44 to 286.62 [257.49]
* Market cap between Apr 01, 2018 - Jun 30, 2018 was 19.328b to 23.136b [19.022b]
* PE range (Apr 01, 2018 - Jun 30, 2018) was 36.11 to 43.23 [38.84]
* PS ratio range (Apr 01, 2018 - Jun 30, 2018) was 10.84 to 12.97 [11.66]
* Free cash flow (TTM) yield range (Apr 01, 2018 - Jun 30, 2018) was 2.80 to 3.35 [3.40]
* EV/Sales between Apr 01, 2018 - Jun 30, 2018 was 9.89 to 12.02 [10.70]

### Revenue

| Quarter   | Revenue   | TTM     | 𝝳 (q-1)   | 𝝳 (YoY)   |
|:----------|:----------|:--------|:----------|:----------|
| 2013Q1    | 61.35m    |         |           |           |
| 2013Q2    | 83.48m    |         | 36%       |           |
| 2013Q3    | 101.62m   |         | 22%       |           |
| 2013Q4    | 114.77m   | 361.22m | 13%       |           |
| 2014Q1    | 117.21m   | 417.08m | 2%        | 91%       |
| 2014Q2    | 137.95m   | 471.55m | 18%       | 65%       |
| 2014Q3    | 155.46m   | 525.38m | 13%       | 53%       |
| 2014Q4    | 173.49m   | 584.11m | 12%       | 51%       |
| 2015Q1    | 179.04m   | 645.94m | 3%        | 53%       |
| 2015Q2    | 195.55m   | 703.55m | 9%        | 42%       |
| 2015Q3    | 217.55m   | 765.63m | 11%       | 40%       |
| 2015Q4    | 245.45m   | 837.59m | 13%       | 41%       |
| 2016Q1    | 242.20m   | 900.74m | -1%       | 35%       |
| 2016Q2    | 268.74m   | 973.93m | 11%       | 37%       |
| 2016Q3    | 290.26m   | 1.047b  | 8%        | 33%       |
| 2016Q4    | 327.97m   | 1.129b  | 13%       | 34%       |
| 2017Q1    | 335.48m   | 1.222b  | 2%        | 39%       |
| 2017Q2    | 405.21m   | 1.359b  | 21%       | 51%       |
| 2017Q3    | 437.63m   | 1.506b  | 8%        | 51%       |
| 2017Q4    | 467.87m   | 1.646b  | 7%        | 43%       |
| 2018Q1    | 472.49m   | 1.783b  | 1%        | 41%       |

### Deferred revenue

| Quarter   | Def.Revenue   | 𝝳 (q-1)   | 𝝳 (YoY)   | Billings(Rev + 𝝳 def. rev)   |
|:----------|:--------------|:----------|:----------|:-----------------------------|
| 2013Q1    |               |           |           |                              |
| 2013Q2    |               |           |           |                              |
| 2013Q3    |               |           |           |                              |
| 2013Q4    | 58.90m        |           |           |                              |
| 2014Q1    | 36.29m        | -38%      |           | 94.59m                       |
| 2014Q2    | 37.89m        | 4%        |           | 139.54m                      |
| 2014Q3    | 40.28m        | 6%        |           | 157.85m                      |
| 2014Q4    | 106.47m       | 164%      | 81%       | 239.68m                      |
| 2015Q1    | 132.82m       | 25%       | 266%      | 205.40m                      |
| 2015Q2    | 164.44m       | 24%       | 334%      | 227.17m                      |
| 2015Q3    | 190.71m       | 16%       | 373%      | 243.81m                      |
| 2015Q4    | 196.81m       | 3%        | 85%       | 251.55m                      |
| 2016Q1    | 219.22m       | 11%       | 65%       | 264.61m                      |
| 2016Q2    | 230.32m       | 5%        | 40%       | 279.85m                      |
| 2016Q3    | 284.83m       | 24%       | 49%       | 344.77m                      |
| 2016Q4    | 372.94m       | 31%       | 89%       | 416.07m                      |
| 2017Q1    | 497.17m       | 33%       | 127%      | 459.71m                      |
| 2017Q2    | 554.51m       | 12%       | 141%      | 462.55m                      |
| 2017Q3    | 565.14m       | 2%        | 98%       | 448.27m                      |
| 2017Q4    | 515.26m       | -9%       | 38%       | 417.98m                      |
| 2018Q1    | 456.05m       | -11%      | -8%       | 413.28m                      |

### Margins

|    | Quarter   | Gross margin   | ebitdamargin   | netmargin   |
|---:|:----------|:---------------|:---------------|:------------|
|  0 | 2016Q2    | 64%            | 22%            | 14%         |
|  1 | 2016Q3    | 64%            | 24%            | 18%         |
|  2 | 2016Q4    | 64%            | 25%            | 18%         |
|  3 | 2017Q1    | 64%            | 24%            | 25%         |
|  4 | 2017Q2    | 64%            | 30%            | 25%         |
|  5 | 2017Q3    | 64%            | 34%            | 30%         |
|  6 | 2017Q4    | 66%            | 32%            | 22%         |
|  7 | 2018Q1    | 64%            | 32%            | 31%         |

### Free cash flow

| Quarter   | FCF     |
|:----------|:--------|
| 2016Q2    | 60.76m  |
| 2016Q3    | -37.01m |
| 2016Q4    | 60.63m  |
| 2017Q1    | 158.22m |
| 2017Q2    | 74.34m  |
| 2017Q3    | 203.24m |
| 2017Q4    | 180.54m |
| 2018Q1    | 189.21m |

### Capital structure

|        | cash    | Investments   | Cash and investments   | Working Capital   | Debt   |   Debt to Equity | Interest   |
|:-------|:--------|:--------------|:-----------------------|:------------------|:-------|-----------------:|:-----------|
| 2016Q2 | 531.06m | 331.90m       | 862.95m                | 878.62m           | 40.44m |             0.04 | 732k       |
| 2016Q3 | 500.48m | 335.80m       | 836.28m                | 969.10m           | 40.04m |             0.04 | 735k       |
| 2016Q4 | 567.92m | 336.05m       | 903.97m                | 1.067b            | 39.59m |             0.04 | 918k       |
| 2017Q1 | 746.57m | 332.81m       | 1.079b                 | 1.204b            | 39.14m |             0.03 | 715k       |
| 2017Q2 | 823.48m | 337.50m       | 1.161b                 | 1.338b            | 38.67m |             0.03 | 623k       |
| 2017Q3 | 854.48m | 524.77m       | 1.379b                 | 1.508b            | 38.20m |             0.03 | 701k       |
| 2017Q4 | 859.19m | 712.50m       | 1.572b                 | 1.737b            | 37.67m |             0.02 | 741k       |
| 2018Q1 | 886.16m | 888.02m       | 1.774b                 | 1.921b            | 37.14m |             0.02 | 687k       |

### Expenses

| Quarter   | R and D   | rnd     | Change (q-1)   | Change (YoY)   | Sales, General, Admin   | Change (q-1)   | Change (YoY)   |
|:----------|:----------|:--------|:---------------|:---------------|:------------------------|:---------------|:---------------|
| 2016Q2    | 69.02m    |         |                |                | 49.27m                  |                |                |
| 2016Q3    | 70.65m    |         | 2%             |                | 52.75m                  | 7%             |                |
| 2016Q4    | 71.40m    |         | 1%             |                | 61.26m                  | 16%            |                |
| 2017Q1    | 81.61m    | 292.68m | 14%            |                | 59.18m                  | -3%            |                |
| 2017Q2    | 81.19m    | 304.85m | -1%            | 18%            | 61.95m                  | 5%             | 26%            |
| 2017Q3    | 79.61m    | 313.81m | -2%            | 13%            | 60.17m                  | -3%            | 14%            |
| 2017Q4    | 107.18m   | 349.59m | 35%            | 50%            | 60.60m                  | 1%             | -1%            |
| 2018Q1    | 102.36m   | 370.35m | -4%            | 25%            | 61.82m                  | 2%             | 4%             |



### DCF
Using a compounded revenue growth rate of 25% over the next 5 years, an EBIT margin of 28.8% (as per current year) and a WACC of 9.6% gives an estimated share value of _$232_.

Over the ten year period, revenue will grow to around $8.5b, compared to the current revenues of Cisco $28b [^cisco], and Juniper ($5b) 

[^cisco]: Cisco revenue is quoted for the 'Infrastructure Platforms' segment only

Any decrease in revenue growth or margins (all things equal) will decrease this share price.

#### DCF examples

--        |5yr CAGR                        | 20% | 25% | 30% | 40%
---------|--------------------------------|-----|-----|-----|-----
Operating margin|Implied 10 year rev      |$6.5b |$8.7b |$11.5b |$19b
20% |                                     |  $134  |$169  | $205 | $317
25% |                                     |  $165 | **$206**  |**$258**  | **$405**
30% |                                     |  $196 |**$247**  | $311 |  $493
 
We can see that the market (assuming all the other knobs in the DCF are equal!) is expecting around 30% growth over the next 5 years, at a 25% op margin (or a 25% growth rate with a 30% op margin).

Note: Morningstar predict 25% growth (ie, Arista's prediction) in 2018, and 15% over the next 5 years (and hence get a lower stock price).

#### Comparisons
Revenues (2017) for comparison 

Company      | Rev (TTM)| Rev Growth% | OpMargin% | NP %
-------------|----------|-------------|-----------|-----
Arista       | $  1646  | 45.8%       |28.6%      |28.9%
Cisco        | $  48096 | -1%         |25%        |20.1%
Juniper      | $  5027  | 0.7%        |16.9%      |11.8%
F5 Networks  | $  2097  | -1%         |25%        |20.1%

#### Other numbers

Metric.     | Value |
------------ | ---------- |
Revenue Growth(TTM)    | 46%  |
P/E (TTM)              | 48   |
**PEG**                | **1.04** |
Gross Margin (TTM)     | 64.5% |
EV/FCF                 | 27 (17.36b/632m) |
[Zacks Rank](https://www.zacks.com/stock/research/ANET/stock-style-scores)            | 4 |
Morningstar fair value[^morningstar] | $207 [24Apr18] |


[^morningstar]: They have however raised their fair value from $57 in June 2015 to $207 now. Lucky you didn't listen to them!

### From [JPMorgan Global Tech Media Comms Conference](https://jpmorgan.metameetings.net/events/tmc18/sessions/14923-arista-networks/webcast)
17min

25% revenue growth comments.

> "Set a reasonably high confidence scenario for the year.."
> 
> "Didn't necessarily believe could sustain mid-40s growth rate..."
> 
> ... not a good way to set up a goal for 2018
> 
> Service providers: Difficult to predict
> 
>"A balanced view of different outcomes."

> Haven seen nothing different from competitive landscape.


White boxes - landcape hasn't changed that much.

#### On campus entry
Places in the network -> Places in the cloud. So having EOS across all places in the cloud.
$3-4b market out of $14b.

Aruba - wireless at the edge, VMware - IoT management.
Revenue not until 2019.

[27min] Value proposition: EOS, state driven architecture, every box exporting state into central net-database, held in CloudVision (or own database). End-to-end management, ML+AI, easy.

Single image -> only have to qualify one image. 

Campus hasn't enjoyed software-driven cloud networking versus datacenter. Op costs down.



## Thoughts
### Porters 5 forces
*Note, these comments are just my opinion, and Porters was my first go-to. Suggestions for other analyses welcome!*

[Wikipedia](https://en.wikipedia.org/wiki/Porter%27s_five_forces_analysis)

1. Bargining power of suppliers - **Low?** Not sure about this, but assume because of the emphasis on commodity components that their hardware could be sourced from a number of suppliers. In their 10K, they do state: "Our products rely on key components, including merchant silicon, integrated circuit components and power supplies purchased from a limited number of suppliers, including certain sole source providers"
2. Threat of new entrants - **Low**. Large purchasers require significant infrastructure, customer support, sales teams etc. White-label switches/routers may be a challenge but its the software that will make the difference (can/would AWS enter this market?)
3. Threat of substitutes - **None**. I don't think switches and routers can be substituted.
4. Industry rivalry - **Significant**. Cisco is the leading name in the industry, and 'no one ever got fired for buying Cisco'. Their CiscoDNA project looks like a direct competitor to CloudVision 
5. Bargining power of buyers - **Significant**. Arista have commented previously on how Cloud Titans receive lower cost deals. From 10K, "Our large end customers have significant purchasing power and, as a result, may receive more favorable terms and conditions than we typically provide to other end customers, including lower prices, bundled upgrades, extended warranties, acceptance terms, indemnification terms and extended return policies and other contractual rights", And, "We also continued to experience pressure in product and service pricing due to competitive market conditions."

Overall, the Porters 5 forces _don't paint an awesome picture for Arista_. I think it comes down to the 'Industry Rivalry' section. How big/bad of a competitor is Cisco? They're huge, with large cash reserves, so how big is Aristas moat?

### White boxes and big customers

It seems the concentration of end customers may be an issue, especially in the Cloud Titan space. Selling big to few customers can lead to discounting, and significant loss-of-revenue if those customers choose another option.

>"We expect large purchases by a limited number of end customers to continue to represent a substantial portion of our revenue."
>Revenue from sales to Microsoft, through our channel partner, World Wide Technology, Inc., accounted for 16% of our revenue for the year ended December 31, 2016.

AWS and Google for example uses its own custom hardware 
>Greg: Although they do say "Our customers include six of the largest cloud services providers based on annual revenue"?

So the target market looks to be next-gen cloud datacenters that are run by companies that don't have the interest/capability to switch to white-label hardware.

However, "Ullal says Arista isn't worried about the white box trend, we're a software company," she said. "We could run on anybody's white box if customers wanted it. We don't view what Facebook or other companies do as a threat, we see it as an opportunity and as collaboration."
[Investors.com](https://www.investors.com/research/the-new-america/how-arista-networks-cloud-strategy-jelled-with-microsoft-facebook/)

[White box discussion (by Forrester)](https://www.cisco.com/web/offers/pdfs/the_myth_of_white_box.pdf)
Basically the summary is, the costs are really in the software. So, Arista is a software company, and will live and die based on the quality of the software.

>Q: If they're a software company.. ? Do they charge per EOS install?
[EOS as a service...](https://www.arista.com/en/company/news/press-release/21-company/press-release/1080-pr-20150331)


### +'s and -'s [Big trends]
1. \+ More datacenters 
2. \+ Datacenters becoming more 'cloud'
3. \+ Datacenters need more bandwidth - 10G->100G->...
4. \- Datacenter consolidation with cloud operators.
5. \- Datacenter using custom hardware and software.

Anything else?

### (IMHO) beliefs required to own the stock
1. The + trends are more powerful than the - trends. [GConf:4]
2. The delta between the trends is underestimated by the market. [GConf:5]
3. Arista EOS is very difficult to duplicate. [GConf:4 [^tinker] - it needs to be difficult to duplicate AND not subject to alternatives AND have the advantages easy to communicate]
4. Competitors (Cisco!) cannot successfully compete in these markets because of Aristas competitive advantages [GConf: 4 ]
5. There are no new disruptive technologies that will undermine Arista's position in the short term. [GConf: ???]
6. Arista will maintain/increase growth and maintain margins in those + trend markets as described in the DCF section. [GConf:4]
7. You believe management can deal with the rapidly changing market. [GConf:4]

[^tinker]: As per Tinkers comment on Sauls Investing Board, the historic results indicate that replicating EOS is difficult. Cisco is playing catchup with their new OS's, but still has a mountain of legacy installs to support.
**GConf: 4.1 / 5**


## Updates
14 May 2018 - "Cognitive cloud networking for the campus". May 7, Arista press release describes a solution for campus networking, a new market for them. Partnering with Aruba (HP) and VMware (not exactly sure how) to deliver "IoT-ready" networks for campuses.

From SA, Cisco has the Cisco 9000 series which is in this market already, and reportedly doing really well. 
>"This is the fastest-ramping new product introduction we've had in our history and a fantastic example of the innovation we've delivered over the last two years," Robbins said in a conference call with Wall Street analysts recently to discuss Cisco's second-quarter results." [https://www.crn.com/news/networking/300099561/cisco-more-than-doubles-its-catalyst-9000-customer-base.htm]




## Definitions
* DirectFlow - Is (I think) sort of a proprietary OpenFlow. "DirectFlow and OpenFlow are mutually exclusive and you can run only one of the two at any given time" It looks (to me) like DirectFlow is OpenFlow for Arista devices (see OpenFlow).
* EOS - EOS is the Arista network operating system. This is the software installed on every device that allows the SDN magic to happen.
* Flow (table) - As opposed to forwarding. Flow tables are like super forwarding tables, which define rules for incoming network packets. The rules and behaviours in flow tables are much more flexible than forwarding tables. For example, any sort of information in the incoming packet can be used to id the packet, and any sort of behaviour, not just correct forwarding You can implement a firewall with flow rules.
* LAN - Local Area Network. What happens any time two devices are plugged into a switch. They can talk to each other but not to other devices not connected to the switch.
* Hybrid WAN - A Wide Area Network for an enterprise that consists of private/dedicated infrastructure and public infrastructure (internet). Essentially, for the most important traffic, the enterprise would have dedicated infrastructure, while less important traffic would be sent over public internet connections.
* MPLS - Multiprotocol Label Switching. Another network protocol that makes life simpler/quicker for MPLS-enabled routers. Used to implement enterprise WANs. The first MPLS configured router applies a “label” on the data, other routers use the label to route the traffic without needing to perform any additional IP lookups. You can specify routes and behaviours based on type of traffic (html, video etc). Essentially, MPLS is used for high-availability network traffic within a distributed enterprise. It's a higher quality connection than what can be guaranteed with internet-based connections.
* OpenFlow - A standard protocol that exposes the flow capabilities of routers/switches that implement OpenFlow. That is, multiple vendors could use the OpenFlow protocol to interface with the devices EOS implements OpenFlow.
* PCS - Post contract customer support
* SDN - Software Defined Networking. The ability to define networks through software, rather than the physical routing of cables. This terminology tends to be used for networks internal to a datacenter (LAN).
* SD-WAN - Software defined Wide Area Networks. ie, SDN but applied to inter-datacenter networks I think CloudVision plays in this space. Instead of using your company WAN using your MPLS-type protocols, SD-WAN lets you use normal internet where appropriate [Greg: I'm not super-clear on this]
* WAN - A wide area network, as opposed to a LAN. Connecting geographically distributed LANs, for example, an enterprise with multiple branch offices.


## Conference calls

### Q1 2018
"Given some tough 2017 comparables, we believe that the current consensus for the balance of the year, which calls for **year-over-year growth in the mid-20% range, remains relevant.**"

Guidance (non-GAAP), revenue: $500m-$514m;gross margin of approximately 62% to 64%; operating margin of approximately 32% to 34%.

Q: 945 certification deferred revenue done and dusted?  
A: Pretty much. Small bit left.

Q: AI?  
A: Very early, experimental. Partners with Nvidia and Pure.

Q: Privacy/Trade wars, any change in customers spend behaviour?  
A: ... um... not really. Some smaller more localised builds by cloud companies.

Q: You said "Mid-20% growth" but you grew 40% in Q1. So second half decelaration? And ASC 606, $19m deferred revenue impact. Did that impact revenue in the quarter?  
A: "the mid-20s is a reasonable way to think about the growth rate" for remainder of year. ASC 606 just impacted balance sheet.

Q: Cloud spenders reporting big beats in CapEx, so cap exp is growing in 2018. But you're guiding lower for rest of 2018. Whats the gap?  
A: Networking small part of their CapExp, and big spend a multi-year exercise, so hard to tell when the networking bit will hit.

Q: Change in mix of top-of-rack switches and (versus?) spine within web-scale customers?  
A: Not much different.

Q: Verticals under versus over performing?  
A: No.

Q: How about enterprise?
A: Clearly our number 2 vertical. We continue to do very very well. 

Q: Where are we at in 100g cycle?  
A: Not even in the first inning.

Q: Gross margin.
A: yeah, 62-65% for year.

Q: would you be able to share insight into opportunities, outlook and the current state of enterprise penetration for both routing and switching?
A: Switching better than routing. Would like to see us do better, but doing very well.

Q: Dumb question on cloud vertical margin
A: Cloud = lower margin

Q: Progress expanding customer base? International?
A: The M&E vertical is a particularly strong one for us..."Enterprises are risk averse and _only in the last year_, I would say, they have started to take Arista seriously"
>GD: Whats M&E?

Q: Number of routing customers? And discuss backlog?
A: re: Backlog-> No. Year end FlexRoute > 200. Only going to give yearly numbers (but think we're going to double).

Q: Mid-20s growth rate for whole year, or remainder?
A: Remainder.

Q: International expansion 80-120. Whats driving international?
>GD: How was this calculated? 67% in US...and therefore?

A: Made lots of international investments 2015-2016. Starting to pay off. Mirrors top 5 verticals. Only Tier-2 service providers not so represented (more a US thing).

Q: Any change in pricing environment? 
A: No.

Q: Incremental pressure from Cisco et al, or white boxes? 
A: Normal aggression.

Q: You're not seeing any incremental uptick of white box solutions by your customers?
A: I am not seeing any difference in competitive behavior due to white box. And white box adoption, or rather disaggregated EOS, I'm not seeing any shift or change.

Q: Winning replacement (ie, of competitors) router deals? Or new footprints?
A: ...actual market has been shrinking... The new change is in the white area side, where more and more of the interfaces are moving to ethernet from traditional SONiC or T1 or ATM type of interfaces. In terms of new footprint versus existing, for us, it's all new. 
>GD: Not sure I really understand this

Q: Campus?
A: Arista does not plan to participate in the traditional campus. As things evolve in the campus and they become more and more akin or aligned with Arista's different value-add and differentiated capabilities, we're open to that. 
> GD: Whats traditional campus given they announced entry into the campuse the next quarter]






<!--stackedit_data:
eyJoaXN0b3J5IjpbNjcyNjA4MDg4XX0=
-->