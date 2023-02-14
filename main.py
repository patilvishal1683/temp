import yaml
import sys

PARAMETER_NOT_PRESENT = []
PARAMETER_NOT_PRESENT_COMPAIR = []
PARAMETER_MISMATCH = []
# Read Values File and convert it into Dict Data Structure
file_name = "f1.yaml"
# file_path = f"./rc/charts/system1-enterprise/{file_name}"
with open(file_name, 'r') as file:
    # AWS File Converted into Dict
    MAIN_FILE_YML_DICT = yaml.safe_load(file)

values_file_path = "f2.yaml"
with open(values_file_path, 'r') as file:
    # Values File Converted Into Dict
    COMPAIR_FILE_DICT = yaml.safe_load(file)


# FUNCTION TO CHECK VALUES FROM BOTH FILES
def check_parameters(file_1_values, file_2_values) -> None:
    # print("Hello")
    try:
        file1_key = [param['name'] for param in file_1_values]
        file2_key = [param['name'] for param in file_2_values]
        # print(file1_key)
        # print(file2_key)
        for f1_key in file1_key:
            if f1_key == "autoscaling.enabled" or f1_key == "extraEnv":
                continue
            if f1_key not in file2_key:
                PARAMETER_MISMATCH.append(f1_key)

    except Exception as e:
        pass


# Recursive Function For Searching Inside Dict
def check_inside_values(**kwargs):
    try:
        # GET KEYS OF FROM BOTH FILES
        MIAN_FILE_KEYS = list(kwargs['val_1'].keys())
        # print(MIAN_FILE_KEYS)
        COMPAIR_FILE_KEYS = list(kwargs['val_2'].keys())
        # print(COMPAIR_FILE_KEYS)

        # LOOP TO CHECK IF KEYS ARE PRESENT
        for key in MIAN_FILE_KEYS:
            # print(key)
            if key in COMPAIR_FILE_KEYS:

                # VARIABLES : STORES KEY FROM BOTH FILES
                SOURCE_FILE = kwargs['val_1'][key]
                COMPAIR_FILE_KEY_CHECK = kwargs['val_2'][key]

                # FURTHURE CHECK IF KEY VALUE PAIR IS OF TYPE DICT IF YES THEN RECURSIVE FUNCTION CALL
                if isinstance(SOURCE_FILE, dict) and isinstance(COMPAIR_FILE_KEY_CHECK, dict):
                    check_inside_values(val_1=SOURCE_FILE, val_2=COMPAIR_FILE_KEY_CHECK)

                # FURTHURE CHECK IF KEY VALUE PAIR IS OF TYPE LIST IF YES THEN RECURSIVE FUNCTION CALL
                elif isinstance(SOURCE_FILE, list) and isinstance(COMPAIR_FILE_KEY_CHECK, list):
                    # print("hello")
                    # CHECK EACH VALUE IN PARAMETERS
                    if key == "parameters":
                        # print("hello")
                        check_parameters(file_1_values=SOURCE_FILE, file_2_values=COMPAIR_FILE_KEY_CHECK)

                    # FURTHURE CHECK IF KEY VALUE PAIR IN LIST
                    for inside_list1, inside_list2 in zip(SOURCE_FILE, COMPAIR_FILE_KEY_CHECK):
                        check_inside_values(val_1=inside_list1, val_2=inside_list2)
            else:
                if key == "helm":
                    for val in kwargs['val_1'][key].get('parameters'):
                        if val.get('name') == "autoscaling.enabled" or val.get('name') == "extraEnv":
                            continue
                        else:
                            PARAMETER_NOT_PRESENT_COMPAIR.append(val.get('name'))
                if key == "parameters":
                    for val in kwargs['val_1'][key]:
                        if val.get('name') == "autoscaling.enabled" or val.get('name') == "extraEnv":
                            continue
                        else:
                            PARAMETER_NOT_PRESENT_COMPAIR.append(val.get('name'))
                    # print(kwargs['val_1'][key])
                # if {key: kwargs['val_1'][key]} not in WARNING_MISMATCH:
                #     WARNING_MISMATCH.append({key: kwargs['val_1'][key]})
    except Exception as e:
        # print(e)
        pass


"""
START OF THE PROGRAM
"""
MAIN_FILE = MAIN_FILE_YML_DICT.keys()
FILE_TO_COMPAIR_WITH = COMPAIR_FILE_DICT.keys()
for _KEY in MAIN_FILE:
    # print(_KEY)
    try:
        # KEYS_EMPTY_IN_VALUES
        if _KEY in FILE_TO_COMPAIR_WITH:
            # FIRST LAYER TYPE CHECKS
            if isinstance(MAIN_FILE_YML_DICT[_KEY], dict) and isinstance(COMPAIR_FILE_DICT[_KEY], dict):
                check_inside_values(val_1=MAIN_FILE_YML_DICT[_KEY], val_2=COMPAIR_FILE_DICT[_KEY])

            elif isinstance(MAIN_FILE_YML_DICT[_KEY], list) and isinstance(COMPAIR_FILE_DICT[_KEY], list):
                for val1, val2 in zip(MAIN_FILE_YML_DICT[_KEY], COMPAIR_FILE_DICT[_KEY]):
                    check_inside_values(val_1=val1, val_2=val2)
        else:
            if {_KEY: MAIN_FILE_YML_DICT[_KEY]} in PARAMETER_NOT_PRESENT:
                pass
            else:
                PARAMETER_NOT_PRESENT.append({_KEY: MAIN_FILE_YML_DICT[_KEY]})
    except Exception as e:
        continue

# RAISING ERROR IF ANY OF THE PARAMETER IS MISSING
# if len(WARNING_MISMATCH) > 0:
#     print(" ⚠⚠⚠ WARNING ⚠⚠⚠")
#     print("Below are the Values which are missing when compared file")
#     for val in WARNING_MISMATCH:
#         print(val)
if len(PARAMETER_MISMATCH) > 0 or len(PARAMETER_NOT_PRESENT_COMPAIR) > 0:

    print("\nMissing Keys {} {}".format(PARAMETER_MISMATCH, PARAMETER_NOT_PRESENT_COMPAIR))