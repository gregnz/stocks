# NTNX 

## My understanding
Nutanix is a leader in 'Hyper-converged infrastructure'. Uh... cool. Whats that again?

Let's say you've decided to set up a datacenter to power your jellybean company. You've got a windows app you want to run that lets you sell jellybeans. You tell your CTO and they run out and buy some servers, hard-drives and a (Arista!) switch to plug everything together. They set everything up, install Windows, and the devops team slap your application on top, and you're done. Easy.

And then what happens? Someone wants to run a reporting application. Except it runs on Linux, not Windows. You don't really want to buy a whole new server, just to run a little linux app. Your CTO starts talking about virtualisation and the benefits of virtual machines.

### What's a virtual machine?

Virtualisation splits your physical server into abstract servers. Normally, your operating system interacts with the hardware (memory, cpu, harddrive etc) of your server. However, install some special software called a _Hypervisor_, and the OS talks to the hypervisor, and the hypervisor then talks to the actual hardware.

What does that do? It lets you install multiple abstract servers (virtual machines) on your single server. The hypervisor is in charge of divvying up the server resources (memory, compute, storage etc) to each virtual machine. Each virtual machine has no idea it's running on a single server, its all hidden by the hypervisor.

So you could pretend you had 2 servers (for example, a windows server and a linux server) all the while running them on one physical server in your datacenter. Or 3. Or as many servers as you had capacity for on your physical hardware.

It's very cool, and virtual machines are the basis for every^1 data-center architecture.

Except... what happens when you need more compute power? Or more hard drive space? You've still got the problem of actually managing and provisioning all the servers. You've got a couple of options. Tell your CTO to buy another server, and maybe another hard drive, wait weeks for them to arrive, plug them in and add manually into your network. Hire people to manage the storage, manage the compute, make sure everything works, set up your hypervisor. You'd have to make sure that the drivers (software which interfaces with hardware) were correct, and worked with your existing infrastructure.

Imagine doing that for hundreds of servers. This is what (expensive) teams of infrastructure people do. And generally, its easier to keep compute separate from storage, and have separate teams. Which is more expense, and slower trouble shooting.

You might be thinking... who wants to do all that? We're a jellybean company, not a hardware infrastructure company. Pain in the ass. Along come AWS, Microsoft, Google who want to sell you their clouds. Except, you've just bought some servers! You want to use it, and you don't really trust your sensitive jellybean information to those cloud people anyway.

^1: I made this up. It's probably right. It's definitely mostly right.

### Convergence (Converged Infrastructure - CI)
Now the CTO starts talking about convergence. Companies like Hewlett Packard Enterprise and Cisco started offering pre-configured appliances that combine compute, storage, virtualisation control and (sometimes) networking components that are guaranteed to work well together. A bit like the Apple approach, where they have complete control of the components, rather than having to deal with different components from different suppliers which may or may not work well together.

Because those appliances all came pre-validated from one point of contact, it becomes much simpler to configure and manage them ("one throat to choke"). Note the components themselves may be from different vendors (eg: Cisco using EMC storage and VMware virtualisation, or Nutanix, with Lenovo, Dell, Supermicro components).

In short, you're removing decisions (type/provider of storage and compute, virtualisation, what works with what etc), and losing some flexibility (particular brand of hard-drive, virtualisation, motherboards etc) in the process. But your CTO assures you, it makes things simple. For example, it gets rid of the whole concept of a storage-area network, because your storage is part of the same appliance as your compute.

"Simple" you say, "I like simple!". 

"Maybe we should look at Nutanix then" your CTO replies.

### What about hyper-converged infrastructure (HCI)? 
At a basic level, HCI is convergence plus. The appliances are physically smaller and more tightly integrated. Nutanix delivers hyper-converged appliances. You can't separate the bits (eg: you can't pull out and replace a hard drive) like you could do with CI.

So you give up even more flexibility to gain more simplicity.

So this is what Nutanix do.
> Kind of. It's more what they did. See below. 

They provide pre-packaged boxes you plug into your server rack (hyper-converged appliances). They're all set up with storage and compute and network, as well as having the Nutanix operating system (Acropolis), virtualisation solution (AHV), and storage controller software installed. In short, they're ready to go, and probably much more performant (?) because the storage is located on the same box as the compute, ie, no network traffic for data access.

