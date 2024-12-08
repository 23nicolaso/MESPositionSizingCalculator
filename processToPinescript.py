# put the output of logisticReg.py into a string
a = "hour: 0, y = e^(0.4317) * x^(0.4146) \n\
hour: 1, y = e^(0.6963) * x^(0.4038) \n\
hour: 2, y = e^(0.8890) * x^(0.3934) \n\
hour: 3, y = e^(1.2643) * x^(0.3780) \n\
hour: 4, y = e^(1.1598) * x^(0.3636) \n\
hour: 5, y = e^(1.0435) * x^(0.3335) \n\
hour: 6, y = e^(0.8833) * x^(0.4125) \n\
hour: 7, y = e^(1.0593) * x^(0.3661) \n\
hour: 8, y = e^(1.2996) * x^(0.4512) \n\
hour: 9, y = e^(1.6841) * x^(0.4567) \n\
hour: 10, y = e^(1.9958) * x^(0.3949) \n\
hour: 11, y = e^(1.7477) * x^(0.4157) \n\
hour: 12, y = e^(1.5962) * x^(0.4157) \n\
hour: 13, y = e^(1.5519) * x^(0.4194) \n\
hour: 14, y = e^(1.6135) * x^(0.3785) \n\
hour: 15, y = e^(1.6652) * x^(0.3898) \n\
hour: 16, y = e^(1.0684) * x^(0.3503) \n\
hour: 18, y = e^(0.9012) * x^(0.3915) \n\
hour: 19, y = e^(0.7879) * x^(0.3878) \n\
hour: 20, y = e^(0.8410) * x^(0.4333) \n\
hour: 21, y = e^(0.8210) * x^(0.3991) \n\
hour: 22, y = e^(0.6370) * x^(0.4022) \n\
hour: 23, y = e^(0.4993) * x^(0.4194)"

# process it into pinescript code
# Split the string into lines
lines = a.split('\n')

# Initialize dictionaries to store the exponents
e_exponents = {}
x_exponents = {}

# Process each line to extract the hour and exponents
for line in lines:
    parts = line.split(', ')
    hour = int(parts[0].split(': ')[1])
    e_exp = float(parts[1].split('e^(')[1].split(')')[0])
    x_exp = float(parts[1].split('x^(')[1].split(')')[0])
    
    e_exponents[hour] = e_exp
    x_exponents[hour] = x_exp

# Print the switch-like structure
print("eExponent = switch hr")
for hour, e_exp in e_exponents.items():
    print(f"    {hour} => {e_exp}")

print("\nxExponent = switch hr")
for hour, x_exp in x_exponents.items():
    print(f"    {hour} => {x_exp}")