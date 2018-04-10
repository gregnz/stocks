# NVDA
GCon = 1 to 5 scale of ‘Gregs conviction’.  
Most buzzwords are in the 'Definitions' section.

## My understanding

Nvidia produces GPU (graphical processing unit) chips. GPUs are developed to be massively parallel floating point processors, which excel at rendering graphics for games.

Think of CPUs which are single-core, dual-core, quad-core, sometimes 8-16 cores. These are the parallel processing brains, so a quad-core CPU can process four concurrent tasks. CPUs are optimised for sequential serial processing.

GPUs on the other hand have thousands of less powerful cores, which means they can run thousands of simpler tasks concurrently. For example, the Geforce GTX 1080Ti has 3584 cores.

There are a bunch of technologies that benefit from massive parallel processing. Graphics, cryptocurrency mining, AI, etc. They all do (more or less) the same thing with slightly different data. These are the big tides lifting Nvidias boat.

The major point is that currently GPUs are the 'solution-du-jour' for ubiquitous parallel processing. There are other technologies that are better for some situations, but in general, GPUs are the best at solving the general problem.

### Stock advisor
Their latest recommendation (Jan 2017) was at a stock price of $101. A large part of the premise was the growth of automated vehicle revenue. [Latest recommmedation](https://www.fool.com/premium/stock-advisor/coverage/18/coverage/updates/2017/01/20/davids-pick-nvidia.aspx)

They mention "In fact, analysts are predicting 5.5 million semi- and fully autonomous cars shipped in 2020" which seems... optimistic to me?



### Nvidia products
- DGX-1 - Computer + AI frameworks Nvidia Cloud 149,000
- Drive - System on a chip for Autonomous vehicles
- GeForce - Gaming GPUs - Note, these are incorporated into graphics cards.
- Virtual GPU - Share a remote GPU with laptop/desktop clients, i.e., the GPU is running in the cloud, the processing takes place there and the data is sent back to the client. Not quite sure who owns/runs the hardware.
- Jetson - “Credit card sized supercomputers” - Embedded AI computing. So if you want onboard AI (e.g.: train in AWS, transfer for inference on mobile robots/machines) [$580USD]
- Quadro - Pro-version GeForce [more precise, ‘better’] cards for use in high end visualisation (e.g.: Weta, Oil and Gas etc). I believe Nvidia manufacturer these cards, rather than just the chips. They’re heaps more expensive than the equivalent GeForce.
- Shield TV - 4K HDR STREAMING MEDIA PLAYER - GD: Does anyone use this? Seems pretty random. Seems to have access to GeForce Now which suggests that games are rendered in Nvidia cloud and streamed to the Shield? - yep, but still very much in beta - not sure how this would deal with latency.
- Tesla - Tesla is the AI focused card which implements the Volta-spec (as opposed to Pascal-spec etc). Tesla is designed to be deployed into data centres. This is the big growth area for Nvidia. I imagine this will be hard to keep up.
- Tegra - Their mobile 'System on a chip'. Used in the Nintendo switch, and I think the MSFT Surface 2, as well as Drive. From the Q4 2018 CFO summary, "Tegra Processor business revenue includes SOC modules for the Nintendo Switch gaming console and development services. Also included is automotive revenue of $132 million...incorporating infotainment modules, production DRIVE PX platforms, and development agreements for self-driving cars."


# Segments
In their 2018 investor presentation, Nvidia break out the big segments:

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

## Automotive
Revenue growth: FY2017-18 = _15%_

>AV is a $60b opportunity by 2035.

Using the same architecture [Xavier] for L2 [human backup] -> L5[robo-taxi]. Xavier replaces four separate computers.
Note that the edge processing (Xavier) is for data gathering, pre-processing and inference. The training takes place on other systems in big datacenters. Nvidia could have a pretty compelling case to be the 'supercomputer-in-the-car' while training takes place on other systems.

Drive Sim and Constellation: Simulate real world driving conditions to train AI systems. 370+ partners developing on Drive Sim.

Definitely a case of providing shovels to gold prospectors. Nvidia is developing the tools to let AV contenders play in the space without developing their own chips. Even as a proof-of-concept tool, I imagine the commercial case is pretty compelling. It's only large very well resourced players (eg: Google) who use their own chips/software.

    Q: Google/Waymo seems to be the runaway leader in AutomotiveAutonomous vehicles. Is the a winner-take-all situation?/
    A: Unclear to me. I can imagine a future where Waymo starts selling their tech to automotive companies, which would be a disaster for Nvidia’s (and others) programs. However, Waymo has no real partners in the automotive industry to date. Although conceptually it makes sense, those companies may (rightly!) be worried about ceding control of the experience to Google/Waymo, essentially giving up a huge chunk of independence to a brutal competitor.

This market should be watched carefully. I'm guessing it will gradually increase in revenue for Nvidia but I'm uncertain whether they will end up powering the majority of autonomous vehicles (if not them, then who?). However, they're definitely one of the primary horses in the race, the other being Google. 

**Red flag** - If Google start making significant deals with automotive companies.


**GCon: 3/5**

## Gaming [3/5]
Revenue growth: FY2017-18 = _21%_
World-wide gaming revenue around 100b (growth of 3x since 2007)
Increasing cinematics -> increasing demand for new chips.
**MORE HERE**
VR is another potential driver. Unknown in contribution.

###Crypto

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


> GD: I'm not convinced that crypto currencies will be a big growth driver over the longer term for NVidia. The future of crypto is pretty murky to me.


### Questions
    Q: Is there a point of ‘good-enough’ for video cards? What does that demand curve actually look like?
    A: Gaming is a growing industry. Faster frame rates and more pixels require new cards.

    Q: But what is the limit before people stop caring? Eg: 4K at 80fps? How far off that are we?
    A: Its not just resolution, its accuracy. For example, real-time ray-tracing in 4K at 80fps. I think we’re a way off that.


### Competition
Seems that AMD is the only real graphics card competition in the gaming space with their Radeon cards. Sounds like NVDA has the edge, but AMD seems to be fairly equivalent. Of course, other chip manufacturers like Intel produce GPU capability but in terms of gaming, only AMD are true competition. Both the XBox 1 and PS4 are powered by AMD GPUs, but margins are reportedly low.


**GCon 3/5**


## AI

AI (I think) is the overarching theme driving Nvidia's success although not specifically a 'segment' identified by Nvidia. AI is in a peak now, due to the stunning sucesses that have been demonstrated over the last few years, and the continued improvement in those algorithms. There doesn't appear to be any significant roadblocks standing in the way of more and more artificial intelligence in the world.

More and more data, more and more sensors, more and more processing required, more and more intelligence. Cars (as a very simple example), will be more and more autonomous which means some significant processing is required to prepare data for inference (Nvidias drive program). Nvidia metropolis offers the same attractiveness for 'smart cities' (no idea what the market is for that, but definitely in the same trend space).

Although the Internet of Things has been a buzzword for a while, the reality is there are more and more devices that are connected, and sending information to be recorded, and hopefully processed. All this results in a massive demand for efficient computation.

### OpenCL versus CUDA
OpenCL and CUDA do the same thing. They interfance higher level languages to GPU-specific instructions. CUDA is Nvidias interface, while OpenCL is the open-source 'standard' supported by AMD amongst others.

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

>GD: I think it unlikely however that the scope of architecture thats useful in AI is actually known at this point. Deep learning is one facet of AI, and other upcoming fields may benefit from the more general capabilities of GPUs.

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

**GCon 5/5 **

## Numbers
Revenue growth: FY2017-18 = _41%_

Q      | Q1 17|Q2 17|Q3 17 |Q4 17 |Q1 18|Q2 18|Q3 18|Q4 18
-------|----- |-----|------|------|-----|-----|-----|-----
Gaming       |  687  |  781  |  1244 |  1348  |  1027  |  1186  |  1561  |  1739
\-       |  \-     |  14%  |  59%  |  8%      |  -24%    |  15%    |  32%    |  11%
Prof vis     |  189  |  214  |  207  |  225  |  205  |  235  |  239  |  254
\-     |    \-   |  13%  |  -3%  |  9%  |  -9%  |  15%  |  2%  |  6%
Datacenter   |  143  |  151  |  240  |  296  |  409  |  416  |  501  |  606
\-   |   \-    |  6%   |  59%  |  23%  |  38%  |  2%  |  20%  |  21%
Automotive   |  113  |  119  |  127  |  128  |  140  |  142  |  144  |  132
\-   |    \-  |  5%   |  7%   |  1%   |  9%  |  1%  |  1%  |  -8%
OEM and IP   |  173  |  163  |  186  |  176  |  156  |  251  |  191  |  180
\-   |   \-   |  -6%  |  14%  |  -5%  |  -11%  |  61%  |  -24%  |  -6%


             |FY2017.  |FY2018|% change
-------------|-------   |-----| ----
Gaming       |4060     |5513  |**36%**
Prof vis     |835      |933   |**12%**
Datacenter   |830      |1932  |**133%**
Automotive   |487      |558   |**15%**
OEM and IP   |698      |778   |**11%**
**Totals**   |**6910** |**9716**|**41%**


### DCF
Coming soon

### Reverse DCF
Coming soon

###Thoughts about revenue numbers
Coming soon

## Discussion
Coming soon




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
- 

### Architectures
- Maxwell - GPU architecture specification [Gen latest-2]
- Pascal - GPU architecture specification [Gen latest- 1]
- Volta - GPU architecture specification [Gen latest]
- Tesla - An implementation of Volta
- Titan V - A consumer level implementation of Volta.
- Titan Xp - A consumer level implementation of Pascal [predecessor of Titan V]
- Xavier - Implementation of the Volta architecture for automobiles. "Xavier is the most complex system on a chip ever created".


“It should be noted that Nvidia cards actually support OpenCL as well as CUDA, they just aren’t quite as efficient as AMD GPUs when it comes to OpenCL computation. This is changing though as the recently released Nvidia GTX 980 is a very capable OpenCL card as well as a CUDA monster. We can only see Nvidia’s OpenCL performance getting better and better in the future, and this is definitely something worth considering.”

The only situation in which we would recommend an AMD GPU to professionals is when they are exclusively using apps that support OpenCL and have no CUDA option.

>GD: If AMD put Nvidia-level support behind OpenCL…? CUDA would no longer be the obvious choice. The longer AMD leave this, the more developers will be experienced with CUDA. Apps (e.g.: Adobe suite etc) talk to CUDA/OpenCL so developer experience counts.

There is also a crossover with gaming where the ubiquity of Nvidia cards means there is more incentive to go down a CUDA-route than the OpenCL route.