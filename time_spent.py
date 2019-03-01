import glob
import json
import os

# TODO
"""
Running with zip file input
Add in lat/lon functionality
ask for home location (+lat/lon)
add in total life time spent

"""

def time_spent(rootdir = "/home/patrick/Documents/PSFeb19", HOMEINCLUDED = False, home = "GB"):
    """
    takes in base directory of a Polarsteps data request
    and returns the time spent (in seconds) in each country
    if trips are not started and ended at home set HOMEINCLUDED = True
    to include the bookend steps
    accounted_for tracks the time in the users history that has been
    allocated a country, for possible future functionality
    """
    homelat = 0
    homelon = 0

    rootdir = rootdir + "/trip/**/*"
    file_list = [f for f in glob.iglob(rootdir, recursive=True) if os.path.isfile(f)]
    location_list = []
    for f in file_list:
        if f[-9:] == "trip.json":
            location_list.append(f)

    if not location_list:
        return None

    trips = []
    j = 0
    accounted_for = []
    for file in location_list:
        trips.append([])
        with open(file, "r") as f:
            data = json.load(f)
            for i in data["all_steps"]:
                trips[j].append([i["start_time"], i["location"]["country_code"],
                            i["location"]["lon"], i["location"]["lat"]])
            if HOMEINCLUDED:
                end = data["end_date"]
                trips[j].append([end, home, homelon, homelat])

        j += 1

    countries = {}
    for trip in trips:
        start_time = None
        end_time = None
        first_step = True
        started = None
        for step in trip:
            if (not HOMEINCLUDED) and first_step:
                first_step = False
                continue
            if start_time:
                end_time = step[0]
                time = end_time - start_time
                try:
                    countries[country] += time
                except KeyError:
                    countries[country] = time
            start_time = step[0]
            country = step[1]
            if not started:
                started = start_time
        accounted_for.append([started, start_time])
    return countries

if __name__=="__main__":
    time_spent()
