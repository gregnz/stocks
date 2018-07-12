# NVDA
GCon = 1 to 5 scale of ‘Gregs conviction’.  
Most buzzwords are in the 'Definitions' section.

## My understanding

Nvidia produces GPU (graphical processing unit) chips. GPUs are developed to be massively parallel floating point processors, which excel at rendering graphics for games.

Think of CPUs which are single-core, dual-core, quad-core, sometimes 8-16 cores. These are the parallel processing brains, so a quad-core CPU can process four concurrent tasks. CPUs are optimised for sequential serial processing.

GPUs on the other hand have thousands of less powerful cores, which means they can run thousands of simpler tasks concurrently. For example, the Geforce GTX 1080Ti has 3584 cores.

https://youtu.be/-P28LKWTzrI
:-)

There are a bunch of technologies that benefit from massive parallel processing. Graphics, cryptocurrency mining, AI, etc. They all do (more or less) the same thing with slightly different data. These are the big tides lifting Nvidias boat.

The major point is that currently GPUs are the 'solution-du-jour' for ubiquitous parallel processing. There are other technologies that are better for some situations, but in general, GPUs are the best at solving the general problem.

### Nvidia products
- DGX-2 - AI System ("worlds most powerful"). Computer + AI frameworks
- Drive - System on a chip for Autonomous vehicles
- GeForce - Gaming GPUs - Note, these are incorporated into graphics cards.
- Virtual GPU - Share a remote GPU with laptop/desktop clients, i.e., the GPU is running in the cloud, the processing takes place there and the data is sent back to the client. Not quite sure who owns/runs the hardware.
- Jetson - “Credit card sized supercomputers” - Embedded AI computing. So if you want onboard AI (e.g.: train in AWS, transfer for inference on mobile robots/machines) [$580USD]
- Quadro - Pro-version GeForce [more precise, ‘better’] cards for use in high end visualisation (e.g.: Weta, Oil and Gas etc). I believe Nvidia manufacturer these cards, rather than just the chips. They’re heaps more expensive than the equivalent GeForce.
- Shield TV - 4K HDR STREAMING MEDIA PLAYER - GD: Does anyone use this? Seems pretty random. Seems to have access to GeForce Now which suggests that games are rendered in Nvidia cloud and streamed to the Shield? - yep, but still very much in beta - not sure how this would deal with latency.
- Tesla - Tesla is the AI focused card which implements the Volta-spec (as opposed to Pascal-spec etc). Tesla is designed to be deployed into data centres. This is the big growth area for Nvidia. 
- Tegra - Their mobile 'System on a chip'. Used in the Nintendo switch, and I think the MSFT Surface 2, as well as Drive. From the Q4 2018 CFO summary, "Tegra Processor business revenue includes SOC modules for the Nintendo Switch gaming console and development services. Also included is automotive revenue of $132 million...incorporating infotainment modules, production DRIVE PX platforms, and development agreements for self-driving cars."


# Segments
In their 2018 investor presentation, Nvidia break out their big segments:

1. Gaming [GeForce]
2. Pro-visualisation [Quadro]
3. Datacenter [Tesla]
4. Autonomous vehicles


## Datacenter 

Revenue growth: FY2016-17 = _145%_
Revenue growth: FY2017-18 = _133%_

Nvida estimate a TAM of $50b, while AMDs estimate is $21b.  

Three major areas of datacenter growth:

1. High Performance Computing **TAM: $10b**
2. Hyperscale and consumer internet (recommendation engine, credit scoring, fraud detection, ad insertion, ai assistant) **TAM: $20b**
3. Cloud computing and industries (startups, healthcare, transport, manufacturing, public sector, oil and gas, + 50% ‘future industries’) **TAM: $10b**

I believe this is where most of Nvidias immediate potential lies. The new Titan cards with included Tensor cores indicate the flexibility of Nvidias chip making capability, which will allow them to compete sucessfully in this area.

This (I believe) will be the immediate number to watch. The other segments I believe will either hold steady or slow growth in the short term.

**GCon:4/5**

## Automotive
Revenue growth: FY2017-18 = _15%_

>AV is a $60b opportunity by 2035.

