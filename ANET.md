# ANET 
GCon = 1 to 5 scale of ‘Gregs conviction’.  
Most buzzwords are in the 'Definitions' section.



## My understanding
Arista produce Gigabit ethernet switches and routers. They're designed for 'cloud-scale' networking, which more or less means 'better than traditional (Cisco?) small datacenter switches and routers'. They also package their EOS cloud-networking operating system (the thing that lets people program the switches/routers instead of changing cables in ports).

### What is a switch? 
A switch creates networks. So you plug in all your devices to the switch, and when one of them (A) wants to communicate with another (B), A sends the data to the switch (through A's port), which forwards to B (via B's port).

### What is a router?
A router connects networks.

A little bit more detail. Each device (some thing that has a network interface) has a MAC address, which is like your social security number, uniquely identifying the device. On an (ether)network, devices communicate via MAC addresses (which look something like: 00:0a:95:9d:68:16).

Device A (IPAddress: 1.1.1.1, MAC: AAA) wants to send to Device B (IPAddress: 1.1.1.2, MAC: BBB) _on the same network_. A doesn't know B's mac address, so it has to ask the network "who has IP address 1.1.1.2?"

The switch tries to help out, by looking up its IP to MAC map (the devices also have these maps). If the IP address is found, it sends the MAC address of B (BBB) back to Device A. Then Device A sends the whole request with the destination MAC address (BBB).

If its not found, the switch sends a request to every other device on the network saying "Who's got IP address 1.1.1.2?", and 1.1.1.2 replies with its MAC address. The switch updates its map, sends the info back to A, who updates its map as well. Then A sends the properly formed message to the switch, and the switch sends it to B and back again.

### The point is...
Local area network traffic works on a MAC address level and use switches. Internet (or connected networks) work on a IP address level and use routers. Switches resolve MAC addresses to devices (computers, printers etc.) and routers resolve IP addresses to networks.

### What's a hub?
A hub is a super-dumb switch, that doesn't care who's connected to what, it just sends the incoming traffic to each device connected to the hub. That means theres a whole bunch of duplication, so all in all, hubs suck. Forget about them.

### Ok, so what does Arista do?
Arista produces cool switches and routers. The basic premise is, in the olden days, switches and routers were relatively simple, even in quite big datacenters. Clients would ask individual servers for a response, and the server produces the response, possibly asking some other device for some information as well.

But most of the traffic was "north-south" (server-client). The routers got the incoming requests from the internet, sent it to the switch, which sent it to the server, who then responded.

In the "cloud age" however, those datacenters are crazy different. Theres a lot more "east-west" traffic between servers inside the datacenter, because those datacenters are supporting much (much) bigger workloads. A cloud datacenter can be considered a mashup of a whole bunch of individual enterprise datacenters, but with the servers being shared between those enterprises and everyone else who wants to use the cloud datacenter.

All of these switches and routers run EOS, their network operating system, which is how people interact (and program) their devices.

#### 'Make'?
Arista don't actually own device manufacturing capabilities themselves. They contract the actual products to other companies, but design the devices (not sure if there's much IP here?), and develop EOS which is installed on each device.

#### Money
Business model... best left to Arista to explain:

"We generate revenue primarily from sales of our switching products which incorporate our EOS software. We generate the majority of our services revenue from post contract support, or PCS, which end customers typically purchase in conjunction with our products. Our end customers span a range of industries and include large Internet companies, service providers, financial services organizations, government agencies, media and entertainment companies and others. As we have grown the functionality of our EOS software, expanded the range of our product portfolio and increased the size of our sales force, our revenue has continued to grow rapidly. We have also been profitable and operating cash flow positive for each year since 2010."

? So no recurring revenue except for 'services'? Why the large increase in deferred revenue? From their Sept-17 10Q, current deferred revenue is 424m, up from 273m in Dec-16. Long-term deferred revenue is up to 141m from 100m. They say, "...related to contract acceptance terms and ongoing growth in PCS contracts"

10K Conference call - "The 2017 year end product deferred revenue balance was essentially flat to 2016 levels."

They break out 'product' versus 'service' revenue.

Question: What is CloudVision?
Question: If companies buy Arista switches and Routers, does that mean theyre more or less likely to buy Arista again? How do we measure that?



