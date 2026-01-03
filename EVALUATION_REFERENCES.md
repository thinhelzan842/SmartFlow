# 📚 SCIENTIFIC REFERENCES FOR SMARTFLOW EVALUATION FRAMEWORK

## 🎯 OVERVIEW

This document provides scientific justification for the **SmartFlow routing evaluation framework**. 

**IMPORTANT NOTE ON TRUTHFULNESS:**
- **What papers provide:** Measurement methodologies, conceptual frameworks, and standard practices
- **What we determined empirically:** Specific threshold values (0.3, 0.95, 1.0s, etc.) based on our 30 test cases
- **Our approach:** We use established metrics from the literature and set thresholds based on our system's performance data

The papers cited below justify **why we measure what we measure**, not necessarily the specific threshold values we chose.

---

## 1️⃣ **ROUTING QUALITY METRICS (Weight: 40%)**

### Why 40% Weight?
**Our Justification:** Routing quality is the core function of our system. We allocated the largest weight (40%) to the primary purpose of the application - finding good routes.

**Methodological Support:**
- **Delling, D., Sanders, P., Schultes, D., & Wagner, D. (2009).** "Engineering Route Planning Algorithms." *Algorithmics of Large and Complex Networks*, Springer LNCS 5515, pp. 117-139.
  - **Link:** https://link.springer.com/chapter/10.1007/978-3-642-02094-0_7
  - **Why cited:** Discusses evaluation of route planning algorithms including route quality metrics

---

### Metric 1.1: Route Diversity (Jaccard Similarity)

**Formula:** `Jaccard = |A ∩ B| / |A ∪ B|`

**Our Threshold:** ≤ 0.3 (determined empirically from our test results - lower values mean more diverse alternative routes)

**Methodological References:**
- **Bader, R., Dees, J., Geisberger, R., & Sanders, P. (2011).** "Alternative Route Graphs in Road Networks." *Lecture Notes in Computer Science*, Springer, vol. 6942, pp. 21-32.
  - **DOI:** https://doi.org/10.1007/978-3-642-24091-5_2
  - **Link:** https://link.springer.com/chapter/10.1007/978-3-642-24091-5_2
  - **Why cited:** Introduces using Jaccard index to measure similarity between alternative routes in road networks

- **Abraham, I., Delling, D., Goldberg, A. V., & Werneck, R. F. (2011).** "Alternative Routes in Road Networks." *Experimental Algorithms: 10th International Symposium*, Springer, pp. 23-34.
  - **DOI:** https://doi.org/10.1007/978-3-642-20662-7_3
  - **Link:** https://link.springer.com/chapter/10.1007/978-3-642-20662-7_3
  - **Why cited:** Discusses algorithms for computing alternative routes with diversity constraints

- **Luxen, D., & Vetter, C. (2011).** "Real-time Routing with OpenStreetMap Data." *SIGSPATIAL GIS '11*, ACM, pp. 513-516.
  - **Link:** https://dl.acm.org/doi/10.1145/2093973.2094062
  - **Why cited:** Demonstrates practical application of route quality metrics in OSM-based routing systems

---

### Metric 1.2: Route Efficiency (Distance Ratio)

**Formula:** `Efficiency = Actual Distance / Straight-line Distance`

**Our Threshold:** ≥ 0.95 (determined empirically - routes should be reasonably direct)

**Methodological References:**
- **Geisberger, R., Sanders, P., Schultes, D., & Vetter, C. (2012).** "Exact Routing in Large Road Networks Using Contraction Hierarchies." *Transportation Science*, 46(3), pp. 388-404.
  - **Link:** https://pubsonline.informs.org/doi/10.1287/trsc.1110.0401
  - **Why cited:** Discusses route quality evaluation including path stretch factor (efficiency ratio) as a metric for assessing route directness

- **Ziebart, B. D., Maas, A. L., Dey, A. K., & Bagnell, J. A. (2008).** "Navigate like a cabbie: Probabilistic reasoning from observed context-aware behavior." *UbiComp '08*, ACM, pp. 322-331.
  - **Link:** https://dl.acm.org/doi/10.1145/1409635.1409678
  - **Why cited:** Studies route efficiency patterns in real-world taxi navigation data using GPS traces

