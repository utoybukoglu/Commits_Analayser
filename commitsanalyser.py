import matplotlib.pyplot as plt
import sys


# The specify_features_of_classification_schema is a helper function designed to specify the features,
# and their corresponding counts for a particular committer based on the given class_schema.
def specify_features_of_classification_schema(committer, class_schema, nested_dict):
    tempDict = {}
    if class_schema == "SwM":
        tempDict['Adaptive Tasks'] = nested_dict[committer]['SwM'][0]
        tempDict['Corrective Tasks'] = nested_dict[committer]['SwM'][1]
        tempDict['Perfective Tasks'] = nested_dict[committer]['SwM'][2]
    elif class_schema == "NFR":
        tempDict['Maintainability'] = nested_dict[committer]['NFR'][0]
        tempDict['Usability'] = nested_dict[committer]['NFR'][1]
        tempDict['Functionality'] = nested_dict[committer]['NFR'][2]
        tempDict['Reliability'] = nested_dict[committer]['NFR'][3]
        tempDict['Efficiency'] = nested_dict[committer]['NFR'][4]
        tempDict['Portability'] = nested_dict[committer]['NFR'][5]
    else:
        tempDict['Forward Engineering'] = nested_dict[committer]['SoftEvol'][0]
        tempDict['Re-Engineering'] = nested_dict[committer]['SoftEvol'][1]
        tempDict['Corrective Engineering'] = nested_dict[committer]['SoftEvol'][2]
        tempDict['Management'] = nested_dict[committer]['SoftEvol'][3]

    return tempDict


# The create_barchart_given_classification_schema is a helper function to create a bar chart
# for a particular developer based on the given class_schema.
def create_barchart_given_classification_schema(tempDict, committer, class_schema):
    features = list(tempDict)
    values = list(tempDict.values())
    plt.bar(features, values)
    plt.xlabel('Features')
    plt.ylabel('Total Number of Commits')
    plt.title(f'Comparison for {committer}\'s Commits Classified by {class_schema}')
    plt.show()


# The create_barchart_given_feature_all_developer is a helper function to create a bar chart
# for all developers based on the given feature.
def create_barchart_given_feature_all_developer(tempDict, feature):
    features = list(tempDict)
    values = list(tempDict.values())
    plt.bar(features, values)
    plt.xlabel('Committers')
    plt.ylabel('Total Number of Commits')
    plt.title(f"Comparison for All Committers' Commits Classified by {feature}")
    plt.show()


# The compare_commits_classification_schema compares the number of commits done by a particular committer
# for a given classification class_schema.
def compare_commits_classification_schema(committer, class_schema, nested_dict):
    tempDict = specify_features_of_classification_schema(committer, class_schema, nested_dict)
    create_barchart_given_classification_schema(tempDict, committer, class_schema)


# The compare_commits_given_feature compares the number of commits done by all developers,
# which are classified with a given class_schema and feature.
def compare_commits_given_feature(class_schema, feature, nested_dict):
    all_committer_feature = {}
    for committer in nested_dict:
        tempDict = specify_features_of_classification_schema(committer, class_schema, nested_dict)
        all_committer_feature[committer] = tempDict[feature]
    
    create_barchart_given_feature_all_developer(all_committer_feature, feature)


# The max_committer_given_feature finds the developer who has the maximum number of commits with given feature.
def max_committer_given_feature(class_schema, feature, nested_dict):
    all_committer_feature = {}
    for committer in nested_dict:
        tempDict = specify_features_of_classification_schema(committer, class_schema, nested_dict)
        all_committer_feature[committer] = tempDict[feature]
        
    print(f"\nThe maximum number of commits for {feature} done by committer {max(zip(all_committer_feature.values(), all_committer_feature.keys()))[1]}.")


def schema_menu():
    print("\nPlease select one of the classification schemas:")
    print("[1] Swanson's Maintenance Tasks")
    print("[2] NFR Labelling")
    print("[3] Software Evolution tasks")


def swm_menu():
    print("\nPlease select the feature:")
    print("[1] Adaptive Tasks")
    print("[2] Corrective Tasks")
    print("[3] Perfective Tasks")


def nfr_menu():
    print("\nPlease select the feature:")
    print("[1] Maintainability")
    print("[2] Usability")
    print("[3] Functionality")
    print("[4] Reliability")
    print("[5] Efficiency")
    print("[6] Portability")


def softevol_menu():
    print("\nPlease select the feature:")
    print("[1] Forward Engineering")
    print("[2] Re-Engineering")
    print("[3] Corrective Engineering")
    print("[4] Management")

