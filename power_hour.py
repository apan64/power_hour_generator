TOTAL_HOURS = 24
DRINKING_SLOTS = 2
hours = [4 if i in range(6, 9) else 3 if i in range(9, 13) else 2 if i in range(13, 20) else 1 for i in range(TOTAL_HOURS)]
# hours should correspond to appropriate weights
# 0: 9pm, 3: midnight, 6: 3am, 9: 6am, 12: 9am, 15: noon, 18: 3pm, 21: 6pm, 23: 8pm
# average value comes out to 2
# with 2 people per hour, 48 total slots = 96 sum, assuming ~30 people, everyone should be around 3.2 weight, will handle this calc later

def convert_hour_to_val(hour):
    if 'am' in hour.lower():
        ans = int(hour[:hour.lower().index('am')]) + 3
        return 3 if ans == 15 else ans
    ans = int(hour[:hour.lower().index('pm')]) + 3
    return ans - 9 if ans >= 12 else ans


def gen_schedule(preferences={}):
    '''
    preferences is a dict mapping from person name -> Tuple[List[preferred timeslots], List[silver bullet slots]]

    assumes nobody selects a timeslot as both a preferred and a silver bulleted slot

    output: Tuple[List[Tuple[drinker1, drinker2]], Dict[people -> their totaled weights]]
    '''
    people_weights = {}
    people_to_assign = set()
    assignments = [[] for __ in range(TOTAL_HOURS)]
    time_bullets = [[] for __ in range(TOTAL_HOURS)]
    time_prefs = [[] for __ in range(TOTAL_HOURS)]
    expected_weight = TOTAL_HOURS * DRINKING_SLOTS * (sum(hours) / len(hours)) / len(preferences)

    for p, p_tuple in preferences.items():
        pref_times, bullets = p_tuple
        for b in bullets:
            time_bullets[convert_hour_to_val(b)].append(p)
        for t in pref_times:
            time_prefs[convert_hour_to_val(t)].append(p)
        people_weights[p] = 0
        people_to_assign.add(p)

    # handle preferences first, then we'll do assignment to avoid penalizing later preference selection
    for i, weight in enumerate(hours):
        drinkers = []
        if len(time_prefs):
            org = sorted(time_prefs[i], key=people_weights.get)
            drinkers = org if len(org) == 1 else org[:2]
            for d in drinkers:
                people_weights[d] += weight
        assignments[i] = drinkers

    # handle assignment using expected weight
    for i, weight in enumerate(hours):
        drinkers = assignments[i]
        if len(drinkers) == 2:
            continue
        sorted_people = sorted(people_to_assign, key=people_weights.get)
        for p in sorted_people:
            if p not in time_bullets[i]:
                drinkers.append(p)
                people_weights[p] += weight
                if people_weights[p] > expected_weight:
                    people_to_assign.remove(p)
                if len(drinkers) == 2:
                    break

    if len(people_to_assign):
        print('people with weights below the expected average: {}'.format(people_to_assign))

    return assignments, people_weights


if __name__ == '__main__':
    test_data = {
                    'q': (['9am', '6am'], ['5pm', '3am', '10pm']),
                    'w': (['9pm', '4pm'], ['2am', '3am', '4am']),
                    'e': (['12am', '7am'], ['11pm', '11am', '4am']),
                    'r': (['6pm', '5am'], ['9pm', '9am', '2am']),
                    't': (['6am', '4pm'], ['5pm', '11pm', '10am']),
                    'y': (['12am', '2pm'], ['10am', '3pm', '10am']),
                    'u': (['2pm', '9pm'], ['10am', '5pm', '2pm']),
                    'i': (['2am', '1am'], ['12pm', '12am', '11am']),
                    'o': (['8am', '7am'], ['8am', '4pm', '4am']),
                    'p': (['4am', '9pm'], ['10am', '12pm', '3pm']),
                    'a': (['6pm', '6am'], ['10am', '5am', '2pm']),
                    's': (['6pm', '3pm'], ['10pm', '6am', '8am']),
                    'd': (['6pm', '4pm'], ['10pm', '2pm', '8am']),
                    'f': (['5am', '7pm'], ['3am', '1pm', '3pm']),
                    'g': (['10pm', '9pm'], ['5pm', '6am', '8pm']),
                    'h': (['11am', '3am'], ['4pm', '4am', '5pm']),
                    'j': (['12pm', '7pm'], ['12pm', '4am', '6pm']),
                    'k': (['4am', '3am'], ['1pm', '4am', '12am']),
                    'l': (['1pm', '4pm'], ['3am', '8pm', '1pm']),
                    'z': (['1am', '6pm'], ['4pm', '12am', '7pm']),
                    'x': (['12am', '7pm'], ['4pm', '2pm', '5pm']),
                    'c': (['12am', '4pm'], ['7pm', '10am', '11pm']),
                    'v': (['4pm', '8am'], ['9pm', '12pm', '4am']),
                    'b': (['7am', '8am'], ['3pm', '5am', '11am']),
                    'n': (['10am', '12pm'], ['7pm', '7pm', '9am']),
                    'm': (['12am', '2am'], ['6am', '5am', '8pm']),
                    ',': (['6pm', '3am'], ['4am', '7pm', '10am']),
                    '.': (['5am', '3pm'], ['1pm', '3pm', '3pm']),
                }
    assignments, people_weights = gen_schedule(test_data)
    print(assignments)
    print(people_weights)