Using the same architecture [Xavier] for L2 [human backup] -> L5[robo-taxi]. Xavier replaces four separate computers.
Note that the edge processing (Xavier) is for data gathering, pre-processing and inference. The training takes place on other systems in big datacenters. Nvidia could have a pretty compelling case to be the 'supercomputer-in-the-car' while training takes place on other systems.

Drive Sim and Constellation: Simulate real world driving conditions to train AI systems. 370+ partners developing on Drive Sim.

Definitely a case of providing shovels to gold prospectors. Nvidia is developing the tools to let AV contenders play in the space without developing their own chips. Even as a proof-of-concept tool, I imagine the commercial case is pretty compelling. It's only large very well resourced players (eg: Google) who use their own chips/software.

    Q: Google/Waymo seems to be the runaway leader in Automotive/Autonomous vehicles. Is the a winner-take-all situation?/
    A: Unclear to me. I can imagine a future where Waymo starts selling their tech to automotive companies, which would be a disaster for Nvidia’s (and others) programs. However, Waymo has no real partners in the automotive industry to date. Although conceptually it makes sense, those companies may (rightly!) be worried about ceding control of the experience to Google/Waymo, essentially giving up a huge chunk of independence to a brutal competitor.

This market should be watched carefully. I'm guessing it will gradually increase in revenue for Nvidia but I'm uncertain whether they will end up powering the majority of autonomous vehicles (however, if not them, then who?). However, they're definitely one of the primary horses in the race, the other being Google. 

**Red flag** - If Google start making significant deals with automotive companies.


## Gaming and Crypto
Revenue growth: FY2017-18 = _21%_

World-wide gaming revenue around 100b (growth of 3x since 2007)
Increasing cinematics -> increasing demand for new chips.

ESports
PC/Console/Mobile
VR is another potential driver. Unknown in contribution and timeframe.


### Competition
Seems that AMD is the only real graphics card competition in the gaming space with their Radeon cards. Sounds like NVDA has the edge, but AMD seems to be fairly equivalent. Of course, other chip manufacturers like Intel produce GPU capability but in terms of gaming, only AMD are true competition. Both the XBox 1 and PS4 are powered by AMD GPUs, but margins are reportedly low.


I'm not sure that gaming is a big growth driver for Nvidia. They're pretty positive about it in the investor presentation, but other resources suggest that the market is growing, but not super-rapidly. 

