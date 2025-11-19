original = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 15, 16, 18, 20, 23, 24, 25, 27, 28, 31, 33, 34, 35, 36, 37, 38, 39, 40, 43, 47, 49, 51, 52, 54, 55, 56, 57, 59, 61, 62, 63, 64, 66, 68, 73, 74, 77, 78, 79, 81, 82, 83, 84, 85, 86, 87, 88, 91, 92, 93, 94, 95, 98, 99 ]

basic = [ 2, 8, 10, 12, 13, 16, 20, 29, 35, 36, 37, 40, 47, 51, 55, 57, 61, 66, 71, 72, 73, 74, 81, 83, 90, 92, 94, 96 ]

detailed = [ 4, 7, 10, 15, 23, 29, 30, 31, 35, 40, 41, 43, 44, 45, 46, 68, 79, 81, 82, 84, 85, 86, 92, 93, 95, 98 ]

minimal = [ 0, 1, 5, 8, 23, 27, 28, 40, 46, 52, 65, 78, 79, 84, 85, 88, 91 ]

structured = [ 1, 6, 10, 16, 17, 28, 31, 33, 34, 35, 37, 39, 41, 43, 44, 46, 51, 52, 54, 57, 61, 62, 64, 65, 69, 71, 72, 74, 76, 79, 80, 83, 84, 85, 87, 88, 91, 99 ]


og_set = set(original)

count_basic_new = 0
for idx in basic:
        if not idx in og_set: count_basic_new += 1
print(f"Basic new: {count_basic_new}")

count_detailed_new = 0
for idx in detailed:
        if not idx in og_set: count_detailed_new += 1
print(f"Detailed new: {count_detailed_new}")

count_minimal_new = 0
for idx in minimal:
        if not idx in og_set: count_minimal_new += 1
print(f"Minimal new: {count_minimal_new}")

count_structured_new = 0
for idx in structured:
        if not idx in og_set: count_structured_new += 1
print(f"Structured new: {count_structured_new}")


total = set(original)
total.update(basic)
total.update(detailed)
total.update(structured)

print(f"Theoretical max(og+basic+detailed+structured): {len(total)}; original: {len(og_set)}; Diff +{len(total) - len(og_set)}")
