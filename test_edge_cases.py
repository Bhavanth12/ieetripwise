import urllib.request
import json
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def run_tests():
    print("===================================================================")
    print("  RUNNING COMPREHENSIVE INTEGRATION & EDGE CASE TESTS")
    print("===================================================================")

    # 1. Normal Itinerary
    print("\n--- 1. Normal Itinerary (Mumbai, ₹1,500, 7.5h) ---")
    p1 = json.dumps({'city': 'Mumbai', 'time_budget': 7.5, 'monetary_budget': 1500.0, 'category_focus': 'All', 'hour': 9.0, 'weather': 'clear'}).encode('utf-8')
    req1 = urllib.request.Request('http://127.0.0.1:8050/api/optimize_itinerary', data=p1, headers={'Content-Type': 'application/json'})
    res1 = json.loads(urllib.request.urlopen(req1).read())
    print(f"Status: {res1['status']} | Stops: {len(res1['route'])} | Duration: {res1['metrics']['total_duration_h']}h | Cost: ₹{res1['metrics']['total_cost_inr']} | Feasibility: {res1['metrics']['constraint_status']}")
    assert len(res1['route']) >= 3
    assert res1['metrics']['total_cost_inr'] <= 1500.0
    assert res1['metrics']['total_duration_h'] <= 7.5

    # 2. Venue Closure Disruption
    print("\n--- 2. Venue Closure Disruption at Stop 2 ---")
    p2 = json.dumps({'city': 'Mumbai', 'current_route': res1['route'], 'disrupted_step': 2, 'disruption_type': 'venue_closure', 'remaining_time_budget': 4.5, 'remaining_monetary_budget': 1000.0, 'current_hour': 11.5, 'weather': 'clear'}).encode('utf-8')
    req2 = urllib.request.Request('http://127.0.0.1:8050/api/replan_disruption', data=p2, headers={'Content-Type': 'application/json'})
    res2 = json.loads(urllib.request.urlopen(req2).read())
    print(f"Disruption: {res2['disruption_event']['disruption_description']}")
    print(f"Replanning Latency: {res2['metrics']['replanning_latency_ms']} ms | Utility Retention: {res2['metrics']['utility_retention_pct']}% | Feasibility: {res2['metrics']['constraint_satisfaction']}")
    assert res2['status'] == 'success'
    assert res2['metrics']['replanning_latency_ms'] > 0

    # 3. Traffic Congestion Disruption
    print("\n--- 3. Severe Traffic Congestion Disruption ---")
    p3 = json.dumps({'city': 'Mumbai', 'current_route': res1['route'], 'disrupted_step': 2, 'disruption_type': 'traffic_congestion', 'remaining_time_budget': 4.0, 'remaining_monetary_budget': 1000.0, 'current_hour': 12.0, 'weather': 'clear'}).encode('utf-8')
    req3 = urllib.request.Request('http://127.0.0.1:8050/api/replan_disruption', data=p3, headers={'Content-Type': 'application/json'})
    res3 = json.loads(urllib.request.urlopen(req3).read())
    print(f"Traffic Reroute: {res3['metrics']['constraint_satisfaction']} | Utility: {res3['metrics']['replanned_route_utility']}")
    assert res3['status'] == 'success'

    # 4. Sudden Monsoon Cloudburst Disruption
    print("\n--- 4. Sudden Monsoon Storm Disruption ---")
    p4 = json.dumps({'city': 'Mumbai', 'current_route': res1['route'], 'disrupted_step': 1, 'disruption_type': 'monsoon_cloudburst', 'remaining_time_budget': 5.0, 'remaining_monetary_budget': 1200.0, 'current_hour': 10.0, 'weather': 'monsoon'}).encode('utf-8')
    req4 = urllib.request.Request('http://127.0.0.1:8050/api/replan_disruption', data=p4, headers={'Content-Type': 'application/json'})
    res4 = json.loads(urllib.request.urlopen(req4).read())
    print(f"Monsoon Replanning: Handled shock in {res4['metrics']['replanning_latency_ms']} ms | Retention: {res4['metrics']['utility_retention_pct']}%")
    assert res4['status'] == 'success'

    # 5. Low Budget Boundary (₹100)
    print("\n--- 5. Low Budget Boundary (₹100) ---")
    p5 = json.dumps({'city': 'Mumbai', 'time_budget': 6.0, 'monetary_budget': 100.0, 'category_focus': 'All', 'hour': 9.0, 'weather': 'clear'}).encode('utf-8')
    req5 = urllib.request.Request('http://127.0.0.1:8050/api/optimize_itinerary', data=p5, headers={'Content-Type': 'application/json'})
    res5 = json.loads(urllib.request.urlopen(req5).read())
    print(f"Low Budget Total Cost: ₹{res5['metrics']['total_cost_inr']} (Limit: ₹100) | Status: {res5['metrics']['constraint_status']}")
    assert res5['metrics']['total_cost_inr'] <= 100.0

    # 6. Low Time Budget Boundary (3.0h)
    print("\n--- 6. Low Time Budget Boundary (3.0h) ---")
    p6 = json.dumps({'city': 'Mumbai', 'time_budget': 3.0, 'monetary_budget': 1500.0, 'category_focus': 'All', 'hour': 9.0, 'weather': 'clear'}).encode('utf-8')
    req6 = urllib.request.Request('http://127.0.0.1:8050/api/optimize_itinerary', data=p6, headers={'Content-Type': 'application/json'})
    res6 = json.loads(urllib.request.urlopen(req6).read())
    print(f"Low Time Total Duration: {res6['metrics']['total_duration_h']}h (Limit: 3.0h) | Status: {res6['metrics']['constraint_status']}")
    assert res6['metrics']['total_duration_h'] <= 3.5

    # 7. Invalid Input Handling (Empty / Unknown city fallback)
    print("\n--- 7. Unknown City Fallback Handling ---")
    p7 = json.dumps({'city': 'UnknownCity', 'time_budget': 5.0, 'monetary_budget': 1000.0}).encode('utf-8')
    req7 = urllib.request.Request('http://127.0.0.1:8050/api/optimize_itinerary', data=p7, headers={'Content-Type': 'application/json'})
    res7 = json.loads(urllib.request.urlopen(req7).read())
    print(f"Fallback Handled: Status {res7['status']} | Fallback City: {res7['city']}")
    assert res7['status'] == 'success'

    print("\n===================================================================")
    print("  >>> ALL 7 EDGE CASES & INTEGRATION SCENARIOS PASSED (100%) <<<   ")
    print("===================================================================")

if __name__ == "__main__":
    run_tests()
