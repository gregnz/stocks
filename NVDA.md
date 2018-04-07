# NVDA
GCon = 1 to 5 scale of ‘Gregs conviction’

## My understanding

Nvidia produces GPU chips, primarily used for gaming. GPUs are developed to be massively parallel floating point processors.

I guess that means linear algebra. But in any case, there are a bunch of new technologies that these chips naturally lend themselves to. Cryptocurrency mining, AI, etc. So a lot of big tides are lifting NVDAs boat.

This point about NVDAs optionality is probably the most interesting point. In my view, that optionality is driving a large amount of interest in the stock.

In their 2018 investor presentation, Nvidia break out the big trends as follows:

1. Gaming [GeForce]
2. Pro-visualisation [Quadro]
3. Datacenter [Tesla]
4. Autonomous vehicles

### Datacenter
Revenue growth: FY2016-17 = _145%_
Revenue growth: FY2017-18 = _133%_

50b TAM [HPC:10, Hyperscale and Consumer: 20, Cloud Computing and industries: 10]
AMD - $21b TAM

1. HPC
2. Hyperscale and consumer internet [recommendation engine, credit scoring, fraud detection, ad insertion, ai assistant
3. Cloud computing and industries [startups, healthcare, transport, manufacturing, public sector, oil and gas, + 50% ‘future industries’

> However, beginning in early 2017, GPUs have begun to face some competition from Field Programmable Gate Arrays (FPGAs). FPGAs can also accelerate Machine Learning and Artificial Intelligence workloads. [https://en.wikipedia.org/wiki/Graphics_processing_unit]


### Automotive [GDC: 2/5]
Revenue growth: FY2017-18 = _15%_ [GD: low]

>AV is a $60b opportunity by 2035.

Using the same architecture [xavier] for L2 [human backup] -> L5[robo-taxi]
Xavier replaces four separate computers.

Providing close to end-to-end systems, smaller, lower power consumption,  lower cost. Eg, one car per year produces 1+petabyte of data.

Drive Sim and Constellation: Simulate real world driving conditions to train AI systems. 370+ partners developing on Drive Sim.

    Q: Google/Waymo seems to be the runaway leader in AutomotiveAutonomous vehicles. Is the a winner-take-all situation?/
    A: Unclear to me. I can imagine a future where Waymo starts selling their tech to automotive companies, which would be a disaster for Nvidia’s (and others program). Does Waymo really want to be in the business of running fleets of cars? It seems unlikely.

However, if they do sell their technology to automotive companies, doesn’t that just make cars commodities? Arguably this is the case today. I guess they continue to distinguish on looks, internal components etc. So we can’t discount this scenario.


### Gaming
Revenue growth: FY2017-18 = _21%_
GeForce
World-wide gaming revenue around 100b (growth of 3x since 2007)
Increasing cinematics -> increasing demand for new chips.


####Crypto
    Q: How much of the demand is because of cryptocurrency mining?
    A: [Chinese Crypto Mining Company Poses a Threat to AMD and Nvidia - Bloomberg](https://www.bloomberg.com/news/articles/2018-04-04/chinese-crypto-mining-hardware-putting-amd-nvidia-under-threat) - “5% of current revenue”
    A: [Cryptocurrency Mining Sales Cool in Q3, Says Nvidia - CoinDesk](https://www.coindesk.com/cryptocurrency-mining-chip-sales-cool-q3-says-nvidia/) 70m down from $150m in Q2

Not clear impact of Crypto. AMD CEO Lisa Su - [AMD: Cryptocurrency Mining Isn’t ‘A Long-Term Growth Driver’ - CoinDesk](https://www.coindesk.com/amd-cryptocurrency-mining-isnt-a-long-term-growth-driver/)
But Huang bullish on Crypto.

>“GPUs are used to mine cryptocurrencies like Ethereum and Litecoin that use the "scrypt" hashing algorithm. Bitcoin, by contrast, is chiefly mined today using dedicated hardware called ASICs.”

#### Questions
    Q: Is there a point of ‘good-enough’ for video cards? What does that demand curve actually look like?
    A: Gaming is a growing industry. Faster frame rates and more pixels require new cards.

    Q: But what is the limit before people stop caring? Eg: 4K at 80fps? How far off that are we?
    A: Its not just resolution, its accuracy. For example, real-time ray-tracing in 4K at 80fps. I think we’re a way off that.

VR is another potential driver. Unknown in contribution.

## Competition
AMD, Google, Bitmain, FPGA (eg: Intel and Microsoft)

Seems that AMD is the only real graphics card competition with their Radeon cards. Sounds like NVDA has the edge, but AMD seems to be fairly equivalent.

XBox 1 powered by AMD

PS4 powered by AMD
> May not be significant because of low margins?


### AI
Note that most of the popular deep learning frameworks do not currently support OpenCL. [https://en.wikipedia.org/wiki/Comparison_of_deep_learning_software]

In the big ones, it appears to be under development  [Theano looks like it works, Torch has 3rd party implementations]. OpenCL appears a contender to CUDA. The open-source nature may also be attractive IFF performance can approach CUDA.

Other anecdotes suggest its cheaper to get going with AMD/OpenCL.

Google Tensor Processing Unit
China https://www.technologyreview.com/s/609954/china-wants-to-make-the-chips-that-will-add-ai-to-any-gadget

FPGAs 
>  what if new AI computing models do not conform to the orderly mold of array-based, data-parallel algorithms that GPUs are so good at processing?
http://eecatalog.com/fpga/2017/10/24/artificial-intelligence-where-fpgas-surpass-gpus/


### Crypto
[Asic Bitcoin Mining Hardware From Bitmain](http://bitmain.com)
GPUs are used to mine cryptocurrencies like ethereum and litecoin that use the "scrypt" hashing algorithm. Bitcoin, by contrast, is chiefly mined today using dedicated hardware called ASICs.

## Numbers
Revenue growth: FY2017-18 = _41%_

Q      | Q1 17|Q2 17|Q3 17 |Q4 17 |Q1 18|Q2 18|Q3 18|Q4 18
-------|----- |-----|------|------|-----|-----|-----|-----
Gaming       |  687  |  781  |  1244 |  1348  |  1027  |  1186  |  1561  |  1739
            |       |  14  |  59  |  8  |  24  |  15  |  32  |  11
Prof vis     |  189  |  214  |  207  |  225  |  205  |  235  |  239  |  254
            |       |  13%  |  -3%  |  9%  |  -9%  |  15%  |  2%  |  6%
Datacenter   |  143  |  151  |  240  |  296  |  409  |  416  |  501  |  606
            |       |  6%   |  59%  |  23%  |  38%  |  2%  |  20%  |  21%
Automotive   |  113  |  119  |  127  |  128  |  140  |  142  |  144  |  132
     |      |  5%   |  7%   |  1%   |  9%  |  1%  |  1%  |  -8%
OEM and IP   |  173  |  163  |  186  |  176  |  156  |  251  |  191  |  180
   |        |  -6%  |  14%  |  -5%  |  -11%  |  61%  |  -24%  |  -6%


             |FY2017.  |FY2018|% change
-------------|-------   |-----| ----
Gaming       |4060.    |5513  |**36%**
Prof vis     |835      |933   |**12%**
Datacenter.  |830      |1932  |**133%**
Automotive.  |487      |558   |**15%**
OEM and IP.  |698      |778   |**11%**
**Totals**.  |**6910** |**9716**|**41%**

> Thoughts about revenue numbers
Some big growth numbers, particularly in datacenter. The other components are solid. 
Automotive is a surprisingly large part of revenue, which I assume will continue as long as the market for autonomous vehicles is not 'solved' [See Waymo discussion below]

## Discussion
The demand for increased processing power is enormous. Will continue to grow. GPUs are taking up the slack that CPUs are dropping.

Crypto-currency? How much of a revenue generator? If crypto crashes, second hand video cards may tank brand new cards…? e.g., FY2019 might be way down.

Open-CL is a contender. However, Open-CL doesn’t matter much to Nvidia. Nvidia will probably choose to support OpenCL. Performance on the cards is what matters.

In any case, its a 2 horse race at this stage.

Pro visualisation doesn’t seem to be much of a growth area for them.

What would happen if they/CUDA does become the ‘only’ platform for AI? 
Q: How does it relate to Tensorflow?
A: CUDA is the API to Nvidia GPUs. Tensorflow is the high-level learning libraries. Tensorflow uses CUDA to run its instructions on the Nvidia GPUs. CUDA is sort of like assembly for Nvidia GPUs. OpenCL performs a similar function for AMD chips is a more standard library (i.e., you can use it to work on Nvidia chips as well). However, reports (my vague recollections) suggest that Nvidia put a lot of effort into making sure CUDA is optimised, much more than AMD does. Therefore… you’ll get more performance out of CUDA+Nvidia over OpenCL+AMD (or Nvidia). If performance is key, then CUDA+Nvidia is your only real option.




###Products
- DGX-1 - Computer + AI frameworks Nvidia Cloud 149,000
- Drive - System on a chip for Autonomous vehicles
- GeForce - Gaming GPUs - Note, these are incorporated into graphics cards.
- Virtual GPU - Share a remote GPU with laptop/desktop clients, i.e., the GPU is running in the cloud, the processing takes place there and the data is sent back to the client. Not quite sure who owns/runs the hardware.
- Jetson - “Credit card sized supercomputers” - Embedded AI computing. So if you want onboard AI (e.g.: train in AWS, transfer for inference on mobile robots/machines) [$580USD]
- Quadro - Pro-version GeForce [more precise, ‘better’] cards for use in high end visualisation (e.g.: Weta, Oil and Gas etc). I believe Nvidia manufacturer these cards, rather than just the chips. They’re heaps more expensive than the equivalent GeForce.
- Shield TV - 4K HDR STREAMING MEDIA PLAYER - GD: Does anyone use this? Seems pretty random. Seems to have access to GeForce Now which suggests that games are rendered in Nvidia cloud and streamed to the Shield? - yep, but still very much in beta - not sure how this would deal with latency.
- Tesla - Tesla is the AI focused card which implements the Volta-spec (as opposed to Pascal-spec etc). Tesla is designed to be deployed into data centres. This is the big growth area for Nvidia. I imagine this will be hard to keep up.


Business model canvas
1. Key Partners
2. Key activities
Production of  GPU chips.
4. Key resources
5. Value proposition
Best video cards for gaming.
GPU for AI
Cards for data visualisation
Cards for data centres

7. Customer relationships
8. Channels
9. Customer segments
10. Cost structure
11. Revenue streams

## Definitions
- ASIC - Application specific integrated circuit - specific chips used to mine bitcoin.
- CUDA - CUDA is the leading proprietary (Nvidia) GPGPU framework [See OpenCL]
- CUDA core - processes floating point operations (multiply-accumulate) [Programming Tensor Cores in CUDA 9 | NVIDIA Developer Blog](https://devblogs.nvidia.com/programming-tensor-cores-cuda-9/)
- Die size - the size of the chunk on a silicon wafer that corresponds to one chip.
- Chip Yield-
- FPGA - Field-programmable gate array. Chips that can be reconfigured 'in the field' for particular purposes. Both MSFT and INTC are betting on this approach for AI, so direct competition to general GPUs and specific chips (eg: TensorFlow)
- GPGPU - GPGPU allows information to be transferred in both directions, from CPU to GPU and GPU to CPU. Such bidirectional processing can hugely improve efficiency in a wide variety of tasks related to images and video
- OpenCL - OpenCL is currently the leading open source GPGPU framework [see CUDA]
- SM - streaming multiprocessor - more SMs allows more parallel processors. SMs consist of multiple stream processors, which deal with one thread at a time.
- Tensor core - A processor that deals with floating point operations on 4x4 matrices.

### Architectures
- Maxwell - GPU architecture specification [Gen latest-2]
- Pascal - GPU architecture specification [Gen latest- 1]
- Volta - GPU architecture specification [Gen latest]
- Tesla - An implementation of Volta
- Titan V - A consumer level implementation of Volta.
- Titan Xp - A consumer level implementation of Pascal [predecessor of Titan V]


“It should be noted that Nvidia cards actually support OpenCL as well as CUDA, they just aren’t quite as efficient as AMD GPUs when it comes to OpenCL computation. This is changing though as the recently released Nvidia GTX 980 is a very capable OpenCL card as well as a CUDA monster. We can only see Nvidia’s OpenCL performance getting better and better in the future, and this is definitely something worth considering.”

The only situation in which we would recommend an AMD GPU to professionals is when they are exclusively using apps that support OpenCL and have no CUDA option.

>GD: If AMD put Nvidia-level support behind OpenCL…? CUDA would no longer be the obvious choice. The longer AMD leave this, the more developers will be experienced with CUDA. Apps (e.g.: Adobe suite etc) talk to CUDA/OpenCL so developer experience counts.

There is also a crossover with gaming where the ubiquity of Nvidia cards means there is more incentive to go down a CUDA-route than the OpenCL route.