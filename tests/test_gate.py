# /tests/test_gate.py

import pytest
import sys, os
# Path fix to allow 'from src.gate import Gate' to work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) 

from src.gate import Gate

def test_ratio_and_skips():
    g = Gate()
    g.arrive("regular","r1"); g.arrive("regular","r2"); g.arrive("regular","r3")
    g.arrive("fastpass","f1")
    # pattern F,R,R,R
    assert g.serve() == "f1"
    assert g.serve() == "r1"
    assert g.serve() == "r2"
    assert g.serve() == "r3"
    with pytest.raises(IndexError):
        g.serve()

def test_peek_next_line():
    g = Gate()
    assert g.peek_next_line() is None
    g.arrive("regular","r1")
    assert g.peek_next_line() == "regular"
    g.arrive("fastpass","f1")
    assert g.peek_next_line() == "fastpass"


# --- Edge Cases ---
def test_edge_serve_when_both_empty():
    g = Gate()
    with pytest.raises(IndexError):
        g.serve()
    assert g.peek_next_line() is None

def test_edge_pattern_wrap_with_sparse_lines():
    g = Gate()
    # Only fastpass riders arrive; ensure cycle still advances correctly
    g.arrive("fastpass", "f1"); g.arrive("fastpass", "f2")
    assert g.peek_next_line() == "fastpass"
    assert g.serve() == "f1"   # consume F slot
    # pattern would point to R, but it's empty; serving should skip to F
    assert g.serve() == "f2"
    with pytest.raises(IndexError):
        g.serve()

# --- Longer Scenario (CORRECTED to serve 7 people) ---
def test_long_mixed_arrivals_and_service():
    g = Gate()
    # Seed queues (5 regulars + 2 fastpass = 7 total people)
    for i in range(1, 6):
        g.arrive("regular", f"r{i}")
    g.arrive("fastpass", "f1"); g.arrive("fastpass", "f2")
    
    served = []
    # ITERATE 7 TIMES (the number of people available)
    for _ in range(7):
        served.append(g.serve())
        
    assert len(served) == 7
    assert served.count("f1") + served.count("f2") == 2
    assert sum(1 for s in served if s.startswith("r")) == 5 
    
    # Check that the next serve (the 8th) raises an error
    with pytest.raises(IndexError):
        g.serve()