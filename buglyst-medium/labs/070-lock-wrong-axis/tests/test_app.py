import threading
import time

from helper import reset_locks, slot_lock


def setup_function():
    reset_locks()


def test_same_caller_can_reserve_different_slots_concurrently():
    """Different slots for one caller should not block each other."""
    slot_b_finished = threading.Event()

    def hold_slot_a():
        with slot_lock("alice", "slot-a"):
            slot_b_finished.wait(timeout=1.0)

    def reserve_slot_b():
        with slot_lock("alice", "slot-b"):
            slot_b_finished.set()

    thread_a = threading.Thread(target=hold_slot_a)
    thread_b = threading.Thread(target=reserve_slot_b)

    thread_a.start()
    time.sleep(0.01)
    thread_b.start()

    thread_b.join(timeout=0.5)
    assert slot_b_finished.is_set(), "slot-b should finish while slot-a is still held"
    slot_b_finished.set()
    thread_a.join(timeout=1.0)


def test_same_slot_still_serializes():
    peak_inside = {"value": 0}
    gate = threading.Barrier(2)

    def reserve():
        gate.wait()
        with slot_lock("bob", "slot-1"):
            peak_inside["value"] = max(peak_inside["value"], peak_inside.get("inside", 0) + 1)
            peak_inside["inside"] = peak_inside.get("inside", 0) + 1
            assert peak_inside["inside"] == 1
            time.sleep(0.02)
            peak_inside["inside"] -= 1

    threads = [threading.Thread(target=reserve) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert peak_inside["value"] == 1
