"""
For investments over $1M it can be typically assumed that they will return 5% forever.
Using the [2022 - 2023 JMU Cost of Attendance](https://www.jmu.edu/financialaid/learn/cost-of-attendance-undergrad.shtml),
calculate how much a rich alumnus would have to give to pay for one full year (all costs) for an in-state student
and an out-of-state student. Store your final answer in the variables: "in_state_gift" and "out_state_gift".

Note: this problem does not require the "compounding interest" formula from the previous problem.

"""

### Your code here ###

# annual rate of return
rate = 0.05

# Calculate the yearly cost for in-state and out-of-state
in_state_sem = 30792
out_state_sem = 47882

# Calculate how much large of a gift to pay for tuition with the return
in_state_gift = in_state_sem / rate
out_state_gift = out_state_sem / rate

# Print responses
print("In-state gift amount:", in_state_gift)
print("Out-of-state gift amount:", out_state_gift)