"We also continued to experience pressure in product and service pricing due to competitive market conditions."

"Our end customers span a range of industries and include large Internet companies, service providers, financial services organizations, government agencies, media and entertainment companies and others. Our customers include six of the largest cloud services providers based on annual revenue."

## Big issue?
>"We expect large purchases by a limited number of end customers to continue to represent a substantial portion of our revenue."
>Revenue from sales to Microsoft, through our channel partner, World Wide Technology, Inc., accounted for 16% of our revenue for the year ended December 31, 2016.
>

AWS and Google for example uses its own custom hardware. 

So... the target market looks to be next-gen cloud datacenters that are run by companies that don't have the interest/capability to switch to white-label hardware.

But: "Ullal says Arista isn't worried about the white box trend". "We're a software company," she said. "We could run on anybody's white box if customers wanted it. We don't view what Facebook or other companies do as a threat, we see it as an opportunity and as collaboration."
[Investors.com](https://www.investors.com/research/the-new-america/how-arista-networks-cloud-strategy-jelled-with-microsoft-facebook/)

Q: If they're a software company... ? Do they charge per EOS install? Theres no evidence of any deferred revenue.
[EOS as a service...](https://www.arista.com/en/company/news/press-release/21-company/press-release/1080-pr-20150331)




### Moat
Arista's moat seems to be mostly in the software. "Software driven cloud-networking" does seem to emphasise the 'software'. EOS is the single interface to all of Arista's hardware, so if you have an investment in how to use EOS, it probably makes a lot of sense to continue to invest in Arista's hardware.

If however, datacenters are your business, for example, AWS/MSFT etc., then it makes sense to push into custom hardware.




### Stock advisor

### Arista networks products
Switches
Routers

EOS - The Arista network operating system.
CloudVision - Network wide configuration and visibility for Arista EOS instances.

### Competition
[From here](https://www.nasdaq.com/symbol/anet/competitors)
MORE HERE
1. Cisco
	- FY2017 'Infrastructure platforms' revenue: 27,779
2. Juniper
3. F5 Networks - I'm not sure these guys are competitors. Still can't quite work out exactly what they do.


## Numbers
Revenue growth: FY2016->FY2017 = _45.8%_

Q      | Q1 16|Q2 16|Q3 16 |Q4 16 | FY 16 | Q1 17|Q2 17|Q3 17|Q4 17 | FY 2017 |
-------|----- |-----|------|------|-----|-----|-----|----- | ---- | ---- |
Revenue   | 212,475  |  268,741 |   290,261| 357690| 1,129,167 |  335,475 | 405,211  |   437,633| 467,867 |1,646,186
Product   | 242,196  |  235,616 | 254,238 | 259287 | 991,337 | 291,367  | 353,904 | 380,344  | 407195 |1,432,810
Service   |  29,721 |    33,125| 36,023 | 38,961 | 137,830|   44,108 | 51,307 |  57,289   | 148888 |213,376
\-   |   \-   |  -%  |  %  |  -%  |  -%  |  %  |  -%  |  -%



### DCF
Using a compounded revenue growth rate of 25% over the next 5 years and an EBIT margin of 28.8% (as per current year) and a WACC of 9.6% gives an estimated share value of _$232_.

Over the ten year period, revenue will grow to around $8.5b, compared to the current revenues of Cisco $28b [^cisco], and Juniper ($5b). 

[^cisco]: Cisco revenue is quoted for the 'Infrastructure Platforms' segment only

Any decrease in revenue growth or margins (all things equal) will decrease this share price.

#### DCF examples

         |5yr CAGR | 20% | 25% | 30% | 40%
---------|--------------------------------------|-----|-----|-----|-----
Operating margin|Implied 10 year rev      |$6.5b |$8.7b |$11.5b |$19b
20% |                                  |  $134  |$169  | $205 | $317
25% |                                  |  $165 | **$206**  |**$258**  | **$405**
30% |                                 |  $196 |**$247**  | $311 |  $493
 
We can see that the market (assuming all the other knobs in the DCF are equal!) is expecting around 30% growth over the next 5 years, at a 25% op margin (or a 25% growth rate with a 30% op margin).

#### Comparisons
Revenues (2017) for comparison include Amazon ($135b), Microsoft ($85b), Alphabet ($90b), Cisco ($49b), Oracle ($37b).

Company      | Rev (TTM)| Rev Growth% | OpMargin% | NP %
-------------|----------|-----|-----|-----
Cisco      | $      |$118 |$149 |$237 
Juniper    | $    |$179 |$228 |$367
F5 Networks| $    |23% |24% |20%

#### Other numbers
Metric      | Value
------------|----------
Revenue Growth(TTM)    | 46%
P/E (TTM)              | 48
**PEG**                | **1.04**
Gross Margin (TTM)     | 64.5%
Operating Margin (TTM) | 28.6%
Net profit Margin (TTM)| 28.9%
EV/FCF                 |


## Framework analysis
### Porters 5 forces
[Wikipedia](https://en.wikipedia.org/wiki/Porter%27s_five_forces_analysis)

1. Bargining power of suppliers
2. Threat of new entrants - Low. Large purchasers require significant infrastructure, customer support etc. White-label switches/routers are a challenge.
3. Threat of substitutes - None
4. Industry rivalry
5. Bargining power of buyers


### +'s and -'s [Big trends]
1. + More datacenters 
2. + Datacenters becoming more 'cloud'
3. + Datacenters requiring faster internal bandwidth - 10G->100G->...
3. - Datacenter consolidation with cloud operators.
4. - Datacenter using custom hardware and software.

## (IMHO) beliefs required to own the stock
1. The + trends are more powerful than the - trends.
2. The delta between them is underestimated by the market.
3. Arista EOS is very difficult to duplicate.
3. Arista will maintain/increase growth and margins in those + trend markets as described in the DCF section.

## Definitions
OpenFlow
EOS
PCS - Post contract customer support

https://www.wired.com/2015/06/google-reveals-secret-gear-connects-online-empire/


## Discussions...
###1
MF: ANET could be the new NFLX / New Paradigm Investing
Hi folks,

First time posting here. In fact, I've never really frequented the public TMF boards much at all before recently discovering Saul's board, despite being a member for over a decade now. I recently replied to this post:

http://boards.fool.com/Message.aspx?mid=32991023

on ANET because it really struck a chord with me that I haven't felt since I first discovered NFLX back in 2008ish. Rizz asked if I'd re-post that discussion here as well, so, here it is:

Hi Dan,

This was a fantastic post! Possibly the best I've read in years!

I'm brand new to Saul's boards, interestingly having stumbled upon them via volfan's post on either the RB or SA ANET boards. Though a Fool member for more than a decade now, my interest in taking part on the boards had waned. I was very content to let my investments, which have done amazingly well over that time, ride. I was getting bored and starting to dabble in options, but found they leave me unfulfilled as an investor as compared to sinking my teeth into a really, really great company. Recently a friend of mine asked me to help him invest, and after making him join SA, we started having lots of chats via texting and IM, with the occasional phone call thrown in. As a result, my interest in reading the boards has picked up again, and it was my friend who asked me about ANET. And so I started digging in. And found Saul's boards (OMG, what a goldmine of information. 10 years of subscriptions to TMF, and this board is worth every penny and more! :) And here I am reading your post today.

It reminds me of the kind of thing I used to write for the SA NFLX boards many years ago. And having dug into ANET recently, I'm finding exactly the same sort of thing with ANET that I have absolutely loved for years about NFLX. I've never really been able to wrap my head around the numbers. Despite being an engineer, and a math person, for some reason, the numbers don't tell me what I need to know. And that's the intangibles. The people, the story, the struggle. With NFLX, I knew who Reed was, I knew where he came from, I understood the companies he had led, I had used and been trained to manage some of their software. I understood the battle against the Goliath that was Blockbuster at the time, etc. I've been searching for another NFLX for 10 years. I found one with Amazon. I thought I had found one with GMCR, but they sold out. I thought SBUX might be one, but no, not really.

But ANET. This could the next one for me. Jayshree seems like the real deal, Andy goes back to my roots as a UNIX geek having co-founded Sun Microsystems, a company I have a very long history with, and was deeply upset they sold out to ORCL a few years ago. And it's as that UNIX geek that makes me intuitively understand exactly what ANET has accomplished (ironically, something I was thinking about 20 years when Linux first came on the scene!). SDN is something that is desperately needed in today's data centers. It's what rules the networking of cloud computing in AWS. But data centers have no real way of doing this. In order to change your routing rules, or firewall filters, it's almost always done via request to the networking group who then has to figure out exactly what you want, try it out, have you test it, go back, fiddle with it, etc. in an endless loop until they get it right.

With SDN, though, combined with Infrastructure as Code, I get to define not only my entire infrastructure in code, but now my networking as well. Routing tables, firewall filters, etc. All as lines of code in the same place as the application I may be deploying! This is already the way things are in "the cloud". But not so in the data center, where static hardware still requires human intervention to make the majority of changes. It's a slow, tedious, manual way of doing things and building, managing, and updating infrastructure. ANET makes my data centers look more like a cloud environment. And, as much as I love AWS, and as unbelievable as they are, there are and will always be terrestrial based data centers for a variety of ways. But developers won't want to develop for them unless they can deploy to them in a similar manner as they do to the cloud. And that's where the private virtual clouds come in using things like Nutanix, VMWare, or even OpenStack. And with ANET's SDN thrown into the mix, private virtual clouds have it all!

Anyway, that's a very long-winded way of saying Thank You! Thank you for addressing the intangibles of the personalities, the characters, THE fundamentals. I've always invested more based on those than I ever have on numbers, and this is the first company since NFLX and AMZN that to get me this excited to want to post anything to a TMF board in a very long time :)

--
Paul - making ANET a significant portion of his portfolio!


### 2. TMF: Diving Into ANET Numbers / New Paradigm Investing
Before I take a look at some numbers for ANET and what Microsoft means I have to ask...Cleveland Who?

Has anyone here ever used or even heard of Cleveland research? Seriously if anybody knew they existed as of last Thursday I’d be interested in hearing about it. I have to admit I don’t really care what they think. I think the only reason they were talked about so much is that their report coincided with a drop in the share price already in motion. I guess an institutional holder dropped a big chunk of shares leaving everyone looking for a reason. And out come the parrots in the media “Cleveland Research, White Boxes, MSFT going to 10%”

Is there any other statement by Arista claiming Microsoft will decrease to 10% of revenue? Is the only attributable remark from the Q4 call? I think the minds at NPI have shown that Ullal did not mean 10% as her official forecast. 

In Q1 2017 Earnings Call, Ullal said this in regards to Microsoft. “As I’ve always commented, it would be difficult to expect them to be the same customer concentration as they were last year(2016), which was I think 16%. But a good guess is they will be in the 10% to 16% range this year.” Where was Cleveland last year saying the sky is falling MSFT will only be 10% of ANET sales for 2017!!

And so what if Microsoft does become a smaller chunk of overall revenue. As Arista grows at a rapid rate it makes since that 1 customer cannot grow their purchases from Arista at a matching rate in perpetuity. This will dilute that concentration level at some point, it has to. 

On to some numbers and I will use top of ANET guidance as I see no reason to doubt they will not exceed guidance as they have a habit of doing. 

Quarter - Rev/YoY Growth/MSFT $

Q1 2016 Rev-$242.2M/35%/$39M

Q1 2017 Rev-$335.5M/38.5%/$54M

Q1 2018 Est-$468M/39.5%/$75M

Revenue of $468 is top of guidance and is the same as Q4 2017 revenue. If Arista sells to MSFT in Q1 100% of what they sold them in Q4 then they will sell them $75M. I know ANET has some recurring revenue but it’s difficult to tell how much of the MSFT revenue is recurring, but it’s safe to say that most of the $75M is new equipment. Will Microsoft need $75M in switches and software support each and every single quarter forever? Will they need $100M in Q4 2018? I don’t know but Arista has lots of opportunities.

If MSFT is 10% of Q1 2018 that is $47M. If MSFT does 100% of business in Q1 2018 as they did in Q1 2017 they will be 11.5% of Arista revenue. 

I think we need to look at the bigger picture. ANET is forecasting 39.5% revenue growth for Q1. That is great growth. In fact it’s accelerating from Q1 2017 growth of 38.5%. And how did 2017 turnout for Arista? A $10M beat yields 42.5% growth. 

Yes this exercise has helped me narrow down the choices. Haven’t added to ANET in awhile. 

Darth