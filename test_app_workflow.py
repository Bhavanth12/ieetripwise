import urllib.request
import json
import sys

# Ensure UTF-8 stdout on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def test_workflow():
    print("Testing TripWise Web App Endpoints (Live Service Integration)...")
    
    # 1. Root
    req = urllib.request.urlopen('http://127.0.0.1:8050/')
    assert req.status == 200
    print('1. GET / Status: 200 OK')

    # 2. City Meta
    req = urllib.request.urlopen('http://127.0.0.1:8050/api/city_meta?city=Mumbai')
    meta = json.loads(req.read())
    assert meta['city'] == 'Mumbai'
    print(f"2. GET /api/city_meta: {meta['city']} | Currency: {meta['currency']} | Timezone: {meta['timezone']}")

    # 3. POIs
    req = urllib.request.urlopen('http://127.0.0.1:8050/api/pois?city=Mumbai')
    pois = json.loads(req.read())
    assert len(pois) >= 10
    print(f"3. GET /api/pois: Loaded {len(pois)} POIs for Mumbai")

    # 4. Neural Recommendations (TripWiseModel GNN Forward Pass)
    data = json.dumps({'city': 'Mumbai', 'weather': 'clear', 'hour': 9.0, 'category': 'All'}).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8050/api/recommend', data=data, headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    recs = json.loads(res.read())
    assert recs['status'] == 'success'
    top_p = recs['recommendations'][0]
    print(f"4. POST /api/recommend: Top POI: {top_p['name']} | Neural Score: {top_p['score']} (Raw: {top_p['raw_model_score']})")
    print(f"   Explanation: {top_p['explanation']}")

    # 5. Multi-Objective Itinerary Optimization (NSGA-II)
    params = json.dumps({
        'city': 'Mumbai',
        'time_budget': 7.5,
        'monetary_budget': 1500.0,
        'category_focus': 'All',
        'hour': 9.0,
        'weather': 'clear',
        'seed': 42
    }).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8050/api/optimize_itinerary', data=params, headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    itin = json.loads(res.read())
    assert itin['status'] == 'success'
    m = itin['metrics']
    print(f"5. POST /api/optimize_itinerary (NSGA-II): {len(itin['route'])} POIs | Cost: Rs {m['total_cost_inr']} / Rs {m['monetary_budget_inr']} | Duration: {m['total_duration_h']}h / {m['time_budget_h']}h | Pareto Solutions: {m['pareto_solutions_found']} | Status: {m['constraint_status']}")
    for step in itin['route']:
        print(f"   Step {step['step']}: {step['name']} ({step['category']}) | {step['arrival']} - {step['departure']} | {step['transit_mode']} | Rs {step['cost_inr']}")

    # 6. Dynamic Replanning (CMD-MOMDP Under Environmental Shock)
    shock_payload = json.dumps({
        'city': 'Mumbai',
        'current_route': itin['route'],
        'disrupted_step': 2,
        'disruption_type': 'venue_closure',
        'remaining_time_budget': 4.5,
        'remaining_monetary_budget': 1000.0,
        'current_hour': 11.5,
        'weather': 'monsoon',
        'seed': 42
    }).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8050/api/replan_disruption', data=shock_payload, headers={'Content-Type': 'application/json'})
    res = urllib.request.urlopen(req)
    replan = json.loads(res.read())
    assert replan['status'] == 'success'
    rm = replan['metrics']
    ev = replan['disruption_event']
    print(f"6. POST /api/replan_disruption (CMD-MOMDP): Disruption: {ev['disruption_type']} at {ev['disrupted_venue']}")
    print(f"   Replanning Latency: {rm['replanning_latency_ms']} ms | Utility Retention: {rm['utility_retention_pct']}% | Feasibility: {rm['constraint_satisfaction']}")
    print(f"   Replanned Stops: {[p['name'] for p in replan['replanned_route']]}")

if __name__ == "__main__":
    test_workflow()