---

### Metric 1.3: Congestion Avoidance

**Formula:** `Avoidance = 1 - (Route Congestion / Avg Network Congestion)`

**Our Threshold:** ≥ 0.85 (determined empirically - routes should avoid congestion better than network average)

**Methodological References:**
- **Yuan, J., Zheng, Y., Zhang, C., Xie, W., Xie, X., Sun, G., & Huang, Y. (2010).** "T-Drive: Driving Directions Based on Taxi Trajectories." *SIGSPATIAL GIS '10*, ACM, pp. 99-108.
  - **Link:** https://dl.acm.org/doi/10.1145/1869790.1869807
  - **Why cited:** Uses real taxi GPS data to analyze routing behavior and congestion avoidance patterns

- **Wang, D., Pedreschi, D., Song, C., Giannotti, F., & Barabási, A.-L. (2011).** "Human Mobility, Social Ties, and Link Prediction." *KDD '11*, ACM, pp. 1100-1108.
  - **DOI:** https://doi.org/10.1145/2020408.2020581
  - **Link:** https://dl.acm.org/doi/10.1145/2020408.2020581
  - **Why cited:** Studies human mobility patterns and route choice behavior in urban environments

---

## 2️⃣ **PERFORMANCE METRICS (Weight: 30%)**

### Why 30% Weight?
**Our Justification:** System performance is critical for user experience in interactive applications. We allocated 30% because real-time response is essential but secondary to the quality of routes produced.

**Methodological Support:**
- **Nielsen, J. (1993).** "Usability Engineering." *Academic Press/AP Professional*, Boston, ISBN: 0-12-518406-9.
  - **Link:** https://www.nngroup.com/articles/response-times-3-important-limits/
  - **Why cited:** Establishes three response time limits for interactive systems (0.1s, 1.0s, 10s) based on human perception

- **ISO 9241-110:2020.** "Ergonomics of human-system interaction — Part 110: Interaction principles."
  - **Link:** https://www.iso.org/standard/75258.html
  - **Note:** ISO standards require purchase; summary available at link
  - **Why cited:** International standard for interactive system design principles including performance guidelines

---

### Response Time Threshold: 1.0 Second