[6% CAGR suggested here](https://newzoo.com/insights/articles/the-global-games-market-will-reach-108-9-billion-in-2017-with-mobile-taking-42/)

My concern is that Gaming GPUs will hit a ... good enough level, and the market will be a market of diminishing returns, less people willing to spend for GPUs, pushing prices of GPUs down.

#### Edit 18/4/2018

Domeyrock (MFSA) pointed out that I didnt mention the Nintendo Switch. Correcting that here. Here's the revenue data from the Tegra business line, which they state "Tegra Processor business revenue includes SOC modules for the Nintendo Switch gaming console and development services". $132m of the Q4 number was Automotive. 

    | Q418 | Q318 | Q218 | 
----|----|----|----|----
Tegra Processor Business | 450 | 419 | 257

The Switch is selling really well, and I think we could safely assume that the majority of the jump in revenue is because of the Switch, so about $160m per quarter. So lets say, $600m for a calendar year (to about March 2018), over which Nintendo estimate sales of 14 million Switches. 

Estimated revenue per Tegra X1 = $45. 

[I could have saved some estimates!](https://www.fool.com/amp/investing/2016/09/26/will-the-nintendo-nx-be-a-major-windfall-for-nvidi.aspx)

The Switch has sold about 15 million units according to [this](https://en.wikipedia.org/wiki/List_of_best-selling_game_consoles). But according to that same list, it could sell... maybe 80-100 million (as per Nintendo DS and PSP numbers). 

Switches sold   |Revenue | Total gross profit (35% margin)
----|----- | ----
80m | $3.6b| $1.2b
100m | $4.5b| $1.6b

Good call by Domeyrock. From the 6% CAGR link about, it suggests that mobile gaming is growing at around 19% which is the market the Switch is playing in. What should this information do to Nvidias growth rate?

### Crypto

    Q: How much of the demand is because of cryptocurrency mining?
    A: [Chinese Crypto Mining Company Poses a Threat to AMD and Nvidia - Bloomberg](https://www.bloomberg.com/news/articles/2018-04-04/chinese-crypto-mining-hardware-putting-amd-nvidia-under-threat) - “5% of current revenue”
    A: [Cryptocurrency Mining Sales Cool in Q3, Says Nvidia - CoinDesk](https://www.coindesk.com/cryptocurrency-mining-chip-sales-cool-q3-says-nvidia/) 70m down from $150m in Q2

Not clear impact of Crypto. AMD CEO Lisa Su - (AMD: Cryptocurrency Mining Isn’t ‘A Long-Term Growth Driver’ - CoinDesk)[https://www.coindesk.com/amd-cryptocurrency-mining-isnt-a-long-term-growth-driver/]

But Huang bullish on Crypto.


#### ASICS
>“GPUs are used to mine cryptocurrencies like Ethereum and Litecoin that use the "scrypt" hashing algorithm. Bitcoin, by contrast, is chiefly mined today using dedicated hardware called ASICs.”

ASICs as mentioned previously are custom chips for a single function. These chips are by definition more efficient than more general purpose chips like GPUs. Bitmain is a Chinese producer of ASICs for bitcoin mining (and other currencies based on SHA256 hash algorithms).

[Asic Bitcoin Mining Hardware From Bitmain](http://bitmain.com)

>GPUs are used to mine cryptocurrencies like ethereum and litecoin that use the "scrypt" hashing algorithm. Bitcoin, by contrast, is chiefly mined today using dedicated hardware called ASICs.
>GD: I assume 'scrypt' algorithms can also be hashed using ASICs. 
 
Update: Bitmain are now producing ASICs for other currencies (including Ethereum). The problem with ASICs is that they're expensive, which means only relatively wealthy miners can utilise them. Because they're so powerful in terms of hashing, other methods of hashing become less useful, which means that the crypto-currency becomes centralised in the hands of the ASIC owners.

Not a great outcome when the point of crypto-currencies is decentralisation.

[The Anti-ASIC Revolt](https://www.coindesk.com/anti-asic-revolt-just-far-will-cryptos-hardware-war-go/)

> GD: I'm not convinced that crypto currencies will be a big growth driver over the longer term for NVidia. The future of crypto is pretty murky to me, and not clear how they will be 'mined' in the future.


## AI

AI (I think) is the overarching theme driving Nvidia's success although not specifically a 'segment' identified by Nvidia. AI is in a peak now, due to the stunning successes that have been demonstrated over the last few years, and the continued improvement in those algorithms. There doesn't appear to be any significant roadblocks standing in the way of more and more artificial intelligence in the world.

More and more data, more and more sensors, more and more processing required, more and more intelligence. Cars (as a very simple example), will be more and more autonomous which means some significant processing is required to prepare data for inference (Nvidias drive program). Nvidia metropolis offers the same attractiveness for 'smart cities' (no idea what the market is for that, but definitely in the same trend space).

Although the Internet of Things has been a buzzword for a while, the reality is there are more and more devices that are connected, and sending information to be recorded, and hopefully processed. All this results in a massive demand for efficient computation.

Linear models can be represented by matrix multiplies. For example, if you're training a classifier on images, you're going to be doing a lot of 'big matrix multiplies' because of the number of pixels in the image. Each of the nodes in the classifier is going to be receiving a lot of inputs from other nodes.

“Big matrix multiplies are exactly what GPUs were designed for”.


### OpenCL versus CUDA

OpenCL and CUDA do the same thing. They interface higher level languages to GPU-specific instructions. CUDA is Nvidias interface, while OpenCL is the open-source 'standard' supported by AMD amongst others.

The high-level frameworks that researchers use, TensorFlow, Torch, Theanos etc., do not really care whether its CUDA or OpenCL under the covers. However, most of the popular deep learning frameworks do not currently support OpenCL 
[Deep learning software comparison](https://en.wikipedia.org/wiki/Comparison_of_deep_learning_software). In the big ones, it appears to be under development  [Theano looks like it works, Torch has 3rd party implementations]. 

OpenCL is definitely a contender to CUDA. The open-source nature may also be attractive IFF performance can approach CUDA.

Nvidia has allocated significant resources to making the CUDA framework (the framework that talks to Nvidias GPUs for parallel processing) very accessible to AI researchers. It's also very performant.

Does it matter? Nvidia chips work fine with OpenCL. Other chips (eg: AMD) don't work with CUDA. Ultimately, the speed of processing will matter. Nvidia/CUDA is definitely the default at the moment, but I'm not sure there is a long-term moat for CUDA. Coders will deal with either, and supporting both CUDA and OpenCL will probably not be super difficult, since they do the same thing. 

### Competition
1. Google (TPU)
2. FPGA (eg: Intel and Microsoft)
3. China (and Russia?) 

####Google Tensor Processing Unit (TPU) 

The TPU is a custom designed chip from Google that is intended to make Deep Learning (very large neural networks) more efficient than standard GPUs. Google has recently revealed the 2nd generation chip (which suggests than there will be more generations to come). The original TPU was best for inference (ie, using a trained model), and required GPUs to train the model. TPU2 allows efficient training as well. 

Nvidia is including Tensor Cores in its new Titan chips, so the performance comparison is unclear. However, it is highly likely that an ASIC (TPU) will perform better on those specific functions.

Some benchmarks:
https://blog.riseml.com/benchmarking-googles-new-tpuv2-121c03b71384

> GD: Interesting benchmarks. I would have assumed that the TPU would have seriously (an order of magnitude) out-performed the GPU. In a cost basis, it is about half in the benchmark report, which is significant, but not as significant as I expected.

---

[Update: 2nd May]

I've learned a bunch more about deep learning and GPUs and TPUs. 

What GPUs do really well is matrix multiplication in floating point. The only interesting point here about floating point numbers is that they require much more memory than integers.

Deep learning (the current 'best' way to do machine learning) is based on matrix multiplications. You get your input matrix coming in, and multiply them by a a matrix of weights representing the strength of each input, with some non-linear activation functions being invoked on the result.

The point is, deep learning networks are large, and pretty much composed of floating-point matrix multiplications.

TPUs however, use quantization to turn floating-point numbers into integers, meaning the TPU has to deal with much smaller memory footprints. A floating-point number may normally require 32-bits (1s and 0s) to give sufficient precision, whereas with a bit of mapping, you could use a 8-bit integer (0-255) to represent the same value, if you don't care about the extra detail.

It's also based on a CISC approach (Complex Instruction Set Computer), which optimises for a limited set of complex operations (matrix multiplication), rather than using simple building blocks to create the complex operations (RISC approach - reduced instruction set computer).

In summary, TPUs are very simple compared to GPUs. There appears to be no reason Nvidia couldnt produce TPUs if they wanted to, and indeed have added them to their Titan chips. However, that suggests they would be a commodity rather than a significant value-added product.

This blog entry by Google talking about the first TPU is really interesting:
https://cloud.google.com/blog/big-data/2017/05/an-in-depth-look-at-googles-first-tensor-processing-unit-tpu

---

####FPGAs 
Field programmable gate arrays are chips that are configurable at a hardware level after production. An ASIC (eg: TPU) on the other hand is fixed after production.

> ...beginning in early 2017, GPUs have begun to face some competition from Field Programmable Gate Arrays (FPGAs). FPGAs can also accelerate Machine Learning and Artificial Intelligence workloads. [https://en.wikipedia.org/wiki/Graphics_processing_unit]
  
>  what if new AI computing models do not conform to the orderly mold of array-based, data-parallel algorithms that GPUs are so good at processing?
http://eecatalog.com/fpga/2017/10/24/artificial-intelligence-where-fpgas-surpass-gpus/



####China (and Russia?)
Its a bit vague, but the Chinese government has been very clear about its emphasis on AI. It seems highly unlikely that they will be content to be dependent on Western technology in the AI race. Russia has made similar noises.

https://www.technologyreview.com/s/609954/china-wants-to-make-the-chips-that-will-add-ai-to-any-gadget
>The chip is just one example of an important trend sweeping China’s tech sector. The country’s semiconductor industry sees a unique opportunity to establish itself amid the current wave of enthusiasm for hardware optimized for AI.


I believe for the foreseeable future, Nvidia has a strong place in any AI pipeline. Anyone who doesnt have access to custom chips will be dealing with either CUDA/OpenCL through the high-level AI frameworks.


## Numbers

### Basic data (TMF1000)

* Revenue was 3.207b up (10.2%) from 2.911b from the previous quarter (1.937b same quarter last year)
* TTM Revenue was 10.984b up (45.6%) from 7.542b 
* TTM Revenue per share (diluted) was 17.46 up (51.8%) from 11.50
* EPS diluted (prev quarter): was 1.98 up (11.9%) from 1.77
* Earnings (same quarter prev year): was 1.98 up (150.6%) from 0.79
* TTM eps was 6.00 up (99.3%) from 3.01
* Diluted share count was 627.00m down (2.2%) from 641.00m
* Cash and short-term investments  was 7.300b up (2.7%) from 7.108b (prev quarter)
* Debt (prev quarter) was 2.000b down (0.0%) from 2.000b (prev quarter)
* Cash flow for quarter was 1.327b down (41.6%) from 2.271b
* Cash flow for TTM was 4.010b up (173.3%) from 1.467b
* Cash flow per share for TTM was $6.40
* Gross margins was 0.65 up (4.2%) from 0.62
* CapExp was 118.00m down (71.5%) from 414.00m

### Last reported quarter ranges min, max [last]

* Trading range between Oct 01, 2017 - Dec 31, 2017 was 178.6542 to 250.3252 [231.4469]
* Market cap between Oct 01, 2017 - Dec 31, 2017 was 108.264b to 151.447b [140.025b]
* PE range (Oct 01, 2017 - Dec 31, 2017) was 28.45 to 39.86 [36.85]
* PS ratio range (Oct 01, 2017 - Dec 31, 2017) was 10.20 to 14.29 [13.21]
* Free cash flow (TTM) yield range (Oct 01, 2017 - Dec 31, 2017) was 2.65 to 3.70 [2.86]
* EV/Sales between Oct 01, 2017 - Dec 31, 2017 was 9.67 to 13.90 [12.86]

### Most recent quarter ranges min, max [last]
(uses more recent price data with last reported results)

* Trading range between Apr 01, 2018 - Jun 30, 2018 was 214.1176 to 266.91 [236.9]
* Market cap between Apr 01, 2018 - Jun 30, 2018 was 134.252b to 167.353b [143.325b]
* PE range (Apr 01, 2018 - Jun 30, 2018) was 34.10 to 42.50 [37.72]
* PS ratio range (Apr 01, 2018 - Jun 30, 2018) was 12.22 to 15.24 [13.52]
* Free cash flow (TTM) yield range (Apr 01, 2018 - Jun 30, 2018) was 2.40 to 2.99 [2.80]
* EV/Sales between Apr 01, 2018 - Jun 30, 2018 was 11.74 to 14.75 [13.04]

### Revenue

| Quarter   | Revenue   | TTM     | 𝝳 (q-1)   | 𝝳 (YoY)   |
|:----------|:----------|:--------|:----------|:----------|
| 2013Q1    | 954.74m   |         |           |           |
| 2013Q2    | 977.24m   |         | 2%        |           |
| 2013Q3    | 1.054b    |         | 8%        |           |
| 2013Q4    | 1.144b    | 4.130b  | 9%        |           |
| 2014Q1    | 1.103b    | 4.278b  | -4%       | 16%       |
| 2014Q2    | 1.103b    | 4.404b  | 0%        | 13%       |
| 2014Q3    | 1.225b    | 4.575b  | 11%       | 16%       |
| 2014Q4    | 1.251b    | 4.682b  | 2%        | 9%        |
| 2015Q1    | 1.151b    | 4.730b  | -8%       | 4%        |
| 2015Q2    | 1.153b    | 4.780b  | 0%        | 5%        |
| 2015Q3    | 1.305b    | 4.860b  | 13%       | 7%        |
| 2015Q4    | 1.401b    | 5.010b  | 7%        | 12%       |
| 2016Q1    | 1.305b    | 5.164b  | -7%       | 13%       |
| 2016Q2    | 1.428b    | 5.439b  | 9%        | 24%       |
| 2016Q3    | 2.004b    | 6.138b  | 40%       | 54%       |
| 2016Q4    | 2.173b    | 6.910b  | 8%        | 55%       |
| 2017Q1    | 1.937b    | 7.542b  | -11%      | 48%       |
| 2017Q2    | 2.230b    | 8.344b  | 15%       | 56%       |
| 2017Q3    | 2.636b    | 8.976b  | 18%       | 32%       |
| 2017Q4    | 2.911b    | 9.714b  | 10%       | 34%       |
| 2018Q1    | 3.207b    | 10.984b | 10%       | 66%       |

### Deferred revenue

| Quarter   |   Def.Revenue | 𝝳 (q-1)   | 𝝳 (YoY)   | Billings(Rev + 𝝳 def. rev)   |
|:----------|--------------:|:----------|:----------|:-----------------------------|
| 2013Q1    |             0 |           |           |                              |
| 2013Q2    |             0 |           |           | 977.24m                      |
| 2013Q3    |             0 |           |           | 1.054b                       |
| 2013Q4    |             0 |           |           | 1.144b                       |
| 2014Q1    |             0 |           |           | 1.103b                       |
| 2014Q2    |             0 |           |           | 1.103b                       |
| 2014Q3    |             0 |           |           | 1.225b                       |
| 2014Q4    |             0 |           |           | 1.251b                       |
| 2015Q1    |             0 |           |           | 1.151b                       |
| 2015Q2    |             0 |           |           | 1.153b                       |
| 2015Q3    |             0 |           |           | 1.305b                       |
| 2015Q4    |             0 |           |           | 1.401b                       |
| 2016Q1    |             0 |           |           | 1.305b                       |
| 2016Q2    |             0 |           |           | 1.428b                       |
| 2016Q3    |             0 |           |           | 2.004b                       |
| 2016Q4    |             0 |           |           | 2.173b                       |
| 2017Q1    |             0 |           |           | 1.937b                       |
| 2017Q2    |             0 |           |           | 2.230b                       |
| 2017Q3    |             0 |           |           | 2.636b                       |
| 2017Q4    |             0 |           |           | 2.911b                       |
| 2018Q1    |             0 |           |           | 3.207b                       |

### Margins

|    | Quarter   | Gross margin   | ebitdamargin   | netmargin   |
|---:|:----------|:---------------|:---------------|:------------|
|  0 | 2016Q2    | 58%            | 26%            | 18%         |
|  1 | 2016Q3    | 59%            | 34%            | 27%         |
|  2 | 2016Q4    | 60%            | 36%            | 30%         |
|  3 | 2017Q1    | 59%            | 31%            | 26%         |
|  4 | 2017Q2    | 58%            | 34%            | 26%         |
|  5 | 2017Q3    | 60%            | 36%            | 32%         |
|  6 | 2017Q4    | 62%            | 39%            | 38%         |
|  7 | 2018Q1    | 64%            | 43%            | 39%         |

### Free cash flow

| Quarter   | FCF     |
|:----------|:--------|
| 2016Q2    | 174.00m |
| 2016Q3    | 394.00m |
| 2016Q4    | 671.00m |
| 2017Q1    | 228.00m |
| 2017Q2    | 651.00m |
| 2017Q3    | 1.088b  |
| 2017Q4    | 944.00m |
| 2018Q1    | 1.327b  |

### Capital structure

|        | cash    | Investments   | Cash and investments   | Working Capital   | Debt   |   Debt to Equity | Interest   |
|:-------|:--------|:--------------|:-----------------------|:------------------|:-------|-----------------:|:-----------|
| 2016Q2 | 426.00m | 4.453b        | 4.879b                 | 3.749b            | 1.508b |             0.34 | 12.00m     |
| 2016Q3 | 1.940b  | 4.731b        | 6.671b                 | 6.266b            | 3.045b |             0.57 | 16.00m     |
| 2016Q4 | 1.766b  | 5.032b        | 6.798b                 | 6.748b            | 2.810b |             0.49 | 19.00m     |
| 2017Q1 | 1.989b  | 4.217b        | 6.206b                 | 7.133b            | 2.210b |             0.36 | 16.00m     |
| 2017Q2 | 1.988b  | 3.889b        | 5.877b                 | 7.038b            | 2.073b |             0.35 | 15.00m     |
| 2017Q3 | 2.802b  | 3.518b        | 6.320b                 | 7.452b            | 2.010b |             0.32 | 15.00m     |
| 2017Q4 | 4.002b  | 3.106b        | 7.108b                 | 8.102b            | 2.000b |             0.27 | 15.00m     |
| 2018Q1 | 765.00m | 6.535b        | 7.300b                 | 8.342b            | 2.000b |             0.26 | 15.00m     |

### Expenses

| Quarter   | R and D   | rnd    | Change (q-1)   | Change (YoY)   | Sales, General, Admin   | Change (q-1)   | Change (YoY)   |
|:----------|:----------|:-------|:---------------|:---------------|:------------------------|:---------------|:---------------|
| 2016Q2    | 350.00m   |        |                |                | 157.00m                 |                |                |
| 2016Q3    | 373.00m   |        | 7%             |                | 171.00m                 | 9%             |                |
| 2016Q4    | 394.00m   |        | 6%             |                | 176.00m                 | 3%             |                |
| 2017Q1    | 411.00m   | 1.528b | 4%             |                | 185.00m                 | 5%             |                |
| 2017Q2    | 416.00m   | 1.594b | 1%             | 19%            | 198.00m                 | 7%             | 26%            |
| 2017Q3    | 462.00m   | 1.683b | 11%            | 24%            | 212.00m                 | 7%             | 24%            |
| 2017Q4    | 507.00m   | 1.796b | 10%            | 29%            | 221.00m                 | 4%             | 26%            |
| 2018Q1    | 542.00m   | 1.927b | 7%             | 32%            | 231.00m                 | 5%             | 25%            |
### DCF
Using a compounded revenue growth rate of 25% over the next 5 years and an EBIT margin of 37% (as per current year) and a WACC of 9.6% gives an estimated share value of _$202_.

Over the ten year period, revenue will grow to around $50b, around about the current revenues of Disney (2017 - $55b), Cisco ($49b), and Intel ($59b).

Any decrease in revenue growth or margins (all things equal) will decrease this share price.

#### DCF examples

---------|5 year compounded revenue growth rate | 20% | 25% | 30% | 40%
---------|--------------------------------------|-----|-----|-----|-----
Operating margin|Implied 10 year revenue.              |$38b |$57b |$75b |$129b
20% |                                  | $93 |$118 |$149 |**$237**
30% |                                  | $140|$179 |**$228** |$367
40% |                                 | $194|**$248** |$318 |$516

#### Comparisons
Revenues (2017) for comparison include Amazon ($135b), Microsoft ($85b), Alphabet ($90b), Cisco ($49b), Oracle ($37b).

Company      | Rev (TTM)| Rev Growth% | OpMargin% | NP %
-------------|----------|-------------|-----------|-----
Nvidia       |  193b    |36%          |2.6%       |1.6%
Amazon       |  193b    |36%          |2.6%       |1.6% 
Microsoft    |  104b    |13%          |28.9%      |27%
Alphabet     |  111b    |23%          |24%        |20%

#### Other numbers
Metric                 | Value     | Comments
-----------------------|---------- | -------
PEG                    | .6
P/E (MRY)              | 49 
Gross Margin (TTM)     |60%
Operating Margin (TTM) |33%
Net profit Margin (TTM)|30%
EV/FCF                 | 27 (17.36b/632m) |
[Zacks Rank](https://www.zacks.com/stock/research/NVDA/stock-style-scores)            | 3 |
Morningstar fair value | $120 [17Apr18] |


### +'s and -'s [Big trends]
1. \+ AI.
2. \+ Autonomous vehicles.
3. \+ Gaming.
Anything else?

This list I believe is the key to Nvidia's recent success. They're playing in markets that are having big tides lifting their boat. However, there is still considerable uncertainty about how each of these tides will play out.

Ultimately the question might be as simple as: How important will floating point matrix multiplication be in the AI space?

If you can say, floating-point is a must! Then Nvidia is likely to continue to do well. 

Gaming is probably the easiest to guesstimate. It will increase in a somewhat linear fashion

## (IMHO) beliefs required to own the stock
1. Demand for high-end GPUs is outstripping demand because of deep learning/crypto.
2. Automotive will actually become a thing. Nvidia will have a platform that will have considerable competitive advantages.
3. Deep learning will stay (mostly) being developed on GPUs [Is there any reason to doubt this? GPUs do deep learning well, and the maths of deep learning will not change in the short-term.]
4. Gaming will stay relatively stable.



Final thoughts: Playing with models, its pretty hard to imagine that Nvidia is cheap. 

My uncertainty rating is: high

## Definitions
- ASIC - Application specific integrated circuit - specific chips used to mine bitcoin.
- CUDA - CUDA is the leading proprietary (Nvidia) GPGPU framework [See OpenCL]
- CUDA core - processes floating point operations (multiply-accumulate) [Programming Tensor Cores in CUDA 9 | NVIDIA Developer Blog](https://devblogs.nvidia.com/programming-tensor-cores-cuda-9/)
- Chip Yield - The number of chips successfully created from a silicon wafer. Manufacturing defects cause chip failures. The larger the chip [die size], the more failures can be expected, leading to higher prices for larger chips.
- Die size - the size of the chunk on a silicon wafer that corresponds to one chip.
- Drive - Nvidias autonomous vehicle programe. Creating an ecosystem around cars. System on a card for Autonomous vehicles.
- FPGA - Field-programmable gate array. Chips that can be reconfigured 'in the field' for particular purposes. Both MSFT and INTC are betting on this approach for AI, so direct competition to general GPUs and specific chips (eg: TensorFlow)
- GPGPU - GPGPU allows information to be transferred in both directions, from CPU to GPU and GPU to CPU. Such bidirectional processing can hugely improve efficiency in a wide variety of tasks related to images and video
- OpenCL - OpenCL is currently the leading open source GPGPU framework [see CUDA]
- Pegasus - A codename for a processor/card in the NVidia Drive project. The successor to the Drive PX 2.
- SM - streaming multiprocessor - more SMs allows more parallel processors. SMs consist of multiple stream processors, which deal with one thread at a time.
- Tensor core - A processor that deals with floating point operations on 4x4 matrices. 

### Architectures
- Maxwell - GPU architecture specification [Gen latest-2]
- Pascal - GPU architecture specification [Gen latest- 1]
- Volta - GPU architecture specification [Gen latest]
- Tesla - An implementation of Volta
- Titan V - A consumer level implementation of Volta.
- Titan Xp - A consumer level implementation of Pascal [predecessor of Titan V]
- Xavier - Implementation of the Volta architecture for automobiles. "Xavier is the most complex system on a chip ever created".



### Rambling notes

“It should be noted that Nvidia cards actually support OpenCL as well as CUDA, they just aren’t quite as efficient as AMD GPUs when it comes to OpenCL computation. This is changing though as the recently released Nvidia GTX 980 is a very capable OpenCL card as well as a CUDA monster. We can only see Nvidia’s OpenCL performance getting better and better in the future, and this is definitely something worth considering.”

The only situation in which we would recommend an AMD GPU to professionals is when they are exclusively using apps that support OpenCL and have no CUDA option.

>GD: If AMD put Nvidia-level support behind OpenCL…? CUDA would no longer be the obvious choice. The longer AMD leave this, the more developers will be experienced with CUDA. Apps (e.g.: Adobe suite etc) talk to CUDA/OpenCL so developer experience counts.

There is also a crossover with gaming where the ubiquity of Nvidia cards means there is more incentive to go down a CUDA-route than the OpenCL route.
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTgyMjUzMzU4MCwtMjc2MzA4MjddfQ==
-->