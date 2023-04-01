# IAM GAAD Combine
# ----------------
# This script navigates the present working directory to
# collect and ingest all files ending with "*-gaad.json"
# and combine them into a final "combined-gaad.json".
# Run `aws iam get-account-authorization-details` for all
# accounts and save the resulting JSON results as files
# with name like "<profile>-gaad.json". Store all of the
# JSON files in a single folder and run this script from
# that folder to build the combined JSON file.

import json
import os

def combine_gaad_files():
    files = [file for file in os.listdir(".") if file.endswith("gaad.json")]
    combined = {"UserDetailList":[], "GroupDetailList":[], "RoleDetailList":[], "Policies":[]}

    for file in files:
        if file == "combined-gaad.json":
            continue
        f = open(file)
        data = json.load(f)
        f.close()
        for i in data["UserDetailList"]:
            combined["UserDetailList"].append(i)
        for i in data["GroupDetailList"]:
            combined["GroupDetailList"].append(i)
        for i in data["RoleDetailList"]:
            combined["RoleDetailList"].append(i)
        for i in data["Policies"]:
            combined["Policies"].append(i)

    f = open("combined-gaad.json", "w")
    json.dump(combined, f)
    f.close()

if __name__ == "__main__":
    combine_gaad_files()
