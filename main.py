from functions import *

df = load_data('students.csv')
df = calculate_average(df)
df = add_result_columns(df)

print("=== Student Performance Analytics ===")
print(df)

print("\n--- Topper Student ---")
print(get_topper(df)[['Name','Department','Average','Grade']])

print("\n--- Subject Wise Average ---")
print(subject_wise_avg(df))

print("\n--- Department Wise Performance ---")
print(df.groupby('Department')['Average'].mean().round(2))

df.to_csv('final_report.csv', index=False)
print("\nFinal report saved as final_report.csv")