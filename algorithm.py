# sample input data: list of dictionaries
data = [
    {"name": "John", "salary": 50000},
    {"name": "Jane", "salary": 60000},
    {"name": "John", "salary": 70000},
    {"name": "Bob",  "salary": 45000},
    {"name": "Jane", "salary": 65000},
]

# ---------------------------
# Step 1: Collect salaries by name
# ---------------------------
salaries_by_name = {}  # name -> list of salaries

for row in data:
    name = row["name"]
    salary = row["salary"]
    # initialize list if name not seen
    if name not in salaries_by_name:
        salaries_by_name[name] = []
    salaries_by_name[name].append(salary)
# {John: [50000, 70000], Jane: [60000, 65000], Bob: [45000]}
# ---------------------------
# Step 2: Identify names with more than one salary
# ---------------------------
names_with_multiple_salaries = []
for name, sal_list in salaries_by_name.items():
    if len(sal_list) > 1:
        names_with_multiple_salaries.append(name)
# [Jone, Jane]
# ---------------------------
# Step 3: Compute max salary for each selected name
# ---------------------------
max_salary_by_name = {}  # name -> max salary
for name in names_with_multiple_salaries:
    max_salary_by_name[name] = max(salaries_by_name[name])
# {John: 70000, Jane: 65000}
# ---------------------------
# Step 4: Print the name and the max salary
# ---------------------------
for name, max_salary in max_salary_by_name.items():
    print(f"Name: {name}  |  Max Salary: {max_salary}")