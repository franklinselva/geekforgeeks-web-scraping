import csv
import pandas as pd

def remove_empty(input_file = './data/college_list.csv', output_file = './data/college.csv'):
    with open(input_file) as in_file:
        with open(output_file, 'w') as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if row:
                    writer.writerow(row)

def remove_duplicates(filename = './data/questions_data.csv', to_file = './data/Corrected_data.csv'):
    data = pd.read_csv(filename, names=['user', 'college', 'category', 'problems', 'problem_link'], low_memory=False, index_col=False) 
    new_data = data.drop_duplicates() 

    new_data.sort_values(by=["user"], ascending=True)
    new_data.to_csv(to_file, mode='a', index=False)

def add_names(from_file = './data/users_data.csv', to_file = './data/questions_data.csv'):
    users =pd.read_csv(from_file, names=['user', 'user_link'])
    data = pd.read_csv(to_file, names=['user', 'college', 'category', 'problems', 'problem_link'])

    for user in users['user']:
        for dat in data:        
            if user is dat['user'] and dat['user'] is not '-':
                pass
            elif dat['user'] is '-':
                pass

if __name__ == "__main__":
    remove_duplicates(filename='questions_data_1.csv')