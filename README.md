# TripWise Research Platform

**IEEE Transactions on Knowledge and Data Engineering (TKDE) / Intelligent Transportation Systems (TITS)**  
*TripWise: Jointly Learned Context-Aware Personalized Recommendation and Multi-Objective Itinerary Optimization under Dynamic Spatio-Temporal Constraints*

---

## 1. System Overview

**TripWise** unifies context-aware deep representation learning with multi-objective Pareto itinerary optimization and online dynamic re-optimization:
1. **Context-Aware Deep Scoring Head** (`ml/proposed_model/`): Bipartite LightGCN graph propagation + Gated Residual Context Encoder + Multi-Head Cross-Attention + Spatio-Temporal Physics Kernel $\phi(u,v,c)$ + Direct Collaborative Inner Product Grounding $\mathbf{e}_u^\top \mathbf{e}_v$.
2. **Multi-Objective Itinerary Optimizer** (`optimization/`): Elitist NSGA-II solver with 2-Opt local refinement across 4 conflicting objectives: Personalized Preference Utility ($f_1$), Calibrated Multi-Modal Transit Time ($f_2$), Category Shannon Diversity ($f_3$), and Monetary Cost ($f_4$).
3. **Online Closed-Loop Dynamic Re-Optimizer** (`web/services/replanning_service.py`): Online dynamic adaptation preserving visited prefixes, updating context (weather, congestion, closures), rescoring remaining candidates, and running suffix NSGA-II with median 10.77 ms latency and zero constraint violations.
4. **India-First Interactive Platform** (`web/`): Live interactive dashboard deployed at `http://127.0.0.1:8050` across Indian metropolitan settings (Mumbai, Delhi, Bengaluru, Jaipur, Varanasi) with curated authentic POI geometry and synthetic mobility.

---

## 2. Reproduction & Experiment Execution Commands

### Reproduce Full IEEE Empirical Campaign (Tables 1 through 6)
```bash
python experiments/run_full_ieee_campaign.py
```
*Generates:*
* `results/ieee_campaign/TABLE_1_DATASET_STATISTICS.csv`
* `results/ieee_campaign/TABLE_2_CONVERGENCE.csv`
* `results/ieee_campaign/TABLE_3_MULTI_SEED_BASELINES.csv`
* `results/ieee_campaign/TABLE_4_ABLATION_STUDY.csv`
* `results/ieee_campaign/TABLE_5_OPTIMIZER_COMPARISON.csv`
* `results/ieee_campaign/TABLE_6_DYNAMIC_REPLANNING_SUMMARY.csv`
* `results/ieee_campaign/TABLE_6_DYNAMIC_REPLANNING_TRIALS.csv`

### Reproduce Contextual Evaluation, Dual-Axis Ablation & Planner Benchmarks (Tables 7 through 12)
```bash
python experiments/run_contextual_evaluation.py
```
*Generates:*
* `results/ieee_campaign/TABLE_7_CONTEXTUAL_EVALUATION.csv`
* `results/ieee_campaign/TABLE_8_CONTEXTUAL_BASELINES.csv`
* `results/ieee_campaign/TABLE_9_DUAL_TASK_ABLATION.csv`
* `results/ieee_campaign/TABLE_10_PLANNER_UTILITY_COMPARISON.csv`
* `results/ieee_campaign/TABLE_11_PARETO_ANALYSIS.csv`
* `results/ieee_campaign/TABLE_12_REPLANNING_LATENCY_DISTRIBUTION.csv`

### Validate Indian POI Vocabulary & Invariance
```bash
python experiments/validate_indian_model_integration.py
```

### Validate ML Web Integration & Provenance
```bash
python experiments/validate_ml_web_integration.py
```

### Launch Interactive Web Application
```bash
python web/app.py
```
*Open your browser at: **`http://127.0.0.1:8050`***

---

## 3. Provenance & Modality Classification

* **Foursquare NYC (TSMC2014)**: Real human LBSN check-ins (1,083 users, 3,837 POIs, 97,587 interactions). Legitimate empirical ML benchmark with strict chronological splitting.
* **Indian Metropolitan Urban Corpus**: Curated Real POI Geometry (coordinates, prices, categories, opening hours) + Synthetic Mobility (150 users, 34 POIs, 6,000 interactions).
