from schulze import SchulzeMethod
import csv
import copy
from typing import List, Dict, Tuple


def nab_prefs(
    results: List[Dict[str, str]], filter_string: str, weights: Dict[str, int]
) -> Tuple[List[str], List[Dict[str, int]]]:
    """
    Filters for office prefs and returns them in a list of candidates and a list of dicts of ints
    """
    prefs = []
    choices = set()
    count = 0
    for ballot in results:
        if isinstance(ballot, dict):
            try:
                count += 1
                ballot_ranks = {}
                for choice, rank in ballot.items():
                    if filter_string.lower() in choice.lower():
                        if rank:
                            choices.add(choice)
                            ballot_ranks[choice] = int(rank[0])
                        else:
                            ballot_ranks[choice] = len(ballot.items()) + 1

                prefs.extend([ballot_ranks] * weights[ballot["Username"].rstrip()])

            except KeyError:
                pass

    print(f"{count} votes counted!")

    return list(choices), prefs


def calculate_winner(candidates, prefs) -> str:
    calculator = SchulzeMethod(candidates, prefs)
    return calculator.evaluate()


def drop_winner(winner: str, results: List[Dict[str, str]]):
    """
    Drop winners for the next, lower round of elections
    """
    dropped_results = []

    for each_result in results:
        keys_to_drop = []

        for key in each_result.keys():
            if winner in key:
                keys_to_drop.append(key)

        for key in keys_to_drop:
            del each_result[key]

        dropped_results.append(each_result)

    return dropped_results


if __name__ == "__main__":
    with open("runs/2021-elections/2021-election-responses.csv") as f:
        raw_results = [copy.deepcopy(x) for x in csv.DictReader(f)]

    weights = {}
    with open("runs/2021-elections/attendance.csv", "r") as f:
        for each_line in f.readlines():
            email = each_line.split("|")[0].rstrip()
            weight = int(each_line.split("|")[1].rstrip())
            if weight >= 4:
                weights[email] = weight + 4
            else:
                weights[email] = 0
                # print(email, "has", weights[email], "weight")

    # Presidency election calculations
    p_cands, p_prefs = nab_prefs(raw_results, "president", weights)
    p_winner, p_strength = calculate_winner(p_cands, p_prefs)
    p_winner = p_winner.split("[")[1].split("]")[0]
    print(p_winner, p_strength)

    # Vice Presidency election calculations
    raw_vp_results = drop_winner(p_winner, raw_results)
    vp_cands, vp_prefs = nab_prefs(raw_vp_results, "vice", weights)
    vp_winner, vp_strength = calculate_winner(vp_cands, vp_prefs)
    vp_winner = vp_winner.split("[")[1].split("]")[0]
    print(vp_winner, vp_strength)

    # Secretary election calculations
    raw_s_results = drop_winner(p_winner, raw_vp_results)
    s_cands, s_prefs = nab_prefs(raw_s_results, "secretary", weights)
    s_winner, s_strength = calculate_winner(s_cands, s_prefs)
    s_winner = s_winner.split("[")[1].split("]")[0]
    print(s_winner, s_strength)
