# /src/gate.py

from collections import deque

class Gate:
    def __init__(self):
        # Defines the repeating pattern: Fastpass, Regular, Regular, Regular
        self._pattern = ["fastpass", "regular", "regular", "regular"]
        # Cycle pointer (0, 1, 2, 3)
        self._idx = 0
        # Queues using deque
        self._fast = deque() 
        self._reg = deque()  

    def arrive(self, line: str, person_id: str) -> None:
        """Enqueue into the chosen line."""
        if line == "fastpass":
            self._fast.append(person_id)
        elif line == "regular":
            self._reg.append(person_id)

    def _get_line_queue(self, line_type: str) -> deque:
        """Helper to get the correct queue object."""
        return self._fast if line_type == "fastpass" else self._reg

    def serve(self) -> str:
        """
        Return the next person based on the F,R,R,R pattern, skipping empty lines.
        Advances the cycle pointer whether a person is served or skipped.
        Raises IndexError if BOTH queues are completely empty after checking the cycle.
        """
        # Loop up to 4 times (the pattern length) to find an available person
        for _ in range(len(self._pattern)):
            required_line = self._pattern[self._idx]
            queue = self._get_line_queue(required_line)

            # Check if the required line is non-empty
            if queue:
                served_person = queue.popleft()
                
                # Advance the cycle pointer for the NEXT call
                self._idx = (self._idx + 1) % len(self._pattern)
                return served_person
            
            # Line was empty: Advance the cycle pointer (skip) and continue the loop
            self._idx = (self._idx + 1) % len(self._pattern)
        
        # If the loop finishes, both lines are empty.
        raise IndexError("Both lines are empty, no one to serve.")

    def peek_next_line(self) -> str or None:
        """
        Determines which line type has the next available person, following the pattern.
        Does NOT modify the internal cycle pointer (_idx).
        """
        current_idx = self._idx
        
        # Try up to 4 times to find a non-empty line without modifying self._idx
        for _ in range(len(self._pattern)):
            required_line = self._pattern[current_idx]
            queue = self._get_line_queue(required_line)

            if queue:
                return required_line
            
            # Advance index for the next peek check
            current_idx = (current_idx + 1) % len(self._pattern)
            
        # If the loop finishes, both lines are empty.
        return None