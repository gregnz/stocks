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
Revenue growth: FY2016->FY2017 = _45.8%_

Q         | Q1 16|Q2 16|Q3 16 |Q4 16 | FY 16 | Q1 17|Q2 17|Q3 17|Q4 17 | FY 2017 |
----------|----- |-----|------|------|------|-----|-----|----- | ---- | ---- |
Revenue   | 242m |269m |290m |328m |1.13b |335m   |405m   |438m|468m|1.65b
 Growth   |     |11% |8%    |13%  |      |2% | 21% |8% |7% | 46%
Product   | 212m |236m |254m  |289m  | 991m | 291m | 354m | 380m| 407m|1,433b
Growth    |      |11% |8%   |14%   |      |1%  |21%  |7%   |7%   |45%
Service   |  30m |33m |36m   |39m   | 138m |44m  | 51m  |57m |61m |213m
Growth    |      |11% |9%   |8%   |     |13% |16%  |12% |6%  |55%



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







<!--stackedit_data:
eyJoaXN0b3J5IjpbODUyMDU3OF19
-->