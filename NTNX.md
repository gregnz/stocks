# NTNX 

## My understanding
Nutanix is a leader in 'Hyper-converged infrastructure'. Uh... cool.

Lets say you've decided to run a datacenter to power your jellybean company. You've got a windows app you want to run that lets you sell jellybeans. You tell your CTO and they run out and buy some servers, hard-drives and a (Arista!) switch to plug everything together. They set everything up, install Windows, and the devops team slap your application on top, and you're done. Easy.

And then what happens? Someone wants to run a reporting application. Except it runs on Linux, not Windows. You don't really want to buy a whole new server, just to run a little linux app. Your CTO starts talking about virtualisation and the benefits of virtual machines.

### What's a virtual machine?

Virtualisation splits your physical server into abstracted servers. Normally, your operating system interacts with the hardware (memory, cpu, harddrive etc) of your server. However, install some special software called a _Hypervisor_, and the OS talks to the hypervisor. The hypervisor then talks to the actual hardware.

What does that do? It lets you install multiple pretend-computers (virtual machines) on your single server. The hypervisor is in charge of divvying up the server resources (memory, compute, storage etc) to each virtual machines. Each virtual machine has no idea it's running on a single server, its all hidden by the hypervisor.

So you could pretend you had two servers (for example, a windows server and a linux server) all the while running them on one physical server in your datacenter. Or 3 servers. Or as many servers as you had capacity for on your physical hardware.

It's very cool, and virtual machines are the basis for every^1 data-center architecture.

Except... what happens when you need more compute power? Or more hard drive space? You've still got the problem of actually managing and provisioning all the servers. You've got a couple of options. Tell your CTO to buy another server, and maybe another hard drive, wait weeks for them to arrive, plug them in and add manually into your network. Hire people to manage the storage, manage the compute, make sure everything worked, set up your hypervisor. You'd have to make sure that the drivers (software which interfaces with hardware) were correct, and worked with your existing infrastructure.

Imagine doing that for hundreds of servers. This is what (expensive) teams of infrastructure people do. And generally, its easier to keep compute separate from storage, and have separate teams. Which is more expense, and slower trouble shooting.

You might be thinking... who wants to do all that? We're a jellybean company, not a hardware infrastructure company. Pain in the ass. Along come AWS, Microsoft, Google who want to sell you their clouds. Except, you've just bought a server! You want to use it, and you don't really trust your sensitive jellybean customer information to those cloud people anyway.

#### A bit more on Hypervisors (feel free to skip)
I glossed over the hypervisor above, and you can probably skip this section. But to recap, the Hypervisor is like a super-minimal operating system that lets multiple operating system in virtual machines to have access to the underlying hardware.

There are 'type 1' and 'type 2' hypervisors. A type-1 hypervisor runs directly on the underlying hardware, while a 'type 2' needs an installed operating system. 

TODO: MORE HERE about AVM

^1: I made this up. It's probably right. It's definitely mostly right.

### Convergence (Converged Infrastructure - CI)
Now the CTO starts talking about convergence. Companies like Hewlett Packard Enterprise and Cisco started offering pre-configured appliances that combine compute, storage, virtualisation control and (sometimes) networking components that are guaranteed to work well together. A bit like the Apple approach, where they have complete control of the components, rather than having to deal with different components from different suppliers which may or may not work well together.

Because those appliances all came pre-validated from one point of contact, it becomes much simpler to configure and manage them. Note the components themselves may be from different vendors (eg: Cisco using EMC storage and VMware virtualisation, or Nutanix, with Lenovo, Dell, Supermicro components).

In short, you're removing decisions (type/provider of storage and compute, virtualisation, what works with what etc), and losing some flexibility (particular brand of hard-drive, virtualisation, motherboards etc) in the process. But your CTO assures you, it makes things simple. For example, it gets rid of the whole concept of a storage-area network, because your storage is part of the same appliance as your compute.

