from typing import List, Dict


class SchulzeMethod:
    def __init__(self, candidates: List[str], preferences: List[Dict[str, int]]):
        """
        Candidates are a list of strings and preferences are a list of dicts,
        indexed by candidate and with value equal to candidate rank.
        """
        self.candidates = candidates
        self.preferences = preferences

    def strongest_paths(self) -> Dict[str, Dict[str, int]]:
        """
        Simple O(n^3) algo to calculate strongest paths
        """
        paths: Dict[str, Dict[str, int]] = {}
        for each_superior_candidate in self.candidates:
            paths[each_superior_candidate] = {}

            for each_inferior_candidate in self.candidates:
                paths[each_superior_candidate][each_inferior_candidate] = 0

                for prefs in self.preferences:
                    try:
                        if prefs.get(each_superior_candidate) < prefs.get(
                            each_inferior_candidate
                        ):
                            # in this case, the superior candidate is ranked higher means ranked higher
                            paths[each_superior_candidate][each_inferior_candidate] += 1
                    except TypeError:  # Zen
                        pass

        # Floyd-Warshall algo variant impl
        path_strengths: Dict[str, Dict[str, int]] = {}
        for x in self.candidates:
            path_strengths[x] = {}
            for y in self.candidates:
                path_strengths[x][y] = 0
                if x != y:
                    if paths[x][y] > paths[y][x]:  # x is stronger
                        path_strengths[x][y] = paths[x][y]

        for i in self.candidates:
            for j in self.candidates:
                if i != j:
                    for k in self.candidates:
                        if i != k and j != k:
                            path_strengths[j][k] = max(
                                path_strengths[j][k],
                                min(path_strengths[j][i], path_strengths[i][k]),
                            )

        return path_strengths

    def evaluate(self) -> str:
        """
        Find schultze winner, if one exists
        """
        strengths = self.strongest_paths()
        winners = []
        for x in self.candidates:
            if all([strengths[x][y] >= strengths[y][x] for y in self.candidates]):
                winners.append(x)

        try:
            assert (
                len(winners) == 1
            )  # we can only have one winner and we better not have none
        except AssertionError:
            print(winners)
            assert len(winners) == 1

        return winners[0]