For geek interest, each Nutanix appliance has 1-4 nodes, that is 1-4 compute units (each with a storage controller) and each with a configurable number of SSDs and HDDs in a 2U form factor. The software replicates data across units (and across cluster) (as opposed to RAID which uses redundant disk space or drives on the same unit). Adding a new appliance, just rack and stack, the node is auto discovered, and can be set up with a couple of clicks in the UI.

### Forget everything above...

Hyper-convergence is a big trend in order to get the simplicity of cloud infrastructure into private datacenters, as well as controllable performance. Essentially, a software-defined datacenter, built on pre-configured appliances that define your compute, storage, virtualisation set up, and nice software that a) gets everything talking to each other (big pool of compute and storage, as well as backups etc) and b) lets you manage everything in one nice UI.

In summary, you get:

1. Repeatable simplicity in your datacenter. Want more compute? plug in another appliance. Want more storage? plug in another appliance.
2. Manage everything through the one UI.
3. Forget about your servers, and deal with one big pool of compute and storage.
4. Stop paying some much for over-capacity. 
5. HCI software deals with all the minutiae of this stuff, like data replication, 
6. Make sure you're optimising your current resources, and only spend for the capacity you need.

The idea is you get a lot of higher level flexibility (which apps run where) and simplicity, and the ability to focus on managing applications and selling jellybeans, rather than having expensive teams setting up servers and hard drives all day. In exchange, you lock into a HCI provider (I can't see it making a lot of sense to mix and match HCI providers), give up the hardware level flexibility and pay the fee.

In the beginning, I was pegging Nutanix more or less as an HCI provider with some nice software, which is sort of true, but ...

>We are a compute storage networking security and application mobility company. It's an entire operating system

and
> We now have a meaningful competitive advantage in being the most portable operating system built for the enterprise cloud. This kept growing our total addressable market as we ported our software to all these platforms in the last three years. A software only form factor gives us ubiquity.

So all the cool hardware stuff I mentioned above... you can pretty much forget about it. Nutanix wants to be the "enterprise cloud operating systems company", which works across your datacenter and across the cloud.

> My take: Nutanix is sitting above your private datacenter and your public clouds and acting as an operating system across everything.

I believe this transition is inevitable, because public clouds won't (and will never) do everything for everyone. Anyone who is running their own datacenter will have to make this sort of transition at some stage, otherwise you'll be left with a private datacenter that uses crappy tools and is difficult to scale, while the public cloud tools become easier and more compelling.

The main takeaway I have (after years of experience with AWS) is ... there's no alternative to AWS'ing your private datacenter. You have to go down this road to make sure you're getting the best value for your IT spend. And if you're running your own datacenter, you probably still want to utilise cloud resources for non-critical workloads.

The only question is, how much of the market can Nutanix capture, and at what margins?

##### Hardware agnostic
Note that Acropolis doesn't need to run on Nutanix hardware. You can run it on other hardware in your datacenter. This is an important  point, because who wants to buy brand new Nutanix boxes when you've got a datacenter full of OEM HCI boxes just sitting there?

Nutanix is actively pursuing this software focus, I guess similarly to how Microsoft took over the PC, by licensing the software (Windows) to OEM manufacturers. So less and less revenue will come from hardware, and more from software sales, which suggests that cost of revenue will decrease and gross margins go up.

**Note: Nutanix is not a SaaS company (at the moment). Very little of their deferred revenue comes from subscriptions, but from support contracts. They're looking to change this going forward.**

#### Containerisation (feel free to skip)
Not sure how relevant this is, just for completeness. Containerisation is another level of virtualisation. With virtual machines, each 'machine' has its own copy of the operating system (eg, linux or windows). Operating systems are pretty large (sometimes, mostly, especially windows) which can make rolling out another version of the virtual machine unweildy, so scaling up can be slow. Think of the use case where your application suddenly gets a big spike in traffic (because you put out a special offer on jellybeans for example). You need more copies of your application.

Standing up a new VM will take a while because you essentially have to stand up a whole new (virtual) machine (unless you have one sitting there waiting) so in the meantime, your application performance will suffer.

Containers just use the underlying server (or virtual machine) operating system and package everything else required to run your application. Containers tend to be pretty small (because they don't include the whole operating system unlike VMs), so can be easily sent around networks, and are much faster to install. You will already have a bunch of virtual machines running, so the idea is that you just install the container on an already running virtual machine that is running on a server with a bit of capacity, making scale up and down much (much!) faster.

The use cases are mostly different however. Containerisation makes sense when running multiple copies of the same application. Virtualisation is running multiple machines (which can then run multiple containers). Scaling up becomes a 'simple' matter of targetting a cluster of machines, and asking the provisioning software to make sure there are enough instances running (this is what Pivotal.io do).

Incidentally, you'll hear the Kubernetes word whenever you're looking at this space. Kubernetes organises the deployment and automatic scaling of containers, and is pretty much the (low-level) standard for doing this.


### Products
#### Acropolis
> Distributed storage fabric, Acropolis hypervisor, app mobility fabric.

Acropolis is the software that makes all the Nutanix appliances talk to each other and perform their functions. These functions include provision of the virtualisation/hypervisor functionality for the appliances (AHV - not sure how many installs actually use the Acropolis Hypervisor as opposed to other flavours), storage services (including caching, duplication and compression), networking capabilities for the appliances, backup and disaster recovery and I'm sure other stuff.

It's the operating system for Nutanix.

#### Prism
> A unified management plane to manage applications and infrastructure across different datacenters and clouds. Prism enables comprehensive datacenter management, operational insights, planning, and performance.

The UI for Nutanix appliances, and your software defined datacenter. Analytics, upgrades, and management functions.

#### Calm 
"Application automation and lifecycle management for the Nutanix and public clouds, as part of the Nutanix Enterprise Cloud OS. Calm orchestrates the provisioning, scaling and management of applications across multiple environments to make IT infrastructure more agile and application-centric."

Sounds like Kubernetes to me? On investigation, Calm is created from the calm.io acquisition in 2016. It appears to be the equivalent of CloudFoundry, Pivotal, Cloud66 etc. That is, getting your applications deployed (and scaled etc) to the place you want them deployed to.

Calm lets you do what CloudFoundry do, or in the AWS space, what ECS/EKS does, but across multiple clouds (eg, across your Nutanix datacenter private cloud and your AWS/Azure/Google clouds). It also gives a single point-of-view of all your cloud (public and private) resources, so for example, you can track down where you're spending what.

For geeks, as an example, you can set up a Kubernetes cluster on your Nutanix cluster, as well as in a public cloud (eg: Google) through the Calm interface.

#### Beam
"Multi-cloud optimization service delivered as part of the Nutanix Enterprise Cloud OS. Beam gives organizations deep visibility and rich analytics detailing cloud consumption patterns, along with one-click cost optimization across cloud environments."

Minjar Botmetic acquistion. I believe it provides insight and control over cloud costs, whats being spent on what by whom, and allow identification of underutilised (ie, over cost) capabilities. That is, analytics across all of your private and public cloud environments. So it grabs data from your Nutanix datacenters (can it grab data from non-Nutanix servers?) and data from AWS/Azure/Google etc., normalises it, and presents it so you can compare apples-to-apples across all clouds.

Summary: Analytics for all your clouds! It plugs into Prism.

#### Flow 
"Native virtual networking built into Nutanix AHV that includes VM Microsegmentation for application security. Flow Microsegmentation leverages an application-centric policy model that is backed by the granular control offered by a distributed stateful VM level firewall, all centrally managed via Prism."

This comes from the company’s recent acquisition of Netsil.

My best guess into Flow is that it extends Prism to allow application level security and firewall specification at a 'higher than app level, lower than perimeter (ie datacenter) level'. For example, in AWS you can specify security groups inside your cloud. Each security group is essentially a firewall, and has different ports allowed access.

On reflection, I believe Flow is really starting to move into the AWS/Security group space. They seem to be building out AWS type capability across the low-level components of datacenter and application deployment. What I mean by that is the blocks that you need in order to get applications to run. They don't package up databases etc. as AWS does, but focus on the server management and security side of things.

#### Era 
"Automates database operations such as provisioning and life cycle management. Copy data management is the first feature of Era. It is powered by a time machine technology that enables database cloning, refresh, and restore to any point in time with just a few simple clicks."

Time machine for databases. Moving along the same "do what AWS do but include private cloud" strategy that Calm, Beam and Flow fit into, Era is about database management. Initially it covers off backup and restore, similarly to AWS's snapshot support, but assume (although not certain) that it will cover more database functionality in the future (provisioning,scaling, auto patching, multi area deployments etc).

#### Xi Cloud
From: https://diginomica.com/2018/05/15/nutanix-partners-with-google-as-it-tries-to-make-the-clouds-all-disappear/
>The objective of Xi is to make all the clouds used by any business effectively invisible by bringing them under one management environment, which is effectively an abstraction layer.

and...

>One of the first applications for this approach is disaster recovery as a service, where Nutanix on premise customers can access the cloud service using Xi and run the primary applications there, should there be a problem with the on premise systems.

So... Xi cloud services is Nutanixs first move into selling services that integrate into their software. What you get is the simplicity of the familiar user interface, and Xi handles the provisioning off cloud services to support your requirements.

That sounds a bit gobbledygook! The first service is disaster recovery, which I believe provisions resources in Google Cloud. You click a few buttons in Prism, and suddenly you have robust DR across multiple data-centers, regions etc. The fact that its Google Cloud under the covers is invisible to you. Sure, you could do the same thing yourself, but ... it would take a lot of work. 

I expect Nutanix to build out capabilities in Xi Cloud for those common use-cases that span public and private datacenters (security would be an obvious one, but am sure theres a bunch of others).


## Numbers

### Basic data (based on TMF1000)

* Revenue was 289.41m up (0.9%) from 286.74m from the previous quarter (205.67m same quarter last year)
* TTM Revenue was 1.025b up (39.8%) from 733.23m 
* TTM Revenue per share (diluted) was 6.39 down (24.6%) from 8.48
* EPS diluted (prev quarter): was -0.51 down (30.8%) from -0.39
* Earnings (same quarter prev year): was -0.51 up (23.9%) from -0.67
* TTM eps was -1.79 up (57.5%) from -4.21
* Diluted share count was 166.85m up (15.8%) from 144.05m
* Cash and short-term investments  was 923.46m up (0.6%) from 918.25m (prev quarter)
* Debt (prev quarter) was 422.57m up (1.7%) from 415.65m (prev quarter)
* Cash flow for quarter was -788k down (102.5%) from 31.58m
* Cash flow for TTM was 17.26m up (147.4%) from -36.40m
* Cash flow per share for TTM was $0.10
* Gross margins was 0.67 up (7.7%) from 0.62
* CapExp was 14.10m up (0.5%) from 14.03m


Cash flow is pretty up and down (tending down!), but not huge amounts. Nutanix is losing money, and there doesn't really seem to be any indication that they'll stop anytime soon. Nothing super concerning, and good to see the improvement in gross margins, which is (I'm guessing) a result of the movement to software-only sales.

### Last reported quarter ranges min, max [last]
* Trading range between Sep 01, 2017 - Mar 31, 2018 was 22.85 to 54.66 [49.11]
* Market cap between Sep 01, 2017 - Mar 31, 2018 was 3.666b to 8.981b [8.069b]
* PE range (Sep 01, 2017 - Mar 31, 2018) not applicable (earnings < 0)
* PS ratio range (Sep 01, 2017 - Mar 31, 2018) was 3.72 to 8.90 [7.99]
* Free cash flow (TTM) yield range (Sep 01, 2017 - Mar 31, 2018) was 0.19 to 0.47 [0.21]
* EV/Sales between Sep 01, 2017 - Mar 31, 2018 was 3.39 to 8.81 [7.92]

### Most recent quarter ranges min, max [last] 
uses more recent price data with last reported results.

* Trading range between Apr 01, 2018 - Jun 30, 2018 was 47.66 to 63.71 [51.57]
* Market cap between Apr 01, 2018 - Jun 30, 2018 was 7.952b to 10.630b [8.473b]
* PE range (Apr 01, 2018 - Jun 30, 2018) not applicable (earnings < 0)
* PS ratio range (Apr 01, 2018 - Jun 30, 2018) was 7.76 to 10.37 [8.39]
* Free cash flow (TTM) yield range (Apr 01, 2018 - Jun 30, 2018) was 0.16 to 0.22 [0.20]
* EV/Sales between Apr 01, 2018 - Jun 30, 2018 was 7.27 to 9.88 [7.90]

### Revenue

| Quarter   | Revenue   | TTM     | 𝝳 (q-1)   | 𝝳 (YoY)   |
|:----------|:----------|:--------|:----------|:----------|
| 2015Q2    |           |         |           |           |
| 2015Q3    | 87.76m    |         |           |           |
| 2015Q4    | 102.70m   |         | 17%       |           |
| 2016Q1    | 114.69m   |         | 12%       |           |
| 2016Q2    | 139.78m   | 444.93m | 22%       |           |
| 2016Q3    | 188.56m   | 545.73m | 35%       | 115%      |
| 2016Q4    | 199.21m   | 642.25m | 6%        | 94%       |
| 2017Q1    | 205.67m   | 733.23m | 3%        | 79%       |
| 2017Q2    | 173.42m   | 766.87m | -16%      | 24%       |
| 2017Q3    | 275.55m   | 853.86m | 59%       | 46%       |
| 2017Q4    | 286.74m   | 941.39m | 4%        | 44%       |
| 2018Q1    | 289.41m   | 1.025b  | 1%        | 41%       |

Revenue for Nutanix comes from 3 major parts,
 1. Software sales
 2. Hardware sales
 3. Services
So (almost) all of the deferred revenue comes from the services section, see below for a discussion.

Revenue is growing strongly, although theres a bit of a slowing in growth going on over the last few quarters. They are transitioning from hardware sales to software sales, with less revenue coming from hardware as they build Acropolis etc to be ubiquitous across different hardware platforms.

### Deferred revenue

| Quarter   | Def.Revenue   | 𝝳 (q-1)   | 𝝳 (YoY)   | Billings (Rev + 𝝳 def. rev) 
|:----------|:--------------|:----------|:----------|:---------------------|
| 2016Q2    | 296.46m       |           |           |                      |
| 2016Q3    | 375.43m       | 27%       | 262%      | 267.53m              |
| 2016Q4    | 420.62m       | 12%       | 306%      | 244.40m              |
| 2017Q1    | 463.00m       | 10%       | 347%      | 248.05m              |
| 2017Q2    | 369.06m       | -20%      | 24%       | 79.48m               |
| 2017Q3    | 408.84m       | 11%       | 9%        | 315.34m              |
| 2017Q4    | 478.00m       | 17%       | 14%       | 355.90m              |
| 2018Q1    | 539.89m       | 13%       | 17%       | 351.30m              |

Deferred revenue really confused me. I didn't think Nutanix had any sort of subscription revenue, so ... where was all the deferred revenue coming from? Reading the 10Q's seemed to confirm my initial thoughts. I contacted Investor Relations (who were really helpful) who confirmed that the deferred revenue is almost all from support contracts. So very little to no subscription revenue.

>The next phase, as presented at our March Investor Day, would be to sell more subscriptions... - Investor Relations

Deferred revenue is pretty substantial, although they also have deferred commissions payable, which takes a little of the shine off (for example, in the last Quarter, they had about $100m of deferred commissions payable).


### Margins

|    | Quarter   | Gross margin   | ebitdamargin   | netmargin   |
|---:|:----------|:---------------|:---------------|:------------|
|  0 | 2016Q2    | 61%            | -30%           | -36%        |
|  1 | 2016Q3    | 63%            | -70%           | -74%        |
|  2 | 2016Q4    | 61%            | -33%           | -38%        |
|  3 | 2017Q1    | 60%            | -41%           | -47%        |
|  4 | 2017Q2    | 57%            | -35%           | -40%        |
|  5 | 2017Q3    | 61%            | -17%           | -22%        |
|  6 | 2017Q4    | 62%            | -17%           | -22%        |
|  7 | 2018Q1    | 67%            | -25%           | -30%        |

Gross margins are improving, as would be expected as they move away from the low margin hardware business. I estimate that gross margins could approach mid to low seventies.

### Free cash flow

| Quarter   | FCF     |
|:----------|:--------|
| 2016Q2    | -6.51m  |
| 2016Q3    | -7.75m  |
| 2016Q4    | 7.05m   |
| 2017Q1    | -29.19m |
| 2017Q2    | -6.46m  |
| 2017Q3    | -7.86m  |
| 2017Q4    | 32.37m  |
| 2018Q1    | -788k   |


### Capital structure

|        | Cash    | Investments   | Cash and investments   | Working Capital   | Debt    |   Debt to Equity |   Interest |
|:-------|:--------|:--------------|:-----------------------|:------------------|:--------|-----------------:|-----------:|
| 2016Q2 | 99.21m  | 85.99m        | 185.20m                | 117.10m           | 73.26m  |            -0.19 |          0 |
| 2016Q3 | 225.46m | 121.65m       | 347.11m                | 272.44m           | 0.00    |             0    |          0 |
| 2016Q4 | 226.01m | 129.15m       | 355.15m                | 249.26m           | 0.00    |             0    |          0 |
| 2017Q1 | 200.77m | 149.57m       | 350.35m                | 230.51m           | 0.00    |             0    |          0 |
| 2017Q2 | 138.36m | 210.69m       | 349.05m                | 269.06m           | 0.00    |             0    |          0 |
| 2017Q3 | 132.46m | 233.49m       | 365.94m                | 273.95m           | 0.00    |             0    |          0 |
| 2017Q4 | 610.45m | 307.81m       | 918.25m                | 788.00m           | 415.65m |             1.38 |          0 |
| 2018Q1 | 376.79m | 546.67m       | 923.46m                | 796.63m           | 422.57m |             1.19 |          0 |

Capital structure looks pretty sound (my opinion FWIW!). The debt component is the convertible note offering that was announced in January 2018 which allows note holders to convert to stock at a price of about $48.85 dollars.

### Expenses

| Quarter   | R and D   | Change (q-1)   | Change (YoY)   | Sales, General, Admin   | Change (q-1)   | Change (YoY)   |
|:----------|:----------|:---------------|:---------------|:------------------------|:---------------|:---------------|
| 2016Q2    | 35.13m    |                |                | 98.21m                  |                |                |
| 2016Q3    | 75.28m    | 114%           |                | 158.00m                 | 61%            |                |
| 2016Q4    | 70.91m    | -6%            |                | 126.86m                 | -20%           |                |
| 2017Q1    | 74.61m    | 5%             |                | 142.36m                 | 12%            |                |
| 2017Q2    | 67.82m    | -9%            | 93%            | 149.38m                 | 5%             | 52%            |
| 2017Q3    | 64.51m    | -5%            | -14%           | 161.46m                 | 8%             | 2%             |
| 2017Q4    | 70.92m    | 10%            | 0%             | 167.15m                 | 4%             | 32%            |
| 2018Q1    | 81.29m    | 15%            | 9%             | 194.79m                 | 17%            | 37%            |

As you'd expect sales, general and admin make up the biggest chunk of expenses for Nutanix (the number for last quarter is $169.86m). Their business model is the land-and-expand model, so sales people will be an increasing part of their expenses.

### DCF
The current share price is at $52 (28 June 18). Using a compounded revenue growth rate of 25% over the next 5 years (dropping to 2.25% over the next 5) and an EBIT margin of 30% (as per current year) and a WACC of 9% gives an estimated share value of _$46_. 

Over the ten year period using these values, revenue will grow to around $5.3b. Any increase (decrease) in revenue growth or margins (all things equal) will increase (decrease) this share price.

#### DCF examples

.|5 year CAGR | 20% | 25% | 30% | 35% | 40%
---------|------------|-----|-----|-----|-----|-----
Operating margin|Implied 10 year revenue. |$4b |$5.3b |$7b |$9.2b | $12b
20% |                 | $18 |$21 |$26 |$33  |$41
30% |                 | $36 |$46 |**$58** |**$74**  |**$93**
40% |                 | **$54** |**$70** |**$90** |**$115** |**$146**



### Comments
Nutanix is growing strongly, over a year and a half more than doubling revenue, with really good gross margins of above 60%, and appear to have a fairly stable free-cash-flow situation.

A lot has been made of the software-centric model, where Nutanix supplies software to OEM HCI boxes. I was a bit surprised when I discovered that the Billings increase was due to support contracts, rather than ongoing software subscriptions. Nutanix definitely isn't a SaaS business, but  it's making the first steps towards that goal (with Calm, Beam, Flow, Era and Xi).

> but the next 12 to 18 months, we really have to think about a hybrid license model - Dheeraj Pandey

I think my bottom line is that the transition to HCI is (IMO) inevitable for all companies running their own datacenter. They either do that, or shift entirely to the public cloud, and Nutanix is a very strong player in the top end of that market. As far as I can see, theres no financial concerns to worry about, and it will be a matter of watching revenue (and customer) growth, as well as margin control. Cost of revenue should continue to decrease as a percentage of revenue as Nutanix shift to the software-centric model.

Overall, I really like Nutanix, much more than when I started this deep-dive. Are the shares cheap? Not really, the DCF is suggesting (all other things being equal!) growth of around 30% and EBIT margins of 30%, so higher share price would require exceeding those values. But, thats not off the table.

The fact they're spending a lot more than they're making is also an issue obviously, but my consideration is that once you're in with Nutanix it would be very difficult to switch, so the land-and-expand model makes a lot of sense.

I think the next quarter report will be the critical one. If growth rates continue and it looks like they're going to beat their 

## Updates
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTIwMzk2NTY2MTgsLTEzMTk3NTA3NzAsNz
MyNTI0OTExLC0xMzMxNjMxOTY0XX0=
-->