**Our Threshold:** ≤ 1.0s average response time (based on Nielsen's 1.0s guideline for maintaining user flow)

**Methodological References:**
- **Card, S. K., Moran, T. P., & Newell, A. (1983).** "The Psychology of Human-Computer Interaction." *Lawrence Erlbaum Associates*, Hillsdale, NJ.
  - **Citation:** ISBN: 0-89859-243-7
  - **Google Scholar:** https://scholar.google.com/scholar?q=Card+Moran+Newell+Psychology+Human+Computer+Interaction
  - **Why cited:** Foundational work on human-computer interaction timing and cognitive response to system latency

- **Miller, R. B. (1968).** "Response time in man-computer conversational transactions." *AFIPS Fall Joint Computer Conference*, pp. 267-277.
  - **Link:** https://dl.acm.org/doi/10.1145/1476589.1476628
  - **Why cited:** Early research establishing response time requirements for interactive systems

---

### Statistical Sample Size: n = 30

**Our Choice:** 30 test cases (standard minimum sample size for parametric statistics)

**Methodological References:**
- **Montgomery, D. C. (2017).** "Design and Analysis of Experiments." *9th Edition*, Wiley, ISBN: 978-1119113478.
  - **Publisher:** https://www.wiley.com/en-us/Design+and+Analysis+of+Experiments%2C+9th+Edition-p-9781119113478
  - **Google Scholar:** https://scholar.google.com/scholar?q=Montgomery+Design+Analysis+Experiments+2017
  - **Why cited:** Standard textbook on experimental design; discusses minimum sample sizes for statistical validity (n ≥ 30 for Central Limit Theorem)

---

## 3️⃣ **BPR ACCURACY METRICS (Weight: 20%)**

### Why 20% Weight?
**Our Justification:** BPR function validation confirms our congestion model works correctly. We allocated 20% because accurate traffic modeling is important for realistic routing but not the system's primary function.

**Methodological Support:**
- **Delling, D., Sanders, P., Schultes, D., & Wagner, D. (2009).** "Engineering Route Planning Algorithms." *Algorithmics of Large and Complex Networks*, Springer LNCS 5515, pp. 117-139.
  - **Link:** https://link.springer.com/chapter/10.1007/978-3-642-02094-0_7
  - **Why cited:** Discusses evaluation of route planning algorithms including validation of underlying traffic models

---

### BPR Function Parameters

**Our Parameters:** α = 1.5, β = 8 (chosen for urban HCMC context based on congested street networks)

**Methodological References:**
- **Bureau of Public Roads (BPR). (1964).** "Traffic Assignment Manual." *U.S. Department of Commerce*, Washington, D.C.
  - **Citation:** Original source of BPR function: `t = t₀ × [1 + α(v/c)^β]`
  - **Google Scholar:** https://scholar.google.com/scholar?q=Bureau+Public+Roads+Traffic+Assignment+Manual+1964
  - **Why cited:** Original formulation of the BPR volume-delay function

- **Branston, D. (1976).** "Link Capacity Functions: A Review." *Transportation Research*, 10(4), pp. 223-236.
  - **DOI:** https://doi.org/10.1016/0041-1647(76)90055-1
  - **Google Scholar:** https://scholar.google.com/scholar?q=Branston+Link+Capacity+Functions+Review+1976
  - **Why cited:** Reviews various BPR parameter values used in practice; discusses parameter selection for different road types

- **Spiess, H. (1990).** "Technical Note—Conical Volume-Delay Functions." *Transportation Science*, 24(2), pp. 153-158.
  - **DOI:** https://doi.org/10.1287/trsc.24.2.153
  - **Google Scholar:** https://scholar.google.com/scholar?q=Spiess+Conical+Volume+Delay+Functions+1990
  - **Why cited:** Discusses alternative volume-delay functions and critiques of BPR parameters for different network types

- **Akcelik, R. (1991).** "Travel time functions for transport planning purposes: Davidson's function, its time dependent form and an alternative travel time function." *Australian Road Research*, 21(3), pp. 49-59.
  - **Citation:** Australian Road Research Board (ARRB)
  - **Link:** https://www.researchgate.net/publication/242258239_Travel_time_functions_for_transport_planning_purposes_Davidson's_function_its_time-dependent_form_and_an_alternative_travel_time_function
  - **Alternative:** Search "Akcelik BPR parameters urban" on Google Scholar
  - **Why cited:** Discusses travel time functions and parameter selection for urban road networks

---

### Mean Absolute Error (MAE) Threshold

**Our Threshold:** MAE < 0.2 (determined from our test results - approximately 20% average prediction error)

**Methodological References:**
- **Vlahogianni, E. I., Karlaftis, M. G., & Golias, J. C. (2014).** "Short-term traffic forecasting: Where we are and where we're going." *Transportation Research Part C: Emerging Technologies*, 43(1), pp. 3-19.
  - **Link:** https://www.sciencedirect.com/science/article/abs/pii/S0968090X14000096
  - **Why cited:** Comprehensive review of traffic forecasting methods discussing accuracy measures including MAE for evaluating prediction quality

---

## 4️⃣ **USER EXPERIENCE (UX) METRICS (Weight: 10%)**

### Why 10% Weight?
**Our Justification:** UX metrics measure subjective satisfaction, which is important but less critical than objective routing quality and performance. We allocated 10% as the smallest weight for this supporting criterion.

**Methodological Support:**
- **Hassenzahl, M., & Tractinsky, N. (2006).** "User experience - a research agenda." *Behaviour & Information Technology*, 25(2), pp. 91-97.
  - **Link:** https://www.researchgate.net/publication/233864602_User_experience_-_A_research_agenda
  - **Why cited:** Provides framework for understanding and measuring user experience in interactive systems

---

### UX Metric 1: Success Rate

**Formula:** `Success Rate = (Successful Routes / Total Routes) × 100%`

**Our Threshold:** ≥ 90% (our target based on usability best practices)

**Methodological References:**
- **ISO 9241-11:2018.** "Ergonomics of human-system interaction — Part 11: Usability: Definitions and concepts."
  - **Link:** https://www.iso.org/standard/63500.html
  - **Note:** ISO standards require purchase; summary available at link
  - **Why cited:** International standard defining usability concepts including effectiveness, efficiency, and satisfaction measurement

- **Sauro, J., & Lewis, J. R. (2012).** "Quantifying the User Experience: Practical Statistics for User Research." *Morgan Kaufmann*, ISBN: 978-0123849687.
  - **Google Scholar:** https://scholar.google.com/scholar?q=Sauro+Lewis+Quantifying+User+Experience+2012
  - **Note:** Published book; check university library or Google Books
  - **Why cited:** Practical guide to measuring UX metrics including task success rates in software systems

---

### UX Metric 2: Detour Acceptability

**Formula:** `Detour Ratio = Route Distance / Shortest Path Distance`

**Our Threshold:** ≤ 1.15 (determined empirically - allowing up to 15% detour)

**Methodological References:**
- **Abdel-Aty, M. A., Kitamura, R., & Jovanis, P. P. (1997).** "Using stated preference data for studying the effect of advanced traffic information on drivers' route choice." *Transportation Research Part C: Emerging Technologies*, 5(1), pp. 39-50.
  - **Link:** https://www.sciencedirect.com/science/article/abs/pii/S0968090X9600023X
  - **Why cited:** Studies acceptable detour ratios in driver route choice behavior using stated preference surveys

- **Papinski, D., Scott, D. M., & Doherty, S. T. (2009).** "Exploring the route choice decision-making process: A comparison of planned and observed routes obtained using person-based GPS." *Transportation Research Part F: Traffic Psychology and Behaviour*, 12(4), pp. 347-358.
  - **DOI:** https://doi.org/10.1016/j.trf.2009.04.001
  - **Google Scholar:** https://scholar.google.com/scholar?q=Papinski+Scott+Doherty+2009+route+choice+GPS
  - **Why cited:** Uses GPS tracking to validate route choice models and measure detour patterns in actual travel behavior

---

### UX Metric 3: Route Simplicity (Cognitive Load)

**Formula:** `Simplicity Score = f(num_turns, num_steps, route_complexity)`

**Our Threshold:** ≤ 50 nodes (determined empirically for manageable route complexity)

**Methodological References:**
- **Burnett, G. E. (2009).** "On-the-move and in your car: An overview of HCI issues for in-car computing." *International Journal of Mobile Human Computer Interaction*, 1(1), pp. 60-78.
  - **DOI:** https://doi.org/10.4018/jmhci.2009010104
  - **Google Scholar:** https://scholar.google.com/scholar?q=Burnett+2009+on+the+move+in+your+car+HCI
  - **Why cited:** Discusses cognitive load and HCI issues in navigation systems; examines how route complexity affects driving performance

- **Tom, A., & Denis, M. (2003).** "Referring to landmark or street information in route directions: What difference does it make?" *Spatial Information Theory*, Springer LNCS 2825, pp. 362-374.
  - **DOI:** https://doi.org/10.1007/978-3-540-39923-0_24
  - **Link:** https://link.springer.com/chapter/10.1007/978-3-540-39923-0_24
  - **Why cited:** Studies how route description complexity affects navigation performance and cognitive load

---

### UX Metric 4: Response Stability (Coefficient of Variation)

**Formula:** `CV = σ / μ` (Standard Deviation / Mean)

**Our Threshold:** CV < 0.3 (determined empirically - acceptable performance variation)

**Methodological References:**
- **Abdi, H. (2010).** "Coefficient of variation." *Encyclopedia of Research Design*, Sage Publications, pp. 169-171.
  - **DOI:** https://doi.org/10.4135/9781412961288.n56
  - **Google Scholar:** https://scholar.google.com/scholar?q=Abdi+Coefficient+of+variation+Encyclopedia+Research+Design
  - **Why cited:** Explains coefficient of variation as a statistical measure of relative variability for assessing consistency

---

## 5️⃣ **OVERALL WEIGHTING SCHEME**

### Final Scoring Formula:
```python
Overall Score = (Routing Quality × 0.4) + (Performance × 0.3) + 
                (BPR Accuracy × 0.2) + (UX Score × 0.1)
```

### Our Weight Allocation:
| Criterion          | Weight | Our Rationale |
|--------------------|--------|---------------|
| Routing Quality    | 40%    | Core function - most critical for meeting user needs |
| Performance        | 30%    | Real-time requirement - essential for usability |
| BPR Accuracy       | 20%    | Model validation - important for credibility |
| User Experience    | 10%    | Subjective metrics - supportive role |

**Methodological Support for Multi-Criteria Evaluation:**
- **Saaty, T. L. (1980).** "The Analytic Hierarchy Process." *McGraw-Hill*, New York, ISBN: 0-07-054371-2.
  - **Link:** https://www.sciencedirect.com/science/article/pii/0270025587904738
  - **Why cited:** Provides the Analytic Hierarchy Process (AHP) methodology for structuring and analyzing complex multi-criteria decisions

---

## 6️⃣ **GRADING SCALE**

| Grade | Score Range | Quality Level | Our Interpretation |
|-------|-------------|---------------|-------------------|
| A     | 80-100      | Excellent     | Production-ready system |
| B     | 60-79       | Good          | Minor improvements needed |
| C     | 40-59       | Acceptable    | Significant improvements required |
| D     | 20-39       | Poor          | Major redesign needed |
| F     | 0-19        | Failed        | Does not meet basic requirements |

**Methodological Support:**
- **IEEE Computer Society. (2014).** "SWEBOK: Guide to the Software Engineering Body of Knowledge." *Version 3.0*, IEEE Press.
  - **Link:** https://www.computer.org/education/bodies-of-knowledge/software-engineering
  - **Google Scholar:** https://scholar.google.com/scholar?q=SWEBOK+Guide+Software+Engineering+Body+Knowledge+2014
  - **Why cited:** Standard reference for software engineering practices including quality assessment frameworks

- **ISO/IEC 25010:2011.** "Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE)."
  - **Link:** https://www.iso.org/obp/ui/#iso:std:iso-iec:25010:ed-1:v1:en
  - **Note:** ISO standards require purchase; summary available at link
  - **Why cited:** International standard for software quality evaluation providing quality model and assessment criteria

---

## 7️⃣ **SUMMARY TABLE**

| Evaluation Component | Weight | Key References | Our Threshold (Empirically Determined) |
|---------------------|--------|----------------|--------------------------------------|
| **Routing Quality** | **40%** |  |  |
| └─ Route Diversity | 13.3% | Bader et al. (2011), Abraham et al. (2011) | Jaccard ≤ 0.3 |
| └─ Route Efficiency | 13.3% | Geisberger et al. (2012), Ziebart et al. (2008) | Ratio ≥ 0.95 |
| └─ Congestion Avoidance | 13.3% | Yuan et al. (2010), Wang et al. (2011) | ≥ 0.85 |
| **Performance** | **30%** |  |  |
| └─ Response Time | 30% | Nielsen (1993), Card et al. (1983), ISO 9241-110 | ≤ 1.0s |
| └─ Statistical Validity | - | Montgomery (2017) | n = 30 |
| **BPR Accuracy** | **20%** |  |  |
| └─ MAE | 20% | Vlahogianni et al. (2014) | < 0.2 |
| └─ Model Parameters | - | BPR (1964), Branston (1976), Akcelik (1991) | α=1.5, β=8 |
| **User Experience** | **10%** |  |  |
| └─ Success Rate | 2.5% | ISO 9241-11, Sauro & Lewis (2012) | ≥ 90% |
| └─ Detour Ratio | 2.5% | Abdel-Aty et al. (1997), Papinski et al. (2009) | ≤ 1.15 |
| └─ Route Simplicity | 2.5% | Burnett (2009), Tom & Denis (2003) | ≤ 50 nodes |
| └─ Response Stability | 2.5% | Abdi (2010) | CV < 0.3 |

---

## 📖 **HOW TO DEFEND THIS FRAMEWORK**

### When Asked: "Why These Criteria?"
**Answer:** "We selected criteria based on established practices in route planning research. Papers by Bader et al., Geisberger et al., and Yuan et al. demonstrate that diversity, efficiency, and congestion avoidance are standard metrics for evaluating routing quality. Nielsen and ISO standards establish performance requirements for interactive systems. BPR validation is standard in transportation engineering (BPR 1964, Vlahogianni 2014)."

### When Asked: "Why These Weights?"
**Answer:** "We allocated weights based on functional priority: routing quality (40%) as the core function, performance (30%) for usability, BPR accuracy (20%) for model validation, and UX (10%) for satisfaction. The multi-criteria structure follows Saaty's AHP methodology (1980), and weight allocation reflects our system's primary purpose."

### When Asked: "Why These Thresholds?" 
**HONEST ANSWER:** "The specific threshold values (0.3, 0.95, 0.85, 1.0s, 0.2, etc.) were determined empirically from our 30 test cases. The papers we cite justify the **metrics themselves** - why Jaccard index measures diversity, why efficiency ratio matters, etc. - but the specific cutoff values are based on what we observed in our testing data. For example:
- Jaccard ≤ 0.3: From analyzing our alternative route pairs
- Response ≤ 1.0s: Nielsen's guideline for user flow
- MAE < 0.2: Based on our BPR prediction accuracy
- Success rate ≥ 90%: Common usability target from ISO/Sauro literature
- Other thresholds: Determined from our test result distributions"

### When Asked: "Are These Thresholds From the Papers?"
**HONEST ANSWER:** "No, the specific numerical thresholds are mostly from our empirical data. The papers provide the **measurement methodology** - they tell us **what** to measure and **how** to measure it. For instance, Bader et al. introduced Jaccard for route diversity, but they didn't specify 0.3 as a universal threshold. We chose 0.3 based on analyzing our 30 test case results and determining what level of diversity we consider acceptable for our HCMC routing context."

---

## 📚 **ADDITIONAL READING**

For deeper understanding of routing algorithms and evaluation:

1. **Dijkstra, E. W. (1959).** "A note on two problems in connexion with graphs." *Numerische Mathematik*, 1(1), pp. 269-271.
   - **DOI:** https://doi.org/10.1007/BF01386390
   - **Why:** Foundational shortest path algorithm

2. **Hart, P. E., Nilsson, N. J., & Raphael, B. (1968).** "A Formal Basis for the Heuristic Determination of Minimum Cost Paths." *IEEE Transactions on Systems Science and Cybernetics*, 4(2), pp. 100-107.
   - **DOI:** https://doi.org/10.1109/TSSC.1968.300136
   - **Why:** A* algorithm for efficient pathfinding

3. **Demiryurek, U., Banaei-Kashani, F., & Shahabi, C. (2010).** "A case for time-dependent shortest path computation in spatial networks." *SIGSPATIAL GIS '10*, ACM, pp. 474-477.
  - **Link:** https://dl.acm.org/doi/10.1145/1869790.1869865
   - **Why:** Time-dependent routing with congestion

---

## ✅ **FINAL NOTE**

This evaluation framework combines:
- **Established metrics** from routing research literature
- **Standard practices** from HCI and software engineering
- **Empirical thresholds** determined from our 30 HCMC test cases

The papers cited provide **methodological justification** for our approach. The specific threshold values reflect **our system's context and performance data**.

**For academic defense:** Be clear about what comes from literature (metrics, methods) vs. what comes from your data (thresholds, weights). This is honest, defensible, and standard practice in engineering research.

---

**Document Version:** 2.0 (Truthful Edition)  
**Last Updated:** 2025  
**Author:** SmartFlow Team  
**Purpose:** Academic defense reference for evaluation framework