def main():

    classification_Dict = {"SwM": ["Adaptive Tasks", "Corrective Tasks", "Perfective Tasks"], 
                       "NFR": ["Maintainability", "Usability", "Functionality", "Reliability", "Efficiency", "Portability"],
                       "SoftEvol": ["Forward Engineering", "Re-Engineering", "Corrective Engineering", "Management"]}

    filename1 = sys.argv[1] # commits.txt
    filename2 = sys.argv[2] # identifies.txt

    try:
        commits = open(filename1, "r")
    except IOError:
        print(f"File '{filename1}' could not be opened.")
        sys.exit(1)

    try:
        identifies = open(filename2, "r")
    except IOError:
        print(f"File '{filename2}' could not be opened.")
        sys.exit(1)

    commits.readline() # skip the first line
    identifies.readline() # skip the first line

    nested_dict = {} # main dictionary
    user_dict = {} # sub dictionary

    for line in identifies:
        identify = line.split(",")
        ID = identify[0]
        user_name = identify[1]
        user_dict[ID] = user_name
        if user_name not in nested_dict:
            nested_dict[user_name] = {"SwM": [0, 0, 0], "NFR": [0, 0, 0, 0, 0, 0], "SoftEvol": [0, 0, 0, 0]}

    identifies.close()

    for line in commits:
        commit = line.split(",")[0:15]

        for i in range(0, 3):
            nested_dict[user_dict[commit[14]]]["SwM"][i] += int(commit[i+1])

        for i in range(0, 6):
            nested_dict[user_dict[commit[14]]]["NFR"][i] += int(commit[i+4])

        for i in range(0, 4):
            nested_dict[user_dict[commit[14]]]["SoftEvol"][i] += int(commit[i+10])

    commits.close()

    while True:
        print("\n*********************************************** MENU **********************************************")
        print("[1] Compare the number of commits done by a particular developer for a given classification scheme")
        print("[2] Compare the number of commits done by all developers, which are classified with a given feature")
        print("[3] Print the developer with the maximum number of commits for a given feature")
        print("[4] Exit")
        print("***************************************************************************************************\n")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            try:
                schema_menu()
                classification_choice = int(input("\nEnter your choice (1-3): "))

                # Check the user input is a valid integer between 1 and 3.
                if classification_choice not in [1, 2, 3]:
                    raise ValueError("Invalid input. Please enter a number between 1 and 3.")
                classification = list(classification_Dict)[classification_choice - 1]

                print("\nPlease select the committer:")

                counter = 1
                for committer in nested_dict:
                    print(f"[{counter}] {committer}")
                    counter += 1
            
                committer = int(input(f"\nEnter your choice (1-{(counter - 1)}): "))

                # Check the user input is a valid integer between 1 and number of committers (counter-1).
                if committer not in list(range(1, counter)):
                    raise ValueError(f"Invalid input. Please enter a number between 1 and {counter - 1}.")

                # Call the function based on the selected committer and classification scheme.
                commiterName = list(nested_dict)[committer - 1]
                compare_commits_classification_schema(commiterName, classification, nested_dict)

            except ValueError as ve:
                print(f"Error: {ve}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        elif choice == '2':
            try:
                schema_menu()
                classification_choice = int(input("\nEnter your choice (1-3): "))

                # Check the user input is a valid integer between 1 and 3.
                if classification_choice not in [1, 2, 3]:
                    raise ValueError("Invalid input. Please enter a number between 1 and 3.")

                if classification_choice == 1:
                    swm_menu()
                    feature_choice = int(input("\nEnter your choice (1-3): "))

                    # Check the user input is a valid integer between 1 and 3.
                    if feature_choice not in [1, 2, 3]:
                        raise ValueError("Invalid input. Please enter a number between 1 and 3.")

                    # Call the function based on the selected classification scheme and its corresponding feature.
                    compare_commits_given_feature("SwM", classification_Dict["SwM"][feature_choice - 1], nested_dict)

                elif classification_choice == 2:
                    nfr_menu()
                    feature_choice = int(input("\nEnter your choice (1-6): "))

                    # Check the user input is a valid integer between 1 and 6.
                    if feature_choice not in [1, 2, 3, 4, 5, 6]:
                        raise ValueError("Invalid input. Please enter a number between 1 and 6.")

                    # Call the function based on the selected classification scheme and its corresponding feature.
                    compare_commits_given_feature("NFR", classification_Dict["NFR"][feature_choice - 1], nested_dict)

                else:
                    softevol_menu()
                    feature_choice = int(input("\nEnter your choice (1-4): "))

                    # Check the user input is a valid integer between 1 and 4.
                    if feature_choice not in [1, 2, 3, 4]:
                        raise ValueError("Invalid input. Please enter a number between 1 and 4.")

                    # Call the function based on the selected classification scheme and its corresponding feature.
                    compare_commits_given_feature("SoftEvol", classification_Dict["SoftEvol"][feature_choice - 1], nested_dict)

            except ValueError as ve:
                print(f"Error: {ve}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        elif choice == '3':
            try:
                schema_menu()
                classification_choice = int(input("\nEnter your choice (1-3): "))

                # Check the user input is a valid integer between 1 and 3.
                if classification_choice not in [1, 2, 3]:
                    raise ValueError("Invalid input. Please enter a number between 1 and 3.")

                if classification_choice == 1:
                    swm_menu()
                    feature_choice = int(input("\nEnter your choice (1-3): "))

                    # Check the user input is a valid integer between 1 and 3.
                    if feature_choice not in [1, 2, 3]:
                        raise ValueError("Invalid input. Please enter a number between 1 and 3.")

                    # Call the function based on the selected classification scheme and its corresponding feature.
                    max_committer_given_feature("SwM", classification_Dict["SwM"][feature_choice - 1], nested_dict)

                elif classification == 2:
                    nfr_menu()
                    feature_choice = int(input("\nEnter your choice (1-6): "))

                    # Check the user input is a valid integer between 1 and 6.
                    if feature_choice not in [1, 2, 3, 4, 5, 6]:
                        raise ValueError("Invalid input. Please enter a number between 1 and 6.")

                    # Call the function based on the selected classification scheme and its corresponding feature.
                    max_committer_given_feature("NFR", classification_Dict["NFR"][feature_choice - 1], nested_dict)
                else:
                    softevol_menu()
                    feature_choice = int(input("\nEnter your choice (1-4): "))

                    # Check the user input is a valid integer between 1 and 4.
                    if feature_choice not in [1, 2, 3, 4]:
                        raise ValueError("Invalid input. Please enter a number between 1 and 4.")

                    # Call the function based on the selected classification scheme and its corresponding feature.
                    max_committer_given_feature("SoftEvol", classification_Dict["SoftEvol"][feature_choice - 1], nested_dict)

            except ValueError as ve:
                print(f"Error: {ve}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        elif choice == '4':
            print("\nExiting the program. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()