"Simple" you say, "I like simple!". 

"Maybe we should look at... Nutanix then" your CTO replies.

### What about hyper-converged infrastructure (HCI)? 
At a basic level, HCI is convergence plus. The appliances are physically smaller and more tightly integrated. Nutanxi deliver hyper-converged appliances. You can't separate the bits (eg: you can't pull out and replace a hard drive) like you could do with CI.

So you give up even more flexibility to gain more simplicity.

So this is what Nutanix do (Kind of. It's the basis of what they do. See below). They provide pre-packaged boxes you plug into your server rack (hyper-converged appliances). They're all set up with storage and compute and network, as well as having the Nutanix operating system, virtualisation solution, and storage controller software installed. In short, they're ready to go, and probably much more performant (?) because the storage is located on the same box as the compute, ie, no network traffic for data access.

For geek interest, each Nutanix appliance has 1-4 nodes, that is 1-4 compute units (each with a storage controller) and each with a configurable number of SSDs and HDDs in a 2U form factor. The software replicates data across units (and across cluster) (as opposed to RAID which uses redundant disk space or drives on the same unit). Adding a new appliance, just rack and stack, the node is auto discovered, and can be set up with a couple of clicks in the UI.

### So Nutanix make HCI hardware you can plug and play?

Exactly! But that's the wood for the trees. All the stuff above (more or less) is hardware focussed. Smaller, integrated hardware. 

But tree view of Nutanix is about shifting from the hardware focus of CI/HCI to being software-focussed. A software-defined datacenter. You can plug these HCI appliances (that contain compute, storage, virtualisation and network) into your racks, and use your management console to create new virtual machines, and just run your applications on them. 

> My take: _HCI is "AWS'ing" your companies datacenter_.

Your clever software lets you see all your compute as something you can define. You can set up software-defined storage that cleverly lets you access all the storage across your datacenter, and deals with backups and compression and so forth that lets you sell jellybeans 24/7 with 0.9999 uptime. It might even let you do no-downtime deploys of your jellybean-selling app. The same way that AWS lets you add new 'servers' (in reality virtual machines)

But the secret is the software. It's very analogous to Arista. What Arista do for networks, Nutanix is doing for datacenters. They're really both software companies, selling simplicity and performance on top of pretty boxes made of commodity components.

**Update: Nutanix is agressively moving away from appliances to the software side of things. So selling the Acropolis/Prism suite while running on OEM hardware from partners.**


### Enterprise Cloud
Thats the private datacenter story. It's really a simplicity versus cost story, and personally I found it pretty compelling. Is it more compelling than the other options? Not sure.

However, the more interesting is that Nutanix has a major focus on 'Enterprise cloud', which means seeing your private datacenter _and_ your public cloud as parts of the same thing. If you want to run your main applications in your private datacenter, and then failover to public cloud, thats something you can do using the same Nutanix interface.

#### My understanding...

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

Nutanix wants to be the integration layer across on-premise infrastructure and public cloud. You stop caring about public versus private compute, and just use what you need when you need it, within whatever policy you have for putting things on public clouds.

I believe this transition is inevitable, because public clouds won't (and will never) do everything for everyone. Anyone who is running their own datacenter will have to make this sort of transition at some stage, otherwise you'll be left with a private datacenter that uses crappy tools and is difficult to scale, while the public cloud tools become easier and more compelling.

The main takeaway I have (after years of experience with AWS) is ... there's no alternative to AWS'ing your private datacenter. You have to go down this road to make sure you're getting the best value for your IT spend. 

The only question is, how much of the market can Nutanix capture, and at what margins?

##### Hardware agnostic
A final note, Acropolis doesn't need to run on Nutanix hardware. You can run it on other hardware in your datacenter. This is an important  point, because who wants to buy brand new Nutanix boxes when you've got a datacenter full of OEM boxes just sitting there?

Nutanix is actively pursuing this software focus, I guess similarly to how Microsoft took over the PC, by licensing the software (Windows) to OEM manufacturers. So less and less revenue will come from hardware, and more from software sales, which suggests that cost of revenue will decrease and gross margins go up.

#### Containerisation
Not sure how relevant this is, just for completeness. Containerisation is another level of virtualisation. With virtual machines, each 'machine' has its own copy of the operating system (eg, linux or windows). Operating systems are pretty large (sometimes, mostly, especially windows) which can make rolling out another version of the virtual machine unweildy, so scaling up can be slow. Think of the use case where your application suddenly gets a big spike in traffic (because you put out a special offer on jellybeans for example). You need more copies of your application.

Standing up a new VM will take a while because you essentially have to stand up a whole new (virtual) machine (unless you have one sitting there waiting) so in the meantime, your application performance will suffer.

Containers just use the underlying server (or virtual machine) operating system and package everything else required to run your application. Containers tend to be pretty small (because they don't include the whole operating system unlike VMs), so can be easily sent around networks, and are much faster to install. You will already have a bunch of virtual machines running, so the idea is that you just install the container on an already running virtual machine that is running on a server with a bit of capacity, making scale up and down much (much!) faster.

The use cases are mostly different however. Containerisation makes sense when running multiple copies of the same application. Virtualisation is running multiple machines (which can then run multiple containers). Scaling up becomes a 'simple' matter of targetting a cluster of machines, and asking the provisioning software to make sure there are enough instances running (this is what Pivotal.io do).

Incidentally, you'll hear the Kubernetes word whenever you're looking at this space. Kubernetes organises the deployment and automatic scaling of containers, and is pretty much the (low-level) standard for doing this.


### Other offerings
#### HPE Simplivity
Appears to be the big, most direct competition. Simplivity was purchased by HPE at the start of 2017, which is pretty much the same as Nutanix's HCI offering.

HyperFlex (Cisco)
HP OneView.

Azure Stack.


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

Summary: analytics for all your clouds! It plugs into Prism.

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

>...

>One of the first applications for this approach is disaster recovery as a service, where Nutanix on premise customers can access the cloud service using Xi and run the primary applications there, should there be a problem with the on premise systems.

Xi Cloud is interesting. My first view on seeing some discussion with the CEO was that they were trying to replicate AWS, Azure etc. My current understanding is that Xi is actually an integration layer between Nutanix Prism and public cloud.







## Numbers

### Basic data (based on TMF1000)

* Revenue was 289.41m up (0.9%) from 286.74m from the previous quarter (205.67m same quarter last year)
* TTM Revenue was 1.025b up (59.6%) from 642.25m 
* TTM Revenue per share was 6.39 down (33.6%) from 9.63
* Earnings (prev quarter): was -0.51 down (30.8%) from -0.39
* Earnings (same quarter prev year): was -0.51 up (23.9%) from -0.67
* TTM eps was -1.79 up (61.0%) from -4.59
* Diluted share count was 166.85m up (15.8%) from 144.05m
* Cash  was 376.79m down (38.3%) from 610.45m (prev quarter)
* Debt (prev quarter) was 422.57m up (1.7%) from 415.65m (prev quarter)
* Cash flow for quarter was -788k down (102.5%) from 31.58m
* Cash flow for TTM was 17.26m up (194.8%) from -18.20m
* Cash flow per share for TTM was $0.10
* Gross margins was 67% up (7.7%) from 62%
* CapExp was 14.10m up (0.5%) from 14.03m

### Last reported quarter ranges min, max [last]

* Trading range between Sep 01, 2017 - Mar 31, 2018 was 22.85 to 54.66 [49.11]
* Market cap between Sep 01, 2017 - Mar 31, 2018 was 3.666b to 8.981b [8.069b]
* PE range (Sep 01, 2017 - Mar 31, 2018) not applicable (earnings < 0)
* PS ratio range (Sep 01, 2017 - Mar 31, 2018) was 3.72 to 8.90 [7.99]
* Free cash flow yield range (Sep 01, 2017 - Mar 31, 2018) was 0.19 to 0.47 [0.21]
* EV/Sales between Sep 01, 2017 - Mar 31, 2018 was 3.39 to 8.81 [7.92]

### Most recent quarter ranges min, max [last] 
uses more recent price data with last reported results.

TODO: THE MAR 01 2018 Number is wrong. It should be APR 1 2018

* Trading range between Mar 01, 2018 - Jun 27, 2018 was 47.66 to 63.71 [51.64]
* Market cap between Mar 01, 2018 - Jun 27, 2018 was 7.952b to 10.630b [8.485b]
* PE range (Mar 01, 2018 - Jun 27, 2018) not applicable (earnings < 0)
* PS ratio range (Mar 01, 2018 - Jun 27, 2018) was 7.76 to 10.37 [8.40]
* Free cash flow yield range (Mar 01, 2018 - Jun 27, 2018) was 0.16 to 0.22 [0.20]
* EV/Sales between Mar 01, 2018 - Jun 27, 2018 was 7.80 to 10.41 [8.45]

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

Revenue is growing strongly, although theres a bit of a slowing in growth going on over the last few quarters. They are transitioning from hardware sales to software sales, with less revenue coming from hardware (TODO - Fill in CC discussion).

Q1 and Q3 are reputedly weak...



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

Capital structure looks pretty sound. The debt component is the convertible note offering that was announced in January 2018 which allows note holders to convert to stock at a price of about $48.85 dollars. There are several clauses as to when the notes can be exercised... TODO MORE HERE. Is it even relevant? Check TMF1000 to see the kind of commentary

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


### Comments
Nutanix is growing strongly, over a year and a half more than doubling revenue, with really good gross margins of above 60%, and appear to have a fairly stable free-cash-flow situation.

A lot has been made of the software-centric model, where Nutanix supplies software to OEM HCI boxes. I was a bit surprised when I discovered that the Billings increase was due to support contracts, rather than ongoing software subscriptions. Nutanix definitely isn't a SaaS business, but perhaps it's making the first steps towards that goal.

> but the next 12 to 18 months, we really have to think about a hybrid license model - Dheeraj Pandey

I think the bottom line is that the transition to HCI is (IMO) inevitable for all companies running their own datacenter. They either do that, or shift entirely to the public cloud, and Nutanix is a very strong player in the top end of that market. As far as I can see, theres no financial concerns to worry about, and it will be a matter of watching revenue (and customer) growth, as well as margin control. Cost of revenue should continue to decrease as a percentage of revenue as Nutanix shift to the software-centric model.

### DCF
Using a compounded revenue growth rate of 25% over the next 5 years and an EBIT margin of 30% (as per current year) and a WACC of 9% gives an estimated share value of _$202_.

Over the ten year period, revenue will grow to around $50b, around about the current revenues of Disney (2017 - $55b), Cisco ($49b), and Intel ($59b).

Any decrease in revenue growth or margins (all things equal) will decrease this share price.

#### DCF examples

---------|5 year CAGR | 20% | 25% | 30% | 35% | 40%
---------|------------|-----|-----|-----|-----|-----
Operating margin|Implied 10 year revenue. |$4b |$5.3b |$7b |$9.2b | $12b
20% |                 | $18 |$21 |$26 |$33  |$41
30% |                 | $36 |$46 |$58 |$74  |$93
40% |                 | $54 |$70 |$90 |$115 |$146

#### Comparisons
Revenues (2017) for comparison include Amazon ($135b), Microsoft ($85b), Alphabet ($90b), Cisco ($49b), Oracle ($37b).

Company      | Rev (TTM)| Rev Growth% | OpMargin% | NP %
-------------|----------|-----|-----|-----
Amazon       | $93      |$118 |$149 |$237 
Microsoft    | $140.    |$179 |$228 |$367
Alphabet     | $111b    |23% |24% |20%

#### Other numbers
Metric      | Value
------------|----------
PEG                    | .6
P/E (MRY)              | 49 
Gross Margin (TTM).    |60%
Operating Margin (TTM) |33%
Net profit Margin (TTM)|30%

---
---
---
---
CORPORATE FINANCIALS

Over the recent past 52-week period, the TREX stock price has soared 100.6% from a low of $64.66/share to a new high of $129.75 last Friday on 6/8/2018.
	
MARKET CAP     $ 3.8 B	
Employees	 1,120
	
52-WK HIGH	129.75
PRICE 6/8/18	129.28
52-WK LOW	 64.66
	
EV/EBITDA (mrq)	 20.12
P/E	         40.15
Fwd P/E	         27.05
EV/Sales (ttm)	  5.67
P/S (ttm)	  6.33

Reflecting the company's positive outlook, Trex Board of Directors has approved a 2-for-1 stock split of the Company’s common shares. The stock split will be in the form of a stock dividend to be distributed on June 18, 2018 to shareholders of record on May 23, 2018. Additionally, in the 2018 first quarter Trex repurchased 50,000 common shares for a total expenditure of $5 million as part of its share buyback program approved by the Board of Directors in February 2018.

Revenue, Net Income and Earnings

	 REVENUE   YoY	  NET INCOME    YoY        EPS       YoY
FY/QTR	  ($ M)	  Change     ($ M)    Change  ($)diluted   Change
						
Q1 ‘18   171.207   18.2%    37.110    32.8%       1.25	    31.6%
						
FY '17	 565.153   17.8%    95.128    40.2%       3.22	    40.6%
						
Q4 ‘17	 122.212   28.2%    18.299    44.9%       0.62	    44.2%
Q3 ‘17	 140.194   32.0%    20.098   158.1%       0.68     161.5%
Q2 ‘17	 157.941    7.8%    28.782    21.3%       0.97	    21.3%
Q1 ‘17	 144.806   10.0%    27.949    17.9%       0.95	    18.8%
						
FY '16	 479.616    8.8%    67.847    41.1%       2.29	    50.7%
					
Q4 ‘16	  95.322	    12.629	          0.43	
Q3 ‘16	 106.168	     7.787	          0.26	
Q2 ‘16	 146.450	    23.725	          0.80	
Q1 ‘16	 131.676	    23.706	          0.80	
						
FY '15	 440.804   12.5%    48.098    15.8%       1.52	    19.7%
FY '14	 391.660   14.3%    41.521    20.0%       1.27	    25.7%
FY '13	 342.511	    34.598	          1.01	

What really stands out in the above table are the substantially large positive YoY % changes in net income and earnings, annually and quarterly, that significantly outpace their respective annual and quarterly sales growth.

In FY 2017, total sales increased almost 18%, reaching $565 million, of which 13% represented growth within the company’s legacy business, the Trex Residential Products segment. The remaining 5% growth reflects the results of its 2017 acquisition of SC Company that became the Trex Commercial Products segment. Trex was able to expand its gross profit margin through continued manufacturing cost savings, lower input costs and higher capacity utilization. As a result, Trex delivered $3.22 of diluted earnings per share in 2017, a 41% increase over 2016, which considerably outpaced sales growth.

While some of the gross margin expansion was due to lower scrap polyethylene prices, the vast majority of it was a product of operating leverage and recent projects to improve production processes and drive operating leverage even higher. CEO James Cline reported: Fast-return projects to streamline production processes and reduce our input costs have methodically reduced manufacturing costs, while sales growth has driven increased capacity utilization, combining to drive significant operating leverage. CFO Bryan Fairbanks pointed out that we expects to continue seeing gains here and we expect to continue to see the benefits from our ongoing manufacturing cost efficiencies and from increased capacity utilization as we scale the business.

For the second quarter of 2018, CEO Cline projected, we expect consolidated net sales of $191 million, comprised of approximately $174 million from Trex Residential Products and $17 million from Trex Commercial Products. This will represent a year-on-year growth of 10% for Residential and 21% on a consolidated basis. Our projected effective tax rate for the year remains at approximately 25%. We forecast our full year 2018 incremental margin to remain at approximately 45% to 50%.

Margins

All margins are realizing significant increases as the company plans to further drive down manufacturing costs and increase throughput from the residential decking business, while also improving the profitability of the new commercial products segment.

MARGINS   GROSS  OPERATING   PROFIT
			
Q1 ‘18	  44.8%    27.9%      21.7%
			
FY 2017   43.1%	   25.2%      16.8%
FY 2016	  39.0%	   21.7%      14.2%
FY 2015	  35.1%	   17.6%      10.9%
FY 2014	  35.8%	   17.3%      10.6%
FY 2013	  28.7%	    7.2%      10.1%


Return on Invested Capital (ROIC)-Weighted Average Cost of Capital (WACC) Spreads

Trex has realized substantial growth in ROIC and ROIC-WACC spreads. As of 6/8/18, Trex is creating 31.9 cents of pure economic value add (EVA) for every dollar invested.

    Date	   ROIC	   WACC	    EVA
			
    6/8/18    45.5%	  13.6%   31.9%
    Q1 ‘18	  54.8%	  13.4%   41.5%
			
    FY 2017   60.4%	  14.1%	  46.3%
    FY 2016	  58.9%	  15.2%	  43.7%
    FY 2015	  43.8%	  18.2%	  25.7%
    FY 2014	  40.7%	  18.3%	  22.4%
    FY 2013	  35.5%	  16.0%	  19.5%

Free Cash Flow
Trex continues to maintain good FCF.
			
	     FCF							
FY 2017	  $ 86.83 M		
FY 2016	  $ 70.74 M		
FY 2015	  $ 39.30 M		
FY 2014	  $ 45.87 M		
FY 2013	  & 32.15 M		


Capital Structure
Trex maintains a solid capital structure as shown in the following table.
	
Cash (mrq)	         $ 2.7 M
Working Capital	        $ 86.269 M
Total Debt (mrq) 	$ 84.5 M
Total Equity (mrq)     $ 261.86 M
Total Capitalization   $ 346.36 M
LT Debt/Equity	          32.2%
Debt/Capitalization	  24.4%
Current Ratio (mrq)	   1.76

Stock-based Compensation

SBC/revenue ratios are favorably low.

FY/QTR	  SBC	SBC/Revenue
	($ M)	
		
Q1 ‘18	  2.30	  1.3%
		
FY 2017   5.19	  0.9%
FY 2016	  4.79	  1.0%
FY 2015	  4.86	  1.1%
FY 2014	  4.81	  1.2%
FY 2013	  3.81	  1.1%

=================================
---
---
---
---




## Whats going on with their sales and marketing expense?!?


## Definitions
Hypervisor
Level 1 Hypervisor (bare metal)
Level 2 Hypervisor (hosted)
Virtual machine
Blades
Virtual storage appliance - A virtual storage appliance (VSA) is a storage controller that runs on a virtual machine (VM) to create shared storage without the cost of additional hardware.
2U form factor - takes up 2 units of height in a standard rack.


resources
https://www.youtube.com/watch?v=N46PFNZE9zM
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTA2MDQ4MDM4NCwtMTU3NTMyNDkyOSwtMT
g5MDY5NjU5MiwtMTA5OTA4ODI4LDEwOTEyNDEyNjIsMTU5ODQ3
MjIzNywtMTM3MDA1MTc0LC0yMDczMTAyODQsMTUyNjkwNDY0My
wtMjEzNzAxMiwxMDE2NDkyMDUzLC0zNjUzNTgyODgsMTA3ODg5
ODMzMSwtMTA0OTIxOTk1N119